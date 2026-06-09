"""OpenTelemetry helpers for AI tokenomics and chargeback workshops.

The helper records low-cardinality owner dimensions as metrics and span attributes.
It intentionally avoids prompt text, user IDs, session IDs, and request IDs.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, MutableMapping

from opentelemetry import metrics, trace


METER_NAME = "splunk.workshop.ai.tokenomics"

REQUIRED_DIMENSIONS = (
    "ai.team",
    "ai.cost_center",
    "ai.tenant.id",
    "ai.workload.name",
    "ai.product_area",
    "deployment.environment",
    "gen_ai.request.model",
)

UNKNOWN = "unknown"


@dataclass(frozen=True)
class TokenRate:
    input_usd_per_1k: float
    output_usd_per_1k: float


DEFAULT_RATE_CARD: Mapping[str, TokenRate] = {
    "meta/llama-3.2-1b-instruct": TokenRate(
        input_usd_per_1k=0.00020,
        output_usd_per_1k=0.00125,
    ),
    "default": TokenRate(
        input_usd_per_1k=0.00020,
        output_usd_per_1k=0.00125,
    ),
}


meter = metrics.get_meter(METER_NAME)

input_tokens_counter = meter.create_counter(
    "ai.tokens.input",
    unit="{token}",
    description="Input tokens attributed for AI chargeback.",
)
output_tokens_counter = meter.create_counter(
    "ai.tokens.output",
    unit="{token}",
    description="Output tokens attributed for AI chargeback.",
)
total_tokens_counter = meter.create_counter(
    "ai.tokens.total",
    unit="{token}",
    description="Total tokens attributed for AI chargeback.",
)
request_counter = meter.create_counter(
    "ai.request.count",
    unit="{request}",
    description="AI requests included in chargeback.",
)
estimated_cost_counter = meter.create_counter(
    "ai.request.estimated_cost_usd",
    unit="USD",
    description="Estimated AI request cost from the active workshop rate card.",
)


def dimensions_from_headers(
    headers: Mapping[str, str],
    defaults: Mapping[str, str] | None = None,
) -> dict[str, str]:
    """Build safe chargeback dimensions from request headers and defaults."""

    defaults = defaults or {}
    dimensions = {
        "ai.team": headers.get("x-ai-team") or defaults.get("ai.team", UNKNOWN),
        "ai.cost_center": headers.get("x-ai-cost-center")
        or defaults.get("ai.cost_center", UNKNOWN),
        "ai.tenant.id": headers.get("x-ai-tenant-id")
        or defaults.get("ai.tenant.id", UNKNOWN),
        "ai.workload.name": defaults.get("ai.workload.name", UNKNOWN),
        "ai.product_area": defaults.get("ai.product_area", UNKNOWN),
        "deployment.environment": defaults.get("deployment.environment", UNKNOWN),
    }
    return normalize_dimensions(dimensions)


def normalize_dimensions(dimensions: Mapping[str, str]) -> dict[str, str]:
    """Return bounded, string-only metric dimensions."""

    normalized: MutableMapping[str, str] = {}
    for key in REQUIRED_DIMENSIONS:
        value = dimensions.get(key, UNKNOWN)
        normalized[key] = _safe_dimension_value(value)
    return dict(normalized)


def estimate_request_cost_usd(
    prompt_tokens: int,
    completion_tokens: int,
    model: str,
    rate_card: Mapping[str, TokenRate] = DEFAULT_RATE_CARD,
) -> float:
    """Estimate request cost from a simple per-1k-token rate card."""

    rate = rate_card.get(model, rate_card["default"])
    input_cost = (prompt_tokens / 1000.0) * rate.input_usd_per_1k
    output_cost = (completion_tokens / 1000.0) * rate.output_usd_per_1k
    return input_cost + output_cost


def record_llm_chargeback(
    *,
    prompt_tokens: int,
    completion_tokens: int,
    model: str,
    dimensions: Mapping[str, str],
    rate_card: Mapping[str, TokenRate] = DEFAULT_RATE_CARD,
) -> float:
    """Record token and cost metrics for one completed LLM request."""

    total_tokens = prompt_tokens + completion_tokens
    attributes = normalize_dimensions(
        {
            **dimensions,
            "gen_ai.request.model": model,
        }
    )
    estimated_cost = estimate_request_cost_usd(
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        model=model,
        rate_card=rate_card,
    )

    input_tokens_counter.add(prompt_tokens, attributes)
    output_tokens_counter.add(completion_tokens, attributes)
    total_tokens_counter.add(total_tokens, attributes)
    request_counter.add(1, attributes)
    estimated_cost_counter.add(estimated_cost, attributes)

    span = trace.get_current_span()
    if span and span.is_recording():
        for key, value in attributes.items():
            span.set_attribute(key, value)
        span.set_attribute("gen_ai.usage.prompt_tokens", prompt_tokens)
        span.set_attribute("gen_ai.usage.completion_tokens", completion_tokens)
        span.set_attribute("gen_ai.usage.total_tokens", total_tokens)
        span.set_attribute("ai.request.estimated_cost_usd", estimated_cost)

    return estimated_cost


def _safe_dimension_value(value: object) -> str:
    text = str(value or UNKNOWN).strip().lower()
    if not text:
        return UNKNOWN
    return text[:128]
