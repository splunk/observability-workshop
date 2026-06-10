#!/usr/bin/env python3
"""Run Galileo experiments that mirror the remediation app.

These experiments are deterministic harnesses around the app's actual concepts:
Splunk MCP evidence handoff, policy gating, agent proposal, approval, execution,
and verification. They do not invent runbooks or unrelated provider scenarios.
"""

from __future__ import annotations

import argparse
import json
import os
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from galileo import log
from galileo.experiments import run_experiment
from galileo.schema.metrics import LocalMetricConfig
from galileo_core.schemas.logging.step import StepType


DEFAULT_PROJECT = "ciscolive26"
DEFAULT_GROUP = "CL26 Galileo App Experiments"
CACHE_METRIC = "claims_knowledge.cache.utilization"
LATENCY_METRIC = "claims_knowledge.claim_status.latency_ms"
CACHE_THRESHOLD = 85
LATENCY_THRESHOLD_MS = 1800
BOUNDED_ACTION = "clean_claims_knowledge_cache"


@dataclass(frozen=True)
class ExperimentSuite:
    key: str
    display_name: str
    name_prefix: str
    story: str
    dataset: Callable[[], list[dict[str, Any]]]
    runner: Callable[[dict[str, Any]], str]
    metrics: Callable[[], list[LocalMetricConfig[float]]]


def load_env_file(path: Path) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def configure_environment() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    load_env_file(repo_root / ".env")
    os.environ.setdefault("GALILEO_PROJECT", DEFAULT_PROJECT)

    if os.getenv("GALILEO_API_KEY") or not os.getenv("GALILEO_API_KEY_FILE"):
        return

    key_file = Path(os.environ["GALILEO_API_KEY_FILE"]).expanduser()
    if not key_file.is_absolute():
        key_file = repo_root / key_file
    os.environ["GALILEO_API_KEY"] = key_file.read_text(encoding="utf-8").strip()


def dataset_records(suite: str, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "input": row,
            "ground_truth": row["expected"],
            "metadata": {
                "scenario_id": row["scenario_id"],
                "suite": suite,
                "detector": "Claims Knowledge Cache Volume Pressure",
                "service": "claims-knowledge",
            },
        }
        for row in rows
    ]


def mcp_evidence_dataset() -> list[dict[str, Any]]:
    rows = [
        {
            "scenario_id": "mcp-complete-cache-pressure",
            "incident": "Splunk detector fires for AI Claim Status latency and claims-knowledge cache pressure.",
            "mcp_tools": [
                {"tool": "tools/list", "status": "ok"},
                {"tool": "search_alerts_or_incidents", "status": "ok", "summary": "Detector alert found."},
                {"tool": "get_apm_service_latency", "status": "ok", "latency_ms": 2350},
                {"tool": "get_apm_service_errors_and_requests", "status": "ok", "error_rate": 0.01},
                {"tool": "get_apm_exemplar_traces", "status": "ok", "trace_ids": ["4bf92f3577b34da6a3ce929d0e0e4736"]},
                {"tool": "execute_signalflow_program", "purpose": "cache", "status": "ok", "cache_utilization": 92},
                {"tool": "execute_signalflow_program", "purpose": "latency", "status": "ok", "latency_ms": 2350},
            ],
            "operator_note": "",
            "expected": {
                "confidence_band": "high",
                "policy_mode": "approval_required",
                "proposed_action": BOUNDED_ACTION,
                "warning_count": 0,
            },
        },
        {
            "scenario_id": "mcp-cache-signalflow-empty",
            "incident": "APM latency is elevated, but the cache SignalFlow query returns no pressure.",
            "mcp_tools": [
                {"tool": "tools/list", "status": "ok"},
                {"tool": "get_apm_service_latency", "status": "ok", "latency_ms": 2400},
                {"tool": "execute_signalflow_program", "purpose": "cache", "status": "empty", "cache_utilization": None},
                {"tool": "execute_signalflow_program", "purpose": "latency", "status": "ok", "latency_ms": 2400},
            ],
            "operator_note": "",
            "expected": {
                "confidence_band": "medium",
                "policy_mode": "approval_required",
                "proposed_action": BOUNDED_ACTION,
                "warning_count": 1,
            },
        },
        {
            "scenario_id": "mcp-latency-tool-timeout",
            "incident": "Cache pressure is confirmed, but the APM latency tool times out.",
            "mcp_tools": [
                {"tool": "tools/list", "status": "ok"},
                {"tool": "get_apm_service_latency", "status": "failed", "error": "query timeout"},
                {"tool": "execute_signalflow_program", "purpose": "cache", "status": "ok", "cache_utilization": 94},
                {"tool": "execute_signalflow_program", "purpose": "latency", "status": "failed", "error": "query timeout"},
            ],
            "operator_note": "",
            "expected": {
                "confidence_band": "medium",
                "policy_mode": "approval_required",
                "proposed_action": BOUNDED_ACTION,
                "warning_count": 2,
            },
        },
        {
            "scenario_id": "mcp-tools-list-failed",
            "incident": "The Splunk MCP tools/list call fails before evidence can be gathered.",
            "mcp_tools": [
                {"tool": "tools/list", "status": "failed", "error": "HTTP 503"},
            ],
            "operator_note": "",
            "expected": {
                "confidence_band": "low",
                "policy_mode": "recommend_only",
                "proposed_action": BOUNDED_ACTION,
                "warning_count": 1,
            },
        },
        {
            "scenario_id": "mcp-no-pressure-confirmed",
            "incident": "MCP tools respond, but neither cache pressure nor latency crosses threshold.",
            "mcp_tools": [
                {"tool": "tools/list", "status": "ok"},
                {"tool": "get_apm_service_latency", "status": "ok", "latency_ms": 410},
                {"tool": "execute_signalflow_program", "purpose": "cache", "status": "ok", "cache_utilization": 41},
                {"tool": "execute_signalflow_program", "purpose": "latency", "status": "ok", "latency_ms": 410},
            ],
            "operator_note": "",
            "expected": {
                "confidence_band": "low",
                "policy_mode": "recommend_only",
                "proposed_action": BOUNDED_ACTION,
                "warning_count": 2,
            },
        },
        {
            "scenario_id": "mcp-exemplar-trace-attached",
            "incident": "MCP confirms cache pressure and attaches APM exemplar trace evidence.",
            "mcp_tools": [
                {"tool": "tools/list", "status": "ok"},
                {"tool": "search_alerts_or_incidents", "status": "ok", "summary": "Detector scoped to claims-knowledge."},
                {"tool": "get_apm_service_latency", "status": "ok", "latency_ms": 2600},
                {"tool": "get_apm_exemplar_traces", "status": "ok", "trace_ids": ["8f3c0cfd5f314f029bd96247b0f982d1"]},
                {"tool": "execute_signalflow_program", "purpose": "cache", "status": "ok", "cache_utilization": 96},
                {"tool": "execute_signalflow_program", "purpose": "latency", "status": "ok", "latency_ms": 2600},
            ],
            "operator_note": "",
            "expected": {
                "confidence_band": "high",
                "policy_mode": "approval_required",
                "proposed_action": BOUNDED_ACTION,
                "warning_count": 0,
            },
        },
    ]
    return dataset_records("mcp", rows)


def remediation_tools_dataset() -> list[dict[str, Any]]:
    rows = [
        {
            "scenario_id": "approval-required-not-clicked",
            "incident": "High-confidence MCP evidence exists, but the presenter has not clicked Approve.",
            "policy_mode": "approval_required",
            "operator_approved": False,
            "execute_result": None,
            "verify_result": None,
            "expected": {
                "approval_allowed": True,
                "execution_status": "not_started",
                "verification_status": "not_started",
                "incident_status": "proposed",
            },
        },
        {
            "scenario_id": "clean-cache-executes-and-validates",
            "incident": "The operator approves clean_claims_knowledge_cache and validation succeeds.",
            "policy_mode": "approval_required",
            "operator_approved": True,
            "execute_result": {"status": "executed", "scenario_state": "healthy"},
            "verify_result": {"status": "validated", "scenario_state": "healthy", "measured_latency_ms": 125},
            "expected": {
                "approval_allowed": True,
                "execution_status": "executed",
                "verification_status": "validated",
                "incident_status": "validated",
            },
        },
        {
            "scenario_id": "remediation-agent-execute-fails",
            "incident": "Approval succeeds, but POST /agent/execute returns a failed action result.",
            "policy_mode": "approval_required",
            "operator_approved": True,
            "execute_result": {"status": "failed", "scenario_state": "cache-disk-pressure"},
            "verify_result": None,
            "expected": {
                "approval_allowed": True,
                "execution_status": "failed",
                "verification_status": "skipped",
                "incident_status": "open",
            },
        },
        {
            "scenario_id": "verification-sees-scenario-still-active",
            "incident": "Execution returns executed, but scenario controller still reports cache-disk-pressure.",
            "policy_mode": "approval_required",
            "operator_approved": True,
            "execute_result": {"status": "executed", "scenario_state": "cache-disk-pressure"},
            "verify_result": {"status": "failed", "scenario_state": "cache-disk-pressure"},
            "expected": {
                "approval_allowed": True,
                "execution_status": "executed",
                "verification_status": "failed",
                "incident_status": "approved",
            },
        },
        {
            "scenario_id": "recommend-only-blocks-approval",
            "incident": "Low-confidence MCP evidence produces recommend_only policy, so approval endpoint must not execute.",
            "policy_mode": "recommend_only",
            "operator_approved": True,
            "execute_result": None,
            "verify_result": None,
            "expected": {
                "approval_allowed": False,
                "execution_status": "blocked_by_policy",
                "verification_status": "not_started",
                "incident_status": "proposed",
            },
        },
    ]
    return dataset_records("tools", rows)


def tool_records(case: dict[str, Any], tool_name: str, purpose: str | None = None) -> list[dict[str, Any]]:
    return [
        tool
        for tool in case.get("mcp_tools", [])
        if tool.get("tool") == tool_name and (purpose is None or tool.get("purpose") == purpose)
    ]


@log(span_type="tool", name="splunk_mcp.tools_list")
def splunk_mcp_tools_list(case: dict[str, Any]) -> dict[str, Any]:
    record = (tool_records(case, "tools/list") or [{"status": "ok"}])[0]
    if record.get("status") == "failed":
        return {"available": False, "warnings": [f"Splunk MCP tools/list failed: {record.get('error', 'unknown error')}."]}
    planned_tools = [
        "search_alerts_or_incidents",
        "get_apm_service_latency",
        "get_apm_service_errors_and_requests",
        "get_apm_exemplar_traces",
        "execute_signalflow_program",
    ]
    return {"available": True, "planned_tools": planned_tools, "warnings": []}


@log(span_type="tool", name="splunk_mcp.search_alerts_or_incidents")
def splunk_mcp_search_alerts(case: dict[str, Any]) -> dict[str, Any]:
    records = tool_records(case, "search_alerts_or_incidents")
    return records[0] if records else {"status": "not_requested"}


@log(span_type="tool", name="splunk_mcp.get_apm_service_latency")
def splunk_mcp_get_apm_service_latency(case: dict[str, Any]) -> dict[str, Any]:
    records = tool_records(case, "get_apm_service_latency")
    return records[0] if records else {"status": "not_returned"}


@log(span_type="tool", name="splunk_mcp.get_apm_exemplar_traces")
def splunk_mcp_get_apm_exemplar_traces(case: dict[str, Any]) -> dict[str, Any]:
    records = tool_records(case, "get_apm_exemplar_traces")
    return records[0] if records else {"status": "not_returned", "trace_ids": []}


@log(span_type="tool", name="splunk_mcp.execute_signalflow_program.cache")
def splunk_mcp_execute_signalflow_cache(case: dict[str, Any]) -> dict[str, Any]:
    records = tool_records(case, "execute_signalflow_program", "cache")
    return records[0] if records else {"status": "not_returned", "cache_utilization": None}


@log(span_type="tool", name="splunk_mcp.execute_signalflow_program.latency")
def splunk_mcp_execute_signalflow_latency(case: dict[str, Any]) -> dict[str, Any]:
    records = tool_records(case, "execute_signalflow_program", "latency")
    return records[0] if records else {"status": "not_returned", "latency_ms": None}


@log(span_type="agent", name="remediation.build_evidence_bundle")
def build_evidence_bundle_from_mcp(
    case: dict[str, Any],
    tools_list: dict[str, Any],
    latency_tool: dict[str, Any],
    trace_tool: dict[str, Any],
    cache_signalflow: dict[str, Any],
    latency_signalflow: dict[str, Any],
) -> dict[str, Any]:
    warnings = list(tools_list.get("warnings", []))
    if not tools_list.get("available"):
        return {
            "source": "splunk_mcp",
            "enrichment_applied": False,
            "sources": [],
            "warnings": warnings,
            "confidence_band": "low",
            "likely_cause": "Splunk MCP did not return live evidence; keep remediation recommendation-only until signals are verified.",
            "candidate_actions": [BOUNDED_ACTION],
            "trace_ids": [],
        }

    if latency_tool.get("status") == "failed":
        warnings.append(f"Splunk MCP tool get_apm_service_latency failed: {latency_tool.get('error', 'unknown error')}.")
    if latency_signalflow.get("status") == "failed":
        warnings.append(f"Splunk MCP tool execute_signalflow_program failed: {latency_signalflow.get('error', 'unknown error')}.")

    cache_utilization = cache_signalflow.get("cache_utilization")
    latency_ms = latency_tool.get("latency_ms") or latency_signalflow.get("latency_ms")
    filesystem_queried = cache_signalflow.get("status") in {"ok", "empty"}
    filesystem_confirmed = isinstance(cache_utilization, (int, float)) and cache_utilization >= CACHE_THRESHOLD
    latency_elevated = isinstance(latency_ms, (int, float)) and latency_ms >= LATENCY_THRESHOLD_MS

    if filesystem_queried and not filesystem_confirmed:
        warnings.append(f"Splunk MCP queried {CACHE_METRIC} but did not confirm cache utilization above {CACHE_THRESHOLD}.")
    if latency_tool.get("status") == "ok" and not latency_elevated:
        warnings.append(f"Splunk MCP queried {LATENCY_METRIC}/APM latency but did not confirm latency above {LATENCY_THRESHOLD_MS} ms.")

    if filesystem_confirmed and latency_elevated:
        confidence = "high"
        likely_cause = "claims-knowledge cache filesystem pressure is correlated with elevated APM latency for AI Claim Status."
    elif filesystem_confirmed or latency_elevated:
        confidence = "medium"
        likely_cause = "Splunk MCP returned partial degradation evidence, but did not confirm both filesystem pressure and elevated latency."
    else:
        confidence = "low"
        likely_cause = "Splunk MCP did not confirm filesystem and APM evidence; keep remediation recommendation-only until signals are verified."

    sources = [
        f"mcp:{tool.get('tool')}"
        for tool in case.get("mcp_tools", [])
        if tool.get("tool") != "tools/list" and tool.get("status") not in {"failed", "not_returned"}
    ]
    return {
        "source": "splunk_mcp",
        "enrichment_applied": bool(sources),
        "sources": sorted(set(sources)),
        "warnings": warnings,
        "confidence_band": confidence,
        "likely_cause": likely_cause,
        "candidate_actions": [BOUNDED_ACTION],
        "affected_journey": "claim_status_response",
        "suspect_service": "claims-knowledge",
        "p95_latency_ms": latency_ms,
        "cache_utilization": cache_utilization,
        "trace_ids": trace_tool.get("trace_ids", []),
    }


@log(span_type="tool", name="remediation.policy_check")
def policy_check(evidence: dict[str, Any]) -> dict[str, Any]:
    if evidence["confidence_band"] == "low":
        return {
            "eligible": False,
            "policy_mode": "recommend_only",
            "reason": "Confidence is too low for automated remediation.",
        }
    return {
        "eligible": True,
        "policy_mode": "approval_required",
        "reason": "Confidence is sufficient, but customer-facing remediation requires approval.",
    }


@log(span_type="agent", name="remediation.agent_evaluate")
def remediation_agent_evaluate(evidence: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    return {
        "recommended_action": evidence["candidate_actions"][0],
        "confidence_band": evidence["confidence_band"],
        "policy_mode": policy["policy_mode"],
        "reasoning_summary": evidence["likely_cause"],
        "needs_approval": True,
    }


@log(span_type="workflow", name="app.splunk_mcp_evidence_handoff")
def evaluate_mcp_evidence_case(case: dict[str, Any]) -> str:
    tools = splunk_mcp_tools_list(case)
    search = splunk_mcp_search_alerts(case)
    latency = splunk_mcp_get_apm_service_latency(case)
    traces = splunk_mcp_get_apm_exemplar_traces(case)
    cache_signalflow = splunk_mcp_execute_signalflow_cache(case)
    latency_signalflow = splunk_mcp_execute_signalflow_latency(case)
    evidence = build_evidence_bundle_from_mcp(case, tools, latency, traces, cache_signalflow, latency_signalflow)
    policy = policy_check(evidence)
    proposal = remediation_agent_evaluate(evidence, policy)

    expected = case["expected"]
    result = {
        "scenario_id": case["scenario_id"],
        "confidence_band": evidence["confidence_band"],
        "policy_mode": policy["policy_mode"],
        "proposed_action": proposal["recommended_action"],
        "warning_count": len(evidence["warnings"]),
        "mcp_sources": evidence["sources"],
        "trace_ids": evidence["trace_ids"],
        "alert_search_status": search.get("status"),
        "expected_confidence_band": expected["confidence_band"],
        "expected_policy_mode": expected["policy_mode"],
        "expected_proposed_action": expected["proposed_action"],
        "expected_warning_count": expected["warning_count"],
        "confidence_passed": evidence["confidence_band"] == expected["confidence_band"],
        "policy_passed": policy["policy_mode"] == expected["policy_mode"],
        "proposal_passed": proposal["recommended_action"] == expected["proposed_action"],
        "warnings_passed": len(evidence["warnings"]) == expected["warning_count"],
    }
    result["overall_passed"] = all(
        [
            result["confidence_passed"],
            result["policy_passed"],
            result["proposal_passed"],
            result["warnings_passed"],
        ]
    )
    return json.dumps(result, sort_keys=True)


@log(span_type="tool", name="remediation.approval_endpoint")
def approval_endpoint(case: dict[str, Any]) -> dict[str, Any]:
    approval_allowed = case["policy_mode"] == "approval_required"
    if not approval_allowed:
        return {
            "approval_allowed": False,
            "status": "blocked_by_policy",
            "reason": "Action is recommend_only and cannot be executed from the approval endpoint.",
        }
    if not case.get("operator_approved"):
        return {"approval_allowed": True, "status": "waiting_for_operator"}
    return {"approval_allowed": True, "status": "approved"}


@log(span_type="tool", name="remediation.execute_action")
def execute_action(case: dict[str, Any], approval: dict[str, Any]) -> dict[str, Any]:
    if approval["status"] == "blocked_by_policy":
        return {"status": "blocked_by_policy", "scenario_state": "unknown"}
    if approval["status"] != "approved":
        return {"status": "not_started", "scenario_state": "unknown"}
    return case.get("execute_result") or {"status": "failed", "scenario_state": "unknown"}


@log(span_type="tool", name="remediation.verify_action")
def verify_action(case: dict[str, Any], execution: dict[str, Any]) -> dict[str, Any]:
    if execution["status"] == "blocked_by_policy":
        return {"status": "not_started", "scenario_state": "unknown"}
    if execution["status"] == "not_started":
        return {"status": "not_started", "scenario_state": "unknown"}
    if execution["status"] == "failed":
        return {"status": "skipped", "scenario_state": execution.get("scenario_state", "unknown")}
    return case.get("verify_result") or {"status": "failed", "scenario_state": execution.get("scenario_state", "unknown")}


@log(span_type="agent", name="remediation.incident_status_update")
def incident_status_update(approval: dict[str, Any], execution: dict[str, Any], verification: dict[str, Any]) -> dict[str, Any]:
    if approval["status"] == "blocked_by_policy":
        incident_status = "proposed"
    elif approval["status"] == "waiting_for_operator":
        incident_status = "proposed"
    elif execution["status"] == "failed":
        incident_status = "open"
    elif verification["status"] == "validated":
        incident_status = "validated"
    elif execution["status"] == "executed":
        incident_status = "approved"
    else:
        incident_status = "proposed"
    return {"incident_status": incident_status}


@log(span_type="workflow", name="app.remediation_tool_flow")
def evaluate_remediation_tool_case(case: dict[str, Any]) -> str:
    approval = approval_endpoint(case)
    execution = execute_action(case, approval)
    verification = verify_action(case, execution)
    incident = incident_status_update(approval, execution, verification)
    expected = case["expected"]
    result = {
        "scenario_id": case["scenario_id"],
        "approval_allowed": approval["approval_allowed"],
        "execution_status": execution["status"],
        "verification_status": verification["status"],
        "incident_status": incident["incident_status"],
        "expected_approval_allowed": expected["approval_allowed"],
        "expected_execution_status": expected["execution_status"],
        "expected_verification_status": expected["verification_status"],
        "expected_incident_status": expected["incident_status"],
        "approval_passed": approval["approval_allowed"] == expected["approval_allowed"],
        "execution_passed": execution["status"] == expected["execution_status"],
        "verification_passed": verification["status"] == expected["verification_status"],
        "incident_status_passed": incident["incident_status"] == expected["incident_status"],
    }
    result["overall_passed"] = all(
        [
            result["approval_passed"],
            result["execution_passed"],
            result["verification_passed"],
            result["incident_status_passed"],
        ]
    )
    return json.dumps(result, sort_keys=True)


def parse_trace_json(trace: Any) -> dict[str, Any]:
    output = getattr(trace, "output", None)
    if isinstance(output, str):
        try:
            return json.loads(output)
        except json.JSONDecodeError:
            return {}
    return {}


def local_metric(name: str, field: str) -> LocalMetricConfig[float]:
    def scorer(trace: Any) -> tuple[float, dict[str, Any]]:
        result = parse_trace_json(trace)
        passed = bool(result.get(field))
        return (
            1.0 if passed else 0.0,
            {
                "scenario_id": str(result.get("scenario_id", "unknown")),
                "confidence_band": str(result.get("confidence_band", "unknown")),
                "policy_mode": str(result.get("policy_mode", "unknown")),
                "status": str(result.get("incident_status") or result.get("execution_status") or "unknown"),
            },
        )

    return LocalMetricConfig(name=name, scorer_fn=scorer, scorable_types=[StepType.trace], aggregatable_types=[])


def mcp_metrics() -> list[LocalMetricConfig[float]]:
    return [
        local_metric("mcp_confidence_match", "confidence_passed"),
        local_metric("mcp_policy_match", "policy_passed"),
        local_metric("mcp_proposal_match", "proposal_passed"),
        local_metric("mcp_warning_match", "warnings_passed"),
        local_metric("overall_mcp_handoff", "overall_passed"),
    ]


def tools_metrics() -> list[LocalMetricConfig[float]]:
    return [
        local_metric("approval_gate_match", "approval_passed"),
        local_metric("execution_status_match", "execution_passed"),
        local_metric("verification_status_match", "verification_passed"),
        local_metric("incident_status_match", "incident_status_passed"),
        local_metric("overall_tool_flow", "overall_passed"),
    ]


SUITES: dict[str, ExperimentSuite] = {
    "mcp": ExperimentSuite(
        key="mcp",
        display_name="Splunk MCP Evidence Handoff",
        name_prefix="cl26-splunk-mcp-handoff",
        story="Does the app respond correctly to real Splunk MCP evidence quality and MCP tool failures?",
        dataset=mcp_evidence_dataset,
        runner=evaluate_mcp_evidence_case,
        metrics=mcp_metrics,
    ),
    "tools": ExperimentSuite(
        key="tools",
        display_name="Remediation Tool Flow",
        name_prefix="cl26-remediation-tool-flow",
        story="Does approval, execute, and verify behave correctly for the app's bounded cache cleanup action?",
        dataset=remediation_tools_dataset,
        runner=evaluate_remediation_tool_case,
        metrics=tools_metrics,
    ),
}


def run_suite(suite: ExperimentSuite, project: str, group: str, explicit_name: str | None = None) -> dict[str, Any]:
    experiment_name = explicit_name or f"{suite.name_prefix}-{int(time.time())}"
    dataset = suite.dataset()
    metrics = suite.metrics()
    result = run_experiment(
        experiment_name,
        project=project,
        dataset=dataset,
        function=suite.runner,
        metrics=metrics,
        experiment_group=group,
        experiment_tags={
            "demo": "ciscolive26",
            "suite": suite.key,
            "story": suite.story,
            "runner": "scripts/galileo-remediation-experiment.py",
        },
    )
    return {
        "suite": suite.key,
        "displayName": suite.display_name,
        "experiment": experiment_name,
        "project": project,
        "group": group,
        "datasetRows": len(dataset),
        "metrics": [metric.name for metric in metrics],
        "link": result.get("link"),
        "message": result.get("message"),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Cisco Live Galileo app-aligned experiment suites.")
    parser.add_argument(
        "--suite",
        choices=[*SUITES.keys(), "all"],
        default=os.getenv("GALILEO_EXPERIMENT_SUITE", "mcp"),
        help="Experiment suite to run. Defaults to mcp.",
    )
    parser.add_argument(
        "--name",
        default=os.getenv("GALILEO_EXPERIMENT_NAME"),
        help="Explicit experiment name. Only valid when running one suite.",
    )
    return parser.parse_args()


def main() -> int:
    configure_environment()
    args = parse_args()
    if args.suite == "all" and args.name:
        raise SystemExit("--name can only be used with one suite")

    project = os.getenv("GALILEO_PROJECT", DEFAULT_PROJECT)
    group = os.getenv("GALILEO_EXPERIMENT_GROUP", DEFAULT_GROUP)
    selected_suites = list(SUITES.values()) if args.suite == "all" else [SUITES[args.suite]]
    summaries = [run_suite(suite, project, group, args.name) for suite in selected_suites]
    print(json.dumps({"experiments": summaries}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
