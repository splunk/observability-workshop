from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, request
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


INSTRUMENTATION_DIR = Path(__file__).resolve().parents[1] / "instrumentation"
sys.path.insert(0, str(INSTRUMENTATION_DIR))

from tokenomics_instrumentation import (  # noqa: E402
    TokenRate,
    dimensions_from_headers,
    record_llm_chargeback,
)


SERVICE_NAME = os.getenv("OTEL_SERVICE_NAME", "local-tokenomics-llm-app")
DEPLOYMENT_ENVIRONMENT = os.getenv("DEPLOYMENT_ENVIRONMENT", "local-tokenomics-workshop")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")
DEFAULT_NUM_PREDICT = int(os.getenv("OLLAMA_NUM_PREDICT", "180"))
INPUT_USD_PER_1M = float(os.getenv("INPUT_USD_PER_1M", "0.20"))
OUTPUT_USD_PER_1M = float(os.getenv("OUTPUT_USD_PER_1M", "1.25"))


def create_app() -> Flask:
    configure_otel()

    app = Flask(__name__)
    FlaskInstrumentor().instrument_app(app)
    tracer = trace.get_tracer(__name__)

    @app.get("/health")
    def health() -> tuple[dict[str, str], int]:
        return {"status": "ok", "model": OLLAMA_MODEL}, 200

    @app.post("/ask")
    def ask() -> tuple[Any, int]:
        payload = request.get_json(silent=True) or {}
        question = payload.get("question") or payload.get("prompt")
        if not question:
            return {"error": "Provide question or prompt in the JSON body."}, 400

        scenario = str(payload.get("scenario", "normal"))
        model = str(payload.get("model", OLLAMA_MODEL))
        num_predict = int(payload.get("num_predict", DEFAULT_NUM_PREDICT))
        prompt = build_prompt(str(question), scenario)
        dimensions = dimensions_from_headers(request.headers, default_dimensions(scenario))

        with tracer.start_as_current_span("local_ollama.generate") as span:
            span.set_attribute("ai.scenario", scenario)
            span.set_attribute("gen_ai.request.model", model)
            span.set_attribute("gen_ai.request.max_tokens", num_predict)
            span.set_attribute("ai.prompt.characters", len(prompt))

            try:
                started = time.perf_counter()
                ollama_response = call_ollama(model, prompt, num_predict)
                wall_duration_ms = (time.perf_counter() - started) * 1000.0
            except urllib.error.URLError as exc:
                span.record_exception(exc)
                return {
                    "error": f"Unable to reach Ollama at {OLLAMA_BASE_URL}",
                    "detail": str(exc),
                    "hint": f"Run: ollama pull {model} && ollama serve",
                }, 502

            prompt_tokens = int(ollama_response.get("prompt_eval_count", 0) or 0)
            completion_tokens = int(ollama_response.get("eval_count", 0) or 0)
            estimated_cost = record_llm_chargeback(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                model=model,
                dimensions=dimensions,
                rate_card=rate_card_for(model),
            )

            span.set_attribute("http.client.duration_ms", wall_duration_ms)
            span.set_attribute("ai.scenario.estimated_cost_usd", estimated_cost)

        return {
            "answer": ollama_response.get("response", ""),
            "model": model,
            "scenario": scenario,
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens,
            },
            "estimated_cost_usd": estimated_cost,
            "chargeback": dimensions,
        }, 200

    return app


def configure_otel() -> None:
    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
    insecure = endpoint.startswith("http://")
    resource = Resource.create(
        {
            "service.name": SERVICE_NAME,
            "service.namespace": "ai-tokenomics",
            "deployment.environment": DEPLOYMENT_ENVIRONMENT,
            "ai.workload.name": os.getenv("AI_WORKLOAD_NAME", "local-ollama-chat"),
            "ai.product_area": os.getenv("AI_PRODUCT_AREA", "ai-platform"),
        }
    )

    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint, insecure=insecure))
    )
    trace.set_tracer_provider(tracer_provider)

    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint=endpoint, insecure=insecure),
        export_interval_millis=5000,
    )
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])

    from opentelemetry import metrics

    metrics.set_meter_provider(meter_provider)


def call_ollama(model: str, prompt: str, num_predict: int) -> dict[str, Any]:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": num_predict,
        },
    }
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{OLLAMA_BASE_URL.rstrip('/')}/api/generate",
        data=body,
        headers={"content-type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=300) as response:
        return json.loads(response.read().decode("utf-8"))


def build_prompt(question: str, scenario: str) -> str:
    if scenario == "surge":
        repeated_context = "\n".join(
            [
                "Customer transcript chunk: The user asks for a detailed explanation of AI chargeback, token budgets, rate cards, and GPU utilization.",
            ]
            * 35
        )
        return f"{repeated_context}\n\nQuestion: {question}\nAnswer in detail."

    if scenario == "misuse":
        return (
            "You are running a bulk proposal-generation job through an interactive chat endpoint. "
            "Generate a comprehensive answer with assumptions, risks, pricing, and implementation steps.\n\n"
            f"Question: {question}"
        )

    return question


def default_dimensions(scenario: str = "normal") -> dict[str, str]:
    dimensions = {
        "ai.team": os.getenv("AI_TEAM_DEFAULT", "support-ai"),
        "ai.cost_center": os.getenv("AI_COST_CENTER_DEFAULT", "cc-ml-1200"),
        "ai.tenant.id": os.getenv("AI_TENANT_ID_DEFAULT", "tenant-local"),
        "ai.workload.name": os.getenv("AI_WORKLOAD_NAME", "local-ollama-chat"),
        "ai.product_area": os.getenv("AI_PRODUCT_AREA", "ai-platform"),
        "deployment.environment": DEPLOYMENT_ENVIRONMENT,
    }
    if scenario == "unknown":
        dimensions["ai.team"] = "unknown"
        dimensions["ai.cost_center"] = "unknown"
        dimensions["ai.tenant.id"] = "tenant-unmapped"
        dimensions["ai.workload.name"] = "unmapped-local-test"
    return dimensions


def rate_card_for(model: str) -> dict[str, TokenRate]:
    token_rate = TokenRate(
        input_usd_per_1k=INPUT_USD_PER_1M / 1000.0,
        output_usd_per_1k=OUTPUT_USD_PER_1M / 1000.0,
    )
    return {
        model: token_rate,
        "default": token_rate,
    }


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
