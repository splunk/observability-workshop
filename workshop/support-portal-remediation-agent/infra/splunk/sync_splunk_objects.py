#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from urllib.error import HTTPError
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
SPECS_DIR = Path(__file__).resolve().parent / "specs"
STATE_PATH = Path(__file__).resolve().parent / ".object-ids.json"

DEFAULT_CONTEXT = {
    "deployment_environment": os.getenv("DEPLOYMENT_ENVIRONMENT", "demo"),
    "instance": os.getenv("INSTANCE", "student-001"),
    "orchestrator_webhook_url": os.getenv("ORCHESTRATOR_PUBLIC_WEBHOOK_URL", ""),
    "filesystem_utilization_threshold": os.getenv("FILESYSTEM_UTILIZATION_THRESHOLD", "85"),
    "cache_mountpoint": os.getenv("SPLUNK_CACHE_MOUNTPOINT", "/var/cache/claims-knowledge"),
    "evidence_metric_source": os.getenv("SPLUNK_EVIDENCE_METRIC_SOURCE", "claims-knowledge-evidence"),
    "cache_utilization_metric": os.getenv(
        "SPLUNK_CACHE_UTILIZATION_METRIC",
        os.getenv("CLAIMS_KNOWLEDGE_CACHE_UTILIZATION_METRIC", "claims_knowledge.cache.utilization"),
    ),
    "claim_status_latency_metric": os.getenv(
        "SPLUNK_CLAIM_STATUS_LATENCY_METRIC",
        os.getenv("CLAIMS_KNOWLEDGE_CLAIM_STATUS_LATENCY_METRIC", "claims_knowledge.claim_status.latency_ms"),
    ),
    "apm_latency_threshold_ns": os.getenv("APM_LATENCY_THRESHOLD_NS", "1800000000"),
    "apm_latency_threshold_ms": str(int(os.getenv("APM_LATENCY_THRESHOLD_NS", "1800000000")) // 1000000),
    "apm_error_threshold": os.getenv("APM_ERROR_THRESHOLD", "0.05"),
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def save_json(path: Path, value: Any) -> None:
    path.write_text(f"{json.dumps(value, indent=2, sort_keys=True)}\n")


def render_template(value: Any, context: dict[str, str]) -> Any:
    if isinstance(value, str):
        rendered = value
        for key, replacement in context.items():
            rendered = rendered.replace(f"{{{{{key}}}}}", str(replacement))
        return rendered
    if isinstance(value, list):
        return [render_template(item, context) for item in value]
    if isinstance(value, dict):
        return {key: render_template(item, context) for key, item in value.items()}
    return value


def load_specs(context: dict[str, str]) -> dict[str, Any]:
    return {
        "dashboard_group": render_template(load_json(SPECS_DIR / "dashboard-group.json"), context),
        "dashboards": render_template(load_json(SPECS_DIR / "dashboards.json"), context),
        "detectors": render_template(load_json(SPECS_DIR / "detectors.json"), context),
    }


def build_dashboard_group_payload(spec: dict[str, Any]) -> dict[str, Any]:
    return {"name": spec["name"]}


def build_dashboard_payload(spec: dict[str, Any], group_name: str) -> dict[str, Any]:
    charts = []
    for chart in spec["charts"]:
        grid = chart["grid"]
        charts.append(
            {
                "name": chart["name"],
                "chartType": chart["type"],
                "programText": chart["programText"],
                "width": grid["width"],
                "height": grid["height"],
                "row": grid["row"],
                "column": grid["column"],
            }
        )

    return {
        "key": spec["key"],
        "name": spec["name"],
        "dashboardGroupName": group_name,
        "timeRange": spec["timeRange"],
        "charts": charts,
    }


def build_detector_payload(spec: dict[str, Any]) -> dict[str, Any]:
    rule = {
        "detectLabel": spec["rule"]["detectLabel"],
        "severity": spec["rule"]["severity"],
        "description": spec["rule"]["description"],
    }
    runbook_url = spec["rule"].get("runbookUrlTemplate")
    if runbook_url:
        rule["runbookUrl"] = runbook_url

    return {
        "key": spec["key"],
        "name": spec["name"],
        "programText": spec["programText"],
        "rule": rule,
    }


def build_payloads(context: dict[str, str]) -> dict[str, Any]:
    specs = load_specs(context)
    group_payload = build_dashboard_group_payload(specs["dashboard_group"])
    return {
        "dashboard_group": group_payload,
        "dashboards": [
            build_dashboard_payload(spec, group_payload["name"]) for spec in specs["dashboards"]
        ],
        "detectors": [build_detector_payload(spec) for spec in specs["detectors"]],
    }


def load_state(path: Path = STATE_PATH) -> dict[str, Any]:
    if not path.exists():
        return {"dashboard_group": {}, "dashboards": {}, "detectors": {}}
    return json.loads(path.read_text())


def save_state(state: dict[str, Any], path: Path = STATE_PATH) -> None:
    save_json(path, state)


def request_json(
    base_url: str,
    token: str,
    method: str,
    path: str,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}{path}",
        method=method,
        headers={
            "content-type": "application/json",
            "x-sf-token": token,
        },
        data=None if payload is None else json.dumps(payload).encode("utf-8"),
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")
            return json.loads(body) if body else {}
    except HTTPError as error:
        body = error.read().decode("utf-8")
        details = body or error.reason
        raise RuntimeError(f"{method} {path} failed with {error.code}: {details}") from error


def upsert_object(
    *,
    base_url: str,
    token: str,
    collection_path: str,
    state_bucket: dict[str, dict[str, Any]],
    key: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    existing = state_bucket.get(key, {})
    object_id = existing.get("id")
    if object_id:
        result = request_json(base_url, token, "PUT", f"{collection_path}/{object_id}", payload)
    else:
        result = request_json(base_url, token, "POST", collection_path, payload)

    resolved_id = result.get("id", object_id)
    state_bucket[key] = {
        "id": resolved_id,
        "name": result.get("name", payload.get("name")),
        "key": key,
        "url": result.get("url"),
    }
    return result


def apply_payloads(
    payloads: dict[str, Any],
    base_url: str,
    token: str,
    state: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    mutable_state = state or load_state()
    results = {
        "dashboard_group": {},
        "dashboards": [],
        "detectors": [],
    }
    results["dashboard_group"] = upsert_object(
        base_url=base_url,
        token=token,
        collection_path="/v2/dashboardgroup",
        state_bucket=mutable_state["dashboard_group"],
        key="default",
        payload=payloads["dashboard_group"],
    )

    for dashboard in payloads["dashboards"]:
        results["dashboards"].append(
            upsert_object(
                base_url=base_url,
                token=token,
                collection_path="/v2/dashboard",
                state_bucket=mutable_state["dashboards"],
                key=dashboard["key"],
                payload=dashboard,
            )
        )
    for detector in payloads["detectors"]:
        results["detectors"].append(
            upsert_object(
                base_url=base_url,
                token=token,
                collection_path="/v2/detector",
                state_bucket=mutable_state["detectors"],
                key=detector["key"],
                payload=detector,
            )
        )
    return results, mutable_state


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render or apply Splunk dashboard and detector specs.")
    parser.add_argument("--apply", action="store_true", help="POST rendered payloads to the Splunk API.")
    parser.add_argument(
        "--base-url",
        default=os.getenv("SPLUNK_API_BASE_URL", "https://api.us1.signalfx.com"),
        help="Splunk Observability API base URL.",
    )
    parser.add_argument(
        "--token",
        default=os.getenv("SPLUNK_ACCESS_TOKEN", ""),
        help="Splunk access token. Required with --apply.",
    )
    parser.add_argument(
        "--output",
        choices=["json", "pretty"],
        default="pretty",
        help="Output format for rendered payloads or API responses.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payloads = build_payloads(DEFAULT_CONTEXT)

    if args.apply:
        if not args.token:
            print("SPLUNK_ACCESS_TOKEN is required with --apply.", file=sys.stderr)
            return 1
        data, state = apply_payloads(payloads, args.base_url, args.token)
        save_state(state)
    else:
        data = payloads

    if args.output == "json":
        print(json.dumps(data))
    else:
        print(json.dumps(data, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
