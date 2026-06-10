#!/usr/bin/env python3
"""ShopMate Sports standalone retail/chat app."""

from __future__ import annotations

import json
import math
import os
import re
import time
import traceback
import asyncio
from contextlib import nullcontext
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

try:
    from openai import AsyncOpenAI
    from agents import Agent, ModelSettings, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled
except ImportError:  # pragma: no cover - optional runtime dependency
    AsyncOpenAI = None
    Agent = None
    ModelSettings = None
    OpenAIChatCompletionsModel = None
    Runner = None
    function_tool = None
    set_tracing_disabled = None

try:
    from agents import gen_trace_id, trace as agent_trace
except ImportError:  # pragma: no cover - optional runtime dependency
    agent_trace = None
    gen_trace_id = None

try:
    from opentelemetry import trace as otel_trace
    from opentelemetry.trace import Status, StatusCode
except ImportError:  # pragma: no cover - optional runtime dependency
    otel_trace = None
    Status = None
    StatusCode = None


APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR / "static"
CATALOG_PATH = APP_DIR / "data" / "catalog.json"
INVENTORY_PATH = APP_DIR / "data" / "inventory.json"
POLICIES_PATH = APP_DIR / "data" / "policies.json"
STORE_PATH = APP_DIR / "data" / "store.json"
HOST = os.environ.get("SHOPMATE_HOST", "0.0.0.0")
PORT = int(os.environ.get("SHOPMATE_PORT", "8080"))

NIM_BASE_URL = os.environ.get("NIM_BASE_URL", "").strip()
NIM_API_KEY = os.environ.get("NIM_API_KEY", "").strip()
NIM_MODEL = os.environ.get("NIM_MODEL", "nim-retail-assistant").strip()
SHOPMATE_AGENT_MAX_TURNS = int(os.environ.get("SHOPMATE_AGENT_MAX_TURNS", "6"))
SHOPMATE_DISABLE_OPENAI_AGENT_TRACING = (
    os.environ.get("SHOPMATE_DISABLE_OPENAI_AGENT_TRACING", "true").strip().lower() != "false"
)
SHOPMATE_USE_AGENT_TOOLS = os.environ.get("SHOPMATE_USE_AGENT_TOOLS", "false").strip().lower() == "true"
CUSTOM_TRACER = otel_trace.get_tracer("shopmate.custom") if otel_trace else None

SYSTEM_PROMPT = """You are ShopMate, a helpful assistant for a fictional athletic retail store.
Help shoppers choose products from the provided catalog. Be concise, ask a follow-up
question when needed, and avoid medical claims. If a shopper mentions pain or injury,
suggest comfort/stability considerations and recommend they consult a professional
for medical advice. Do not invent products, brands, policies, promotions, delivery
commitments, or order actions outside the catalog and prompt."""


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


CATALOG = load_json(CATALOG_PATH)
INVENTORY = load_json(INVENTORY_PATH)
POLICIES = load_json(POLICIES_PATH)
STORE = load_json(STORE_PATH)
STOPWORDS = {
    "about",
    "after",
    "also",
    "and",
    "are",
    "can",
    "for",
    "from",
    "good",
    "have",
    "happens",
    "how",
    "if",
    "into",
    "find",
    "fit",
    "me",
    "need",
    "options",
    "pickup",
    "policy",
    "return",
    "returns",
    "shoe",
    "shoes",
    "shipping",
    "size",
    "the",
    "them",
    "they",
    "this",
    "try",
    "under",
    "what",
    "when",
    "with",
    "wrong",
    "you",
}
FOOTWEAR_TERMS = {"boot", "boots", "cleat", "cleats", "footwear", "sandal", "sandals", "shoe", "shoes", "slide", "slides", "trainer", "trainers"}
PRICE_CEILING_RE = re.compile(r"(?:under|below|less than|up to|max(?:imum)?|budget of)\s*\$?\s*(\d+(?:\.\d+)?)", re.IGNORECASE)


def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return max(1, math.ceil(len(text) / 4))


def preview_text(text: str, limit: int = 500) -> str:
    normalized = " ".join(str(text).split())
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 3] + "..."


def set_span_error(span: Any, exc: Exception) -> None:
    if not span:
        return
    span.set_attribute("error.type", type(exc).__name__)
    span.set_attribute("error.message", preview_text(str(exc), 300))
    if Status and StatusCode:
        span.set_status(Status(StatusCode.ERROR, str(exc)))


def workflow_span_context(message: str, history: list[dict[str, str]], specialist_count: int) -> Any:
    if not CUSTOM_TRACER:
        return nullcontext(None)
    return CUSTOM_TRACER.start_as_current_span(
        "shopmate.workflow",
        attributes={
            "shopmate.workflow.name": "multi_agent_retail_assistant",
            "shopmate.model.system": "nvidia_nim",
            "shopmate.model.name": NIM_MODEL,
            "shopmate.coordinator.agent_name": "ShoppingAssistantAgent",
            "shopmate.request.preview": preview_text(message),
            "shopmate.history.user_messages": sum(1 for item in history if item.get("role") == "user"),
            "shopmate.specialist.count": specialist_count,
        },
    )


def agents_trace_context(workflow_id: str, message: str) -> Any:
    if not agent_trace:
        return nullcontext()
    trace_id = gen_trace_id() if gen_trace_id else None
    return agent_trace(
        "ShopMate multi-agent workflow",
        trace_id=trace_id,
        group_id=workflow_id,
        metadata={
            "service.name": "shopmate-ai",
            "deployment.environment": os.environ.get("OTEL_RESOURCE_ATTRIBUTES", ""),
            "gen_ai.request.model": NIM_MODEL,
            "shopmate.workflow.id": workflow_id,
            "shopmate.request.preview": preview_text(message),
        },
    )


def agent_step_span_context(agent_name: str, prompt: str) -> Any:
    if not CUSTOM_TRACER:
        return nullcontext(None)
    return CUSTOM_TRACER.start_as_current_span(
        f"shopmate.agent.{agent_name}",
        attributes={
            "shopmate.agent.name": agent_name,
            "shopmate.model.system": "nvidia_nim",
            "shopmate.model.name": NIM_MODEL,
            "shopmate.agent.prompt.preview": preview_text(prompt, 400),
        },
    )


def catalog_context(products: list[dict[str, Any]] | None = None) -> str:
    rows = []
    for item in products or CATALOG:
        rows.append(
            f"- {item['name']} ({item['category']}, {item['audience']}): "
            f"${item['price']:.2f}; stock {item['stock']}; colors {', '.join(item['colors'])}; "
            f"sizes {', '.join(item['sizes'])}; widths {', '.join(item['widths'])}; tags {', '.join(item['tags'])}; "
            f"{item['description']}"
        )
    return "\n".join(rows)


def catalog_names() -> str:
    return ", ".join(item["name"] for item in CATALOG)


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in re.findall(r"[a-zA-Z0-9]+(?:\.[0-9]+)?", text)]


def term_variants(term: str) -> set[str]:
    variants = {term}
    if len(term) > 4 and term.endswith("ing"):
        variants.add(term[:-3])
    if len(term) > 3 and term.endswith("ies"):
        variants.add(term[:-3] + "y")
    if len(term) > 3 and term.endswith("es"):
        variants.add(term[:-2])
    if len(term) > 3 and term.endswith("s"):
        variants.add(term[:-1])
    return variants


def searchable_product_text(product: dict[str, Any]) -> str:
    return " ".join(
        [
            product["name"],
            product["category"],
            product["audience"],
            product["description"],
            " ".join(product["tags"]),
            " ".join(product["colors"]),
            " ".join(product["widths"]),
        ]
    )


def policy_context() -> str:
    lines = []
    for policy in POLICIES.get("policies", []):
        details = "; ".join(policy.get("details", []))
        lines.append(f"- {policy['name']}: {policy['summary']} {details}".strip())
    limitations = POLICIES.get("limitations", [])
    if limitations:
        lines.append("Limitations: " + "; ".join(limitations))
    return "\n".join(lines)


def matching_policies(message: str) -> list[dict[str, Any]]:
    return matching_keyword_records(message, POLICIES.get("policies", []))


def policy_line(policy: dict[str, Any]) -> str:
    details = "; ".join(policy.get("details", []))
    return f"{policy['name']}: {policy['summary']} {details}".strip()


def matching_keyword_records(message: str, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    tokens = set(tokenize(message))
    token_forms = set().union(*(term_variants(token) for token in tokens)) if tokens else set()
    matches = []
    for record in records:
        keywords = set(record.get("keywords", []))
        keyword_forms = set().union(*(term_variants(keyword) for keyword in keywords)) if keywords else set()
        if token_forms & keyword_forms:
            matches.append(record)
    return matches


def matching_store_topics(message: str) -> list[dict[str, Any]]:
    return matching_keyword_records(message, STORE.get("topics", []))


def store_topic_line(topic: dict[str, Any]) -> str:
    details = "; ".join(topic.get("details", []))
    return f"{topic['name']}: {topic['summary']} {details}".strip()


def product_by_id(product_id: str) -> dict[str, Any] | None:
    for product in CATALOG:
        if product["id"] == product_id:
            return product
    return None


def inventory_by_product_id(product_id: str) -> dict[str, Any] | None:
    for item in INVENTORY.get("items", []):
        if item["product_id"] == product_id:
            return item
    return None


def location_by_id(location_id: str) -> dict[str, Any] | None:
    for location in INVENTORY.get("locations", []):
        if location["id"] == location_id:
            return location
    return None


def inventory_lines(products: list[dict[str, Any]]) -> list[str]:
    lines = []
    for product in products:
        item = inventory_by_product_id(product["id"])
        if not item:
            lines.append(f"- {product['name']}: no inventory record in inventory.json.")
            continue
        locations = []
        for location_id, quantity in item.get("location_quantities", {}).items():
            location = location_by_id(location_id)
            location_name = location["name"] if location else location_id
            locations.append(f"{location_name}: {quantity}")
        lines.append(f"- {product['name']}: " + "; ".join(locations))
    return lines


def extract_constraints(message: str) -> dict[str, Any]:
    tokens = set(tokenize(message))
    price_match = PRICE_CEILING_RE.search(message)
    return {
        "max_price": float(price_match.group(1)) if price_match else None,
        "wide": "wide" in tokens,
        "footwear": bool(tokens & FOOTWEAR_TERMS),
    }


def nim_base_url() -> str:
    return NIM_BASE_URL.rstrip("/")


def product_matches_constraints(product: dict[str, Any], constraints: dict[str, Any], *, strict_price: bool = True) -> bool:
    max_price = constraints.get("max_price")
    if strict_price and max_price is not None and product["price"] > max_price:
        return False
    if constraints.get("wide") and "Wide" not in product.get("widths", []):
        return False
    if constraints.get("footwear") and not product.get("widths"):
        return False
    return True


def product_score(product: dict[str, Any], query_terms: set[str]) -> int:
    product_terms = set(tokenize(searchable_product_text(product)))
    expanded_product_terms = set().union(*(term_variants(term) for term in product_terms))
    score = 0
    for term in query_terms:
        variants = term_variants(term)
        if variants & expanded_product_terms:
            score += 2
            continue
        if len(term) >= 4 and any(product_term.startswith(term[:4]) for product_term in expanded_product_terms):
            score += 1
    return score


def catalog_analysis(message: str, limit: int = 5) -> dict[str, Any]:
    constraints = extract_constraints(message)
    query_terms = {term for term in tokenize(message) if len(term) > 2 and term not in STOPWORDS}
    scored: list[tuple[int, dict[str, Any]]] = []
    for product in CATALOG:
        score = product_score(product, query_terms)
        if product_matches_constraints(product, constraints):
            score += 4
        elif product_matches_constraints(product, constraints, strict_price=False):
            score += 2
        if score:
            scored.append((score, product))
    scored.sort(key=lambda pair: (-pair[0], pair[1]["price"]))
    exact = [product for _, product in scored if product_matches_constraints(product, constraints)]
    alternatives = [
        product
        for _, product in scored
        if product not in exact and product_matches_constraints(product, constraints, strict_price=False)
    ]
    if not exact and not alternatives:
        alternatives = CATALOG[:limit]
    notes = []
    if constraints.get("max_price") is not None and not exact:
        notes.append(f"No exact catalog match satisfies the ${constraints['max_price']:.0f} price ceiling with the other request constraints.")
    if constraints.get("wide") and not exact:
        notes.append("No exact catalog match satisfies the requested wide-width constraint with the other request constraints.")
    if constraints.get("footwear") and not exact:
        notes.append("No exact footwear match satisfies all requested constraints; use alternatives only as tradeoffs.")
    return {
        "constraints": constraints,
        "exact_matches": exact[:limit],
        "alternatives": alternatives[:limit],
        "notes": notes,
    }


def catalog_matches(message: str, limit: int = 5) -> list[dict[str, Any]]:
    analysis = catalog_analysis(message, limit)
    matches = []
    for product in [*analysis["exact_matches"], *analysis["alternatives"]]:
        if product not in matches:
            matches.append(product)
        if len(matches) >= limit:
            break
    return matches


def product_evidence(product: dict[str, Any]) -> str:
    return (
        f"{product['name']} | category={product['category']} | price=${product['price']:.2f} | "
        f"stock={product['stock']} | widths={', '.join(product['widths']) or 'not applicable'} | "
        f"tags={', '.join(product['tags'])} | {product['description']}"
    )


def catalog_evidence(message: str) -> str:
    analysis = catalog_analysis(message)
    constraints = analysis["constraints"]
    lines = ["Catalog matching evidence:"]
    if constraints.get("max_price") is not None:
        lines.append(f"- Requested price ceiling: ${constraints['max_price']:.2f}")
    if constraints.get("wide"):
        lines.append("- Requested width: Wide")
    if constraints.get("footwear"):
        lines.append("- Request is for footwear.")
    if analysis["exact_matches"]:
        lines.append("- Best catalog matches:")
        lines.extend(f"  - {product_evidence(product)}" for product in analysis["exact_matches"])
    if analysis["alternatives"]:
        lines.append("- Alternatives / tradeoffs:")
        lines.extend(f"  - {product_evidence(product)}" for product in analysis["alternatives"])
    for note in analysis["notes"]:
        lines.append(f"- Constraint note: {note}")
    return "\n".join(lines)


def tool_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True)


def search_catalog_data(query: str) -> str:
    analysis = catalog_analysis(query)
    return tool_json(
        {
            "query": query,
            "constraints": analysis["constraints"],
            "best_matches": analysis["exact_matches"],
            "alternatives": analysis["alternatives"],
            "notes": analysis["notes"],
        }
    )


def lookup_inventory_data(query: str) -> str:
    products = catalog_matches(query, limit=5)
    inventory_items = []
    for product in products:
        item = inventory_by_product_id(product["id"]) or {"product_id": product["id"], "location_quantities": {}}
        locations = []
        for location_id, quantity in item.get("location_quantities", {}).items():
            location = location_by_id(location_id) or {"id": location_id, "name": location_id, "pickup_enabled": False}
            locations.append(
                {
                    "location_id": location["id"],
                    "location_name": location["name"],
                    "pickup_enabled": location.get("pickup_enabled", False),
                    "quantity": quantity,
                }
            )
        inventory_items.append(
            {
                "product_id": product["id"],
                "product_name": product["name"],
                "catalog_stock": product["stock"],
                "locations": locations,
            }
        )
    return tool_json(
        {
            "query": query,
            "inventory": inventory_items,
            "limitations": INVENTORY.get("limitations", []),
        }
    )


def lookup_store_policy_data(query: str) -> str:
    return tool_json(
        {
            "query": query,
            "policies": matching_policies(query),
            "limitations": POLICIES.get("limitations", []),
        }
    )


def lookup_store_info_data(query: str) -> str:
    return tool_json(
        {
            "query": query,
            "store_name": STORE.get("name"),
            "topics": matching_store_topics(query),
            "locations": INVENTORY.get("locations", []),
            "limitations": STORE.get("limitations", []),
        }
    )


if function_tool:

    @function_tool
    def search_catalog(query: str) -> str:
        """Search catalog.json for products that match the shopper query."""
        return search_catalog_data(query)

    @function_tool
    def lookup_inventory(query: str) -> str:
        """Read inventory.json for location quantities related to the shopper query."""
        return lookup_inventory_data(query)

    @function_tool
    def lookup_store_policy(query: str) -> str:
        """Read policies.json for return, exchange, and fit policy information."""
        return lookup_store_policy_data(query)

    @function_tool
    def lookup_store_info(query: str) -> str:
        """Read store.json for pickup, delivery, store hours, and demo limitations."""
        return lookup_store_info_data(query)

else:  # pragma: no cover - optional dependency fallback
    search_catalog = None
    lookup_inventory = None
    lookup_store_policy = None
    lookup_store_info = None


def format_product_recommendation(product: dict[str, Any]) -> str:
    widths = ", ".join(product["widths"]) if product["widths"] else "not applicable"
    return (
        f"- {product['name']} (${product['price']:.2f}, {product['category']}): "
        f"{product['description']} Stock: {product['stock']}. Widths: {widths}. "
        f"Tags: {', '.join(product['tags'])}."
    )


def compose_grounded_reply(message: str) -> str:
    analysis = catalog_analysis(message, limit=5)
    recommended = catalog_matches(message, limit=3)
    policies = matching_policies(message)
    store_topics = matching_store_topics(message)
    lines = []
    if recommended:
        lines.append("Best matches from the demo catalog:")
        lines.extend(format_product_recommendation(product) for product in recommended)
    else:
        lines.append("I do not see a matching product in the demo catalog.")

    if analysis["notes"]:
        lines.append("")
        lines.append("Catalog tradeoffs:")
        lines.extend(f"- {note}" for note in analysis["notes"])

    if recommended:
        lines.append("")
        lines.append("Inventory examples:")
        lines.extend(inventory_lines(recommended))

    if policies:
        lines.append("")
        lines.append("Policy notes:")
        lines.extend(f"- {policy_line(policy)}" for policy in policies)

    if store_topics:
        lines.append("")
        lines.append("Store notes:")
        lines.extend(f"- {store_topic_line(topic)}" for topic in store_topics)

    store_limitations = STORE.get("limitations", [])
    inventory_limitations = INVENTORY.get("limitations", [])
    if store_topics and (store_limitations or inventory_limitations):
        lines.append("")
        lines.append("Demo data limits:")
        lines.extend(f"- {item}" for item in [*inventory_limitations, *store_limitations][:3])

    lines.append("")
    lines.append("Practical next step: choose size, width, and color, then compare the top match against the listed tradeoffs.")
    return "\n".join(lines)


def agents_available() -> bool:
    return all([AsyncOpenAI, Agent, ModelSettings, OpenAIChatCompletionsModel, Runner, function_tool])


def build_model() -> Any:
    if not agents_available():
        raise RuntimeError("OpenAI Agents SDK dependencies are not installed")
    if not nim_base_url():
        raise RuntimeError("NIM_BASE_URL is not configured")
    if set_tracing_disabled:
        set_tracing_disabled(disabled=SHOPMATE_DISABLE_OPENAI_AGENT_TRACING)
    client = AsyncOpenAI(api_key=NIM_API_KEY or "nim-local-key", base_url=nim_base_url())
    return OpenAIChatCompletionsModel(model=NIM_MODEL, openai_client=client)


def build_agents() -> Any:
    model = build_model()
    model_settings = ModelSettings(temperature=0.2, max_tokens=350)
    tool_guardrail = "\n\nUse the provided tools for catalog, inventory, policy, and store facts. Do not answer from memory."
    base_instructions = SYSTEM_PROMPT + tool_guardrail
    if not SHOPMATE_USE_AGENT_TOOLS:
        return Agent(
            name="ShoppingAssistantAgent",
            instructions=(
                base_instructions
                + "\n\nCall search_catalog before recommending products. Include product names, prices, and one practical reason for each recommendation."
            ),
            model=model,
            tools=[search_catalog],
        )

    catalog_agent = Agent(
        name="CatalogAgent",
        handoff_description="Finds catalog matches and compares products.",
        instructions=(
            base_instructions
            + "\n\nYou are a retail catalog specialist. Call search_catalog with the shopper request before recommending or comparing products. "
            + "Only use products returned by the tool."
        ),
        model=model,
        model_settings=model_settings,
        tools=[search_catalog],
    )
    inventory_agent = Agent(
        name="InventoryAgent",
        handoff_description="Checks product availability and delivery estimates.",
        instructions=(
            base_instructions
            + "\n\nYou are an inventory specialist. Call lookup_inventory for quantities and lookup_store_info for pickup or delivery context. "
            + "Only use inventory and store facts returned by the tools."
        ),
        model=model,
        model_settings=model_settings,
        tools=[lookup_inventory, lookup_store_info],
    )
    policy_agent = Agent(
        name="PolicyAgent",
        handoff_description="Answers shipping, returns, fit, and promotion policy questions.",
        instructions=(
            SYSTEM_PROMPT
            + tool_guardrail
            + "\n\nYou are a retail policy specialist. Call lookup_store_policy for return and fit policy, and lookup_store_info for pickup or delivery questions. "
            + "Only use facts returned by the tools."
        ),
        model=model,
        model_settings=model_settings,
        tools=[lookup_store_policy, lookup_store_info],
    )
    checkout_agent = Agent(
        name="CheckoutAgent",
        handoff_description="Builds cart previews, promotion summaries, and mock order previews.",
        instructions=(
            base_instructions
            + "\n\nYou are a checkout specialist. Call search_catalog and lookup_inventory before summarizing a possible demo cart. "
            + "Do not claim that an order was created, payment was collected, or a checkout total was calculated."
        ),
        model=model,
        model_settings=model_settings,
        tools=[search_catalog, lookup_inventory],
    )
    cost_agent = Agent(
        name="CostAgent",
        handoff_description="Summarizes estimated token usage and chargeback context for the lab.",
        instructions=(
            "You are a lab cost specialist for an AI observability workshop. "
            "Describe why a request is likely cheap, moderate, or expensive in terms of agent work and LLM reasoning. "
            "Do not invent exact token counts, dollar costs, or chargeback accounts."
        ),
        model=model,
        model_settings=model_settings,
    )
    shopping_agent = Agent(
        name="ShoppingAssistantAgent",
        instructions=base_instructions
        + "\n\nCoordinate specialist findings from CatalogAgent, InventoryAgent, PolicyAgent, CheckoutAgent, and CostAgent. "
        + "Call tools when you need product, inventory, policy, or store facts. Discard unsupported specialist claims.",
        model=model,
        model_settings=model_settings,
        tools=[search_catalog, lookup_inventory, lookup_store_policy, lookup_store_info],
    )
    return {
        "shopping": shopping_agent,
        "catalog": catalog_agent,
        "inventory": inventory_agent,
        "policy": policy_agent,
        "checkout": checkout_agent,
        "cost": cost_agent,
    }


def format_history(history: list[dict[str, str]]) -> str:
    if not history:
        return ""
    lines = ["Prior shopper messages for context only. The current request overrides prior topics unless it explicitly refers back:"]
    for item in history[-8:]:
        role = item.get("role", "unknown")
        if role != "user":
            continue
        content = item.get("content", "")
        lines.append(f"user: {content}")
    if len(lines) == 1:
        return ""
    return "\n".join(lines)


def format_specialist_outputs(outputs: dict[str, str]) -> str:
    lines = ["Specialist findings:"]
    for name, output in outputs.items():
        lines.append(f"\n[{name}]\n{output.strip()}")
    return "\n".join(lines)


def record_coordinator_response(prompt: str, reply: str) -> None:
    with agent_step_span_context("ShoppingAssistantAgent", prompt) as span:
        if span:
            span.set_attribute("shopmate.agent.output.preview", preview_text(reply))
            span.set_attribute("shopmate.agent.output.length", len(reply))
            span.set_attribute("shopmate.agent.role", "final_coordinator")


async def run_agent_step(agent_name: str, agent: Any, prompt: str) -> str:
    with agent_step_span_context(agent_name, prompt) as span:
        try:
            result = await Runner.run(agent, prompt, max_turns=SHOPMATE_AGENT_MAX_TURNS)
            output = str(result.final_output)
            if span:
                span.set_attribute("shopmate.agent.output.preview", preview_text(output))
                span.set_attribute("shopmate.agent.output.length", len(output))
            return output
        except Exception as exc:  # pragma: no cover - keeps the demo response path reliable
            set_span_error(span, exc)
            return f"{type(exc).__name__}: {exc}"


async def call_agents_sdk(message: str, history: list[dict[str, str]]) -> str:
    agent_input = "\n\n".join(
        part
        for part in [
            format_history(history),
            f"Current shopper request: {message}",
            "Use the current shopper request as the task. Do not carry over products, constraints, or policy topics from prior messages unless the current request explicitly refers to them.",
            "Use tools for facts: search_catalog, lookup_inventory, lookup_store_policy, and lookup_store_info.",
        ]
        if part
    )
    agents = build_agents()
    specialist_prompts = [
        (
            "CatalogAgent",
            "catalog",
            f"{agent_input}\n\nCall search_catalog with the current shopper request. Then summarize the matching products and tradeoffs returned by the tool.",
        ),
        (
            "InventoryAgent",
            "inventory",
            f"{agent_input}\n\nCall lookup_inventory with the current shopper request. If the shopper asks pickup or delivery questions, also call lookup_store_info.",
        ),
        (
            "PolicyAgent",
            "policy",
            f"{agent_input}\n\nCall lookup_store_policy for return or fit policy questions. Call lookup_store_info for pickup, delivery, or store questions.",
        ),
        (
            "CheckoutAgent",
            "checkout",
            f"{agent_input}\n\nCall search_catalog and lookup_inventory. Summarize a possible cart from returned data and any checkout caveats. Do not create a real order.",
        ),
        (
            "CostAgent",
            "cost",
            f"{agent_input}\n\nFor workshop observability, explain whether this prompt should create normal, moderate, or high agent/LLM work and why.",
        ),
    ]
    workflow_id = f"shopmate-{int(time.time() * 1000)}"
    specialist_count = len(specialist_prompts) + 1 if SHOPMATE_USE_AGENT_TOOLS else 1

    with workflow_span_context(message, history, specialist_count) as workflow_span:
        try:
            with agents_trace_context(workflow_id, message):
                if not SHOPMATE_USE_AGENT_TOOLS:
                    await run_agent_step("ShoppingAssistantAgent", agents, agent_input)
                    reply = compose_grounded_reply(message)
                    record_coordinator_response(agent_input, reply)
                    if workflow_span:
                        workflow_span.set_attribute("shopmate.response.preview", preview_text(reply))
                        workflow_span.set_attribute("shopmate.response.tokens.estimated", estimate_tokens(reply))
                    return reply

                specialist_outputs: dict[str, str] = {}
                for agent_name, key, prompt in specialist_prompts:
                    specialist_outputs[agent_name] = await run_agent_step(agent_name, agents[key], prompt)

                grounded_reply = compose_grounded_reply(message)
                coordinator_prompt = "\n\n".join(
                    [
                        agent_input,
                        format_specialist_outputs(specialist_outputs),
                        "Write the final shopper-facing answer. Use only supported catalog, inventory, policy, and store facts. "
                        "If a specialist finding conflicts with the grounded reference answer, prefer the grounded reference.",
                        f"Grounded reference answer:\n{grounded_reply}",
                    ]
                )
                record_coordinator_response(coordinator_prompt, grounded_reply)

            reply = grounded_reply
            if workflow_span:
                workflow_span.set_attribute("shopmate.response.preview", preview_text(reply))
                workflow_span.set_attribute("shopmate.response.tokens.estimated", estimate_tokens(reply))
                workflow_span.set_attribute("shopmate.specialist.names", ",".join([*specialist_outputs.keys(), "ShoppingAssistantAgent"]))
                workflow_span.set_attribute(
                    "shopmate.specialist.output_tokens.estimated",
                    sum(estimate_tokens(output) for output in specialist_outputs.values()),
                )
            return reply
        except Exception as exc:
            set_span_error(workflow_span, exc)
            raise


def call_nim(message: str, history: list[dict[str, str]]) -> tuple[str, dict[str, int], bool, str | None]:
    if not nim_base_url():
        raise RuntimeError("NIM_BASE_URL is not configured")
    if not agents_available():
        raise RuntimeError("OpenAI Agents SDK dependencies are not installed")
    reply = asyncio.run(call_agents_sdk(message, history))
    return reply, {
        "prompt_tokens": estimate_tokens(message),
        "completion_tokens": estimate_tokens(reply),
        "total_tokens": estimate_tokens(message) + estimate_tokens(reply),
    }, True, None


class ShopMateHandler(SimpleHTTPRequestHandler):
    server_version = "ShopMateSports/0.1"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def log_message(self, format: str, *args: Any) -> None:
        print(f"{self.address_string()} - {format % args}")

    def send_json(self, payload: Any, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status.value)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        return json.loads(raw.decode("utf-8"))

    def do_GET(self) -> None:
        if self.path == "/api/products":
            self.send_json({"products": CATALOG})
            return
        if self.path == "/healthz":
            self.send_json({"ok": True, "nim_configured": bool(nim_base_url()), "agents_available": agents_available()})
            return
        super().do_GET()

    def do_POST(self) -> None:
        try:
            payload = self.read_json()
            if self.path == "/api/chat":
                started = time.perf_counter()
                message = str(payload.get("message", "")).strip()
                if not message:
                    self.send_json({"error": "message is required"}, HTTPStatus.BAD_REQUEST)
                    return
                history = payload.get("history") or []
                try:
                    reply, usage, used_nim, error = call_nim(message, history)
                except Exception as exc:
                    traceback.print_exc()
                    latency_ms = round((time.perf_counter() - started) * 1000)
                    self.send_json(
                        {
                            "error": f"AgentsSDKError {type(exc).__name__}: {exc}",
                            "latency_ms": latency_ms,
                            "nim_enabled": False,
                        },
                        HTTPStatus.BAD_GATEWAY,
                    )
                    return
                latency_ms = round((time.perf_counter() - started) * 1000)
                self.send_json(
                    {
                        "reply": reply,
                        "usage": usage,
                        "latency_ms": latency_ms,
                        "nim_enabled": used_nim,
                        "nim_error": error,
                        "recommended_products": catalog_matches(message, limit=3),
                    }
                )
                return

            self.send_json({"error": "not found"}, HTTPStatus.NOT_FOUND)
        except Exception as exc:  # pragma: no cover - defensive server boundary
            traceback.print_exc()
            self.send_json({"error": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR)


def main() -> None:
    display_host = "127.0.0.1" if HOST == "0.0.0.0" else HOST
    print(f"ShopMate Sports running at http://{display_host}:{PORT}/")
    print(f"NIM configured: {bool(nim_base_url())}")
    print(f"OpenAI Agents SDK available: {agents_available()}")
    ThreadingHTTPServer((HOST, PORT), ShopMateHandler).serve_forever()


if __name__ == "__main__":
    main()
