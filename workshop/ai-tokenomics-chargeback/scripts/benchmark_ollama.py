#!/usr/bin/env python3
"""Benchmark a local Ollama model and derive internal token economics.

This script uses Ollama's native /api/generate endpoint because the final response
includes prompt token count, output token count, and phase durations.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


DEFAULT_PROMPTS = [
    "Explain GPU chargeback for AI inference in two concise paragraphs.",
    "List five metrics that help allocate shared AI infrastructure cost.",
    "Write a short incident summary for a slow local LLM request.",
]


@dataclass
class Sample:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    total_duration_s: float
    prompt_eval_duration_s: float
    eval_duration_s: float
    wall_duration_s: float


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Benchmark local Ollama throughput and derive token rates."
    )
    parser.add_argument("--url", default="http://localhost:11434")
    parser.add_argument("--model", required=True, help="Ollama model name, for example llama3.2:1b")
    parser.add_argument("--iterations", type=int, default=3)
    parser.add_argument("--num-predict", type=int, default=160)
    parser.add_argument("--prompt", action="append", help="Prompt to run. Can be passed more than once.")
    parser.add_argument(
        "--accelerator-hourly-usd",
        type=float,
        default=0.0,
        help="Hourly hardware, cloud, or internal GPU proxy rate.",
    )
    parser.add_argument(
        "--support-hourly-usd",
        type=float,
        default=0.0,
        help="Optional hourly license, support, or platform labor allocation.",
    )
    parser.add_argument("--power-watts", type=float, default=0.0)
    parser.add_argument("--electricity-usd-per-kwh", type=float, default=0.17)
    parser.add_argument("--overhead-percent", type=float, default=15.0)
    parser.add_argument("--json-out", help="Optional path to write the full JSON result.")
    args = parser.parse_args()

    prompts = args.prompt or DEFAULT_PROMPTS
    samples: list[Sample] = []

    for iteration in range(args.iterations):
        for prompt in prompts:
            try:
                samples.append(run_generate(args.url, args.model, prompt, args.num_predict))
            except urllib.error.URLError as exc:
                print(f"Unable to reach Ollama at {args.url}: {exc}", file=sys.stderr)
                print("Start Ollama and pull the model, for example: ollama pull llama3.2:1b", file=sys.stderr)
                return 2

    result = summarize(args, samples)
    print_summary(result)

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as handle:
            json.dump(result, handle, indent=2)
            handle.write("\n")

    return 0


def run_generate(url: str, model: str, prompt: str, num_predict: int) -> Sample:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": num_predict,
        },
    }
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        f"{url.rstrip('/')}/api/generate",
        data=body,
        headers={"content-type": "application/json"},
        method="POST",
    )

    start = time.perf_counter()
    with urllib.request.urlopen(request, timeout=300) as response:
        data = json.loads(response.read().decode("utf-8"))
    wall_duration_s = time.perf_counter() - start

    prompt_tokens = int(data.get("prompt_eval_count", 0) or 0)
    completion_tokens = int(data.get("eval_count", 0) or 0)
    total_tokens = prompt_tokens + completion_tokens

    return Sample(
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
        total_duration_s=ns_to_seconds(data.get("total_duration")),
        prompt_eval_duration_s=ns_to_seconds(data.get("prompt_eval_duration")),
        eval_duration_s=ns_to_seconds(data.get("eval_duration")),
        wall_duration_s=wall_duration_s,
    )


def summarize(args: argparse.Namespace, samples: list[Sample]) -> dict[str, Any]:
    prompt_tokens = sum(sample.prompt_tokens for sample in samples)
    completion_tokens = sum(sample.completion_tokens for sample in samples)
    total_tokens = sum(sample.total_tokens for sample in samples)

    prompt_eval_seconds = sum(sample.prompt_eval_duration_s for sample in samples)
    eval_seconds = sum(sample.eval_duration_s for sample in samples)
    total_duration_seconds = sum(sample.total_duration_s for sample in samples)
    wall_seconds = sum(sample.wall_duration_s for sample in samples)

    energy_hourly_usd = (args.power_watts / 1000.0) * args.electricity_usd_per_kwh
    base_hourly_usd = args.accelerator_hourly_usd + args.support_hourly_usd + energy_hourly_usd
    effective_hourly_usd = base_hourly_usd * (1 + args.overhead_percent / 100.0)

    input_usd_per_1m = phase_cost_per_1m(
        effective_hourly_usd,
        prompt_tokens,
        prompt_eval_seconds,
    )
    output_usd_per_1m = phase_cost_per_1m(
        effective_hourly_usd,
        completion_tokens,
        eval_seconds,
    )
    blended_usd_per_1m = phase_cost_per_1m(
        effective_hourly_usd,
        total_tokens,
        total_duration_seconds or wall_seconds,
    )

    return {
        "model": args.model,
        "samples": len(samples),
        "token_counts": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
        },
        "durations_seconds": {
            "prompt_eval": prompt_eval_seconds,
            "completion_eval": eval_seconds,
            "reported_total": total_duration_seconds,
            "wall_total": wall_seconds,
        },
        "throughput_tokens_per_second": {
            "prompt_eval": safe_div(prompt_tokens, prompt_eval_seconds),
            "completion_eval": safe_div(completion_tokens, eval_seconds),
            "reported_total": safe_div(total_tokens, total_duration_seconds),
            "wall_total": safe_div(total_tokens, wall_seconds),
        },
        "hourly_cost_usd": {
            "accelerator": args.accelerator_hourly_usd,
            "support": args.support_hourly_usd,
            "energy": energy_hourly_usd,
            "base": base_hourly_usd,
            "overhead_percent": args.overhead_percent,
            "effective": effective_hourly_usd,
        },
        "derived_token_rates_usd_per_1m": {
            "input": input_usd_per_1m,
            "output": output_usd_per_1m,
            "blended": blended_usd_per_1m,
        },
        "per_sample": [sample.__dict__ for sample in samples],
        "notes": [
            "Input and output rates are phase-based: hourly cost multiplied by prompt or completion phase time.",
            "Use a market proxy, hardware amortization, or energy-only hourly rate depending on the lab goal.",
        ],
    }


def print_summary(result: dict[str, Any]) -> None:
    rates = result["derived_token_rates_usd_per_1m"]
    throughput = result["throughput_tokens_per_second"]
    hourly = result["hourly_cost_usd"]

    print(f"Model: {result['model']}")
    print(f"Samples: {result['samples']}")
    print(f"Effective hourly cost: ${hourly['effective']:.6f}")
    print(f"Prompt throughput: {throughput['prompt_eval']:.2f} tokens/sec")
    print(f"Output throughput: {throughput['completion_eval']:.2f} tokens/sec")
    print(f"Derived input rate: ${rates['input']:.6f} per 1M tokens")
    print(f"Derived output rate: ${rates['output']:.6f} per 1M tokens")
    print(f"Derived blended rate: ${rates['blended']:.6f} per 1M tokens")


def phase_cost_per_1m(hourly_usd: float, tokens: int, seconds: float) -> float:
    if hourly_usd <= 0 or tokens <= 0 or seconds <= 0:
        return 0.0
    phase_cost = hourly_usd * (seconds / 3600.0)
    return (phase_cost / tokens) * 1_000_000.0


def ns_to_seconds(value: Any) -> float:
    try:
        return float(value or 0) / 1_000_000_000.0
    except (TypeError, ValueError):
        return 0.0


def safe_div(numerator: float, denominator: float) -> float:
    if denominator <= 0:
        return 0.0
    return numerator / denominator


if __name__ == "__main__":
    raise SystemExit(main())
