#!/usr/bin/env python3
"""
SAO Trace Generator

Replays a fixed set of traces (defined in input.csv, exported from Splunk Agent
Observability) so demos and workshops always have deterministic data to look at.

Each run:
  * generates fresh trace/span/session/tool-call IDs,
  * re-bases all timestamps so the replayed traces end "now",
  * keeps the original relative timing/durations, with a small random jitter,
  * sends everything through SplunkAOLogger (including Agent Control spans).

Configuration (environment variables):
  SPLUNK_AO_PROJECT        project name
  SPLUNK_AO_AGENT_STREAM   agent stream name
  SPLUNK_AO_REALM          Splunk Observability Cloud realm (e.g. us1)
  SPLUNK_AO_O11Y_TOKEN     Splunk Observability Cloud access token

Usage:
  python generate_traces.py                 # send traces
  python generate_traces.py --dry-run       # print the span trees, send nothing
"""
from __future__ import annotations

import argparse
import ast
import csv
import logging
import os
import random
import re
import sys
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger("sao-trace-generator")

DEFAULT_INPUT = Path(__file__).parent / "input.csv"
FALLBACK_TRACE_NAME = "Hallucination Demo"  # used when a trace has no agent root span
CONTAINER_TYPES = {"agent", "workflow", "tool"}

csv.field_size_limit(sys.maxsize)


# --------------------------------------------------------------------------- #
# CSV parsing
# --------------------------------------------------------------------------- #
@dataclass
class Node:
    row: dict
    id: str
    parent_id: str
    type: str
    offset_ns: int = 0  # start offset from trace start
    dur_ns: int = 0
    children: list["Node"] = field(default_factory=list)


@dataclass
class TracePlan:
    source_trace_id: str
    conversation_id: str
    roots: list[Node]  # direct children of the trace
    start: datetime  # original start (used for offsets only)


_ENUM_RE = re.compile(r"<[A-Za-z]+\.\w+: '([^']*)'>")
_CALL_ID_RE = re.compile(r"call_[A-Za-z0-9]{10,}")


def _parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value)


def _to_int(value: str) -> Optional[int]:
    try:
        return int(float(value)) if value not in ("", None) else None
    except ValueError:
        return None


def parse_repr(value: str) -> Any:
    """Parse the Python-repr strings exported by Agent Observability.

    Enum reprs such as <MessageRole.assistant: 'assistant'> are replaced with
    their plain value. Returns the original string if it can't be parsed.
    """
    if not value or value[0] not in "[{":
        return value
    try:
        return ast.literal_eval(_ENUM_RE.sub(r"'\1'", value))
    except (ValueError, SyntaxError):
        return value


def load_traces(path: Path) -> list[TracePlan]:
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        raise SystemExit(f"{path} contains no spans")

    by_trace: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_trace[r["trace_id"]].append(r)

    plans: list[TracePlan] = []
    for trace_id, trace_rows in by_trace.items():
        nodes = {r["id"]: Node(r, r["id"], r["parent_id"], r["type"]) for r in trace_rows}
        roots: list[Node] = []
        for n in nodes.values():
            parent = nodes.get(n.parent_id)
            (parent.children if parent else roots).append(n)

        start = min(_parse_ts(n.row["created_at"]) for n in nodes.values())
        for n in nodes.values():
            n.offset_ns = int((_parse_ts(n.row["created_at"]) - start).total_seconds() * 1e9)
            n.dur_ns = _to_int(n.row["metrics/duration_ns"]) or 0
            n.children.sort(key=lambda c: c.offset_ns)
        roots.sort(key=lambda c: c.offset_ns)

        conv = next((r["user_metadata/gen_ai.conversation.id"] for r in trace_rows
                     if r.get("user_metadata/gen_ai.conversation.id")), "")
        plans.append(TracePlan(trace_id, conv, roots, start))

    plans.sort(key=lambda p: p.start)
    return plans


# --------------------------------------------------------------------------- #
# Timing: jitter + re-basing to "now"
# --------------------------------------------------------------------------- #
def _walk(nodes: list[Node]):
    for n in nodes:
        yield n
        yield from _walk(n.children)


def apply_jitter(plan: TracePlan, rng: random.Random, spread: float) -> int:
    """Jitter durations in place. Returns the trace duration in ns.

    Offsets and durations share one per-trace scale factor (keeps the relative
    timing recognisable); each span also gets a small independent wobble.
    Container spans are then stretched if needed so they still contain children.
    """
    scale = rng.uniform(1 - spread, 1 + spread)
    for n in _walk(plan.roots):
        n.offset_ns = int(n.offset_ns * scale)
        n.dur_ns = int(n.dur_ns * scale * rng.uniform(0.97, 1.03))

    def fit(n: Node) -> None:
        for c in n.children:
            fit(c)
        if n.children:
            needed = max(c.offset_ns + c.dur_ns for c in n.children) - n.offset_ns
            n.dur_ns = max(n.dur_ns, needed)

    for r in plan.roots:
        fit(r)
    return max((r.offset_ns + r.dur_ns for r in plan.roots), default=0)


# --------------------------------------------------------------------------- #
# Row -> SDK argument helpers
# --------------------------------------------------------------------------- #
class Replayer:
    def __init__(self, sao_logger: Any, rng: random.Random):
        self.log = sao_logger
        self.rng = rng
        self._call_ids: dict[str, str] = {}

    # fresh OpenAI-style tool call IDs, consistent within a run
    def _fresh(self, text: str) -> str:
        if not text:
            return text

        def sub(m: re.Match) -> str:
            old = m.group(0)
            if old not in self._call_ids:
                self._call_ids[old] = "call_" + uuid.uuid4().hex[:24]
            return self._call_ids[old]

        return _CALL_ID_RE.sub(sub, text)

    def _val(self, raw: str) -> Any:
        return parse_repr(self._fresh(raw))

    @staticmethod
    def _text(value: Any) -> str:
        if isinstance(value, dict) and "content" in value:
            return str(value["content"])
        return value if isinstance(value, str) else str(value)

    # ---- per-type emitters ------------------------------------------------ #
    def emit(self, node: Node, t0: datetime) -> None:
        r = node.row
        created = t0 + timedelta(microseconds=node.offset_ns / 1000)
        common = {"created_at": created, "duration_ns": node.dur_ns}
        name = r["name"] or None
        inp = self._fresh(r["input"])
        out = self._fresh(r["output"])
        kind = node.type

        if kind in ("agent", "workflow", "tool"):
            if kind == "agent":
                from galileo_core.schemas.logging.agent import AgentType
                try:
                    agent_type = AgentType(r["agent_type"]) if r["agent_type"] else None
                except ValueError:
                    agent_type = None
                self.log.add_agent_span(input=inp, name=name, agent_type=agent_type,
                                        status_code=200, **common)
            elif kind == "workflow":
                self.log.add_workflow_span(input=inp, name=name, status_code=200, **common)
            else:
                self.log.add_tool_span(input=inp, output=out, name=name, status_code=200,
                                       tool_call_id=self._fresh(r["tool_call_id"]) or None, **common)
            for child in node.children:
                self.emit(child, t0)
            if kind != "tool":  # tool spans are completed leaves in the SDK
                self.log.conclude(output=out, duration_ns=node.dur_ns, status_code=200)

        elif kind == "llm":
            tools = parse_repr(r["tools"]) if r["tools"] else None
            kwargs: dict[str, Any] = dict(
                input=self._val(r["input"]), output=self._val(r["output"]),
                model=r["model"] or None, name=name, status_code=200,
                num_input_tokens=_to_int(r["metrics/num_input_tokens"]),
                num_output_tokens=_to_int(r["metrics/num_output_tokens"]),
                total_tokens=_to_int(r["metrics/num_total_tokens"]),
                tools=tools if isinstance(tools, list) else None, **common)
            if r["temperature"]:
                kwargs["temperature"] = round(float(r["temperature"]), 2)
            ttft = r.get("user_metadata/gen_ai.response.time_to_first_chunk")
            if ttft:
                kwargs["time_to_first_token_ns"] = int(float(ttft) * 1e9)
            self.log.add_llm_span(**kwargs)

        elif kind == "retriever":
            docs = self._val(r["output"])
            if not isinstance(docs, list):
                docs = [{"content": str(docs), "metadata": {}}]
            self.log.add_retriever_span(input=inp, output=docs, name=name,
                                        status_code=200, **common)

        elif kind == "control":
            from galileo_core.schemas.logging.control import (ControlAction, ControlCheckStage,
                                                              ControlResult)
            from splunk_ao.logger.control import ControlAppliesTo
            res = parse_repr(r["output"])
            result = None
            if isinstance(res, dict):
                result = ControlResult(
                    action=ControlAction(res.get("action", "observe")),
                    matched=bool(res.get("matched", False)),
                    confidence=res.get("confidence"),
                    error_message=res.get("error_message"))
            self.log.add_control_span(
                input=inp, output=result, name=name, status_code=200,
                control_id=_to_int(r["control_id"]),
                agent_name=r["agent_name"] or None,
                check_stage=ControlCheckStage(r["check_stage"]) if r["check_stage"] else None,
                applies_to=ControlAppliesTo(r["applies_to"]) if r["applies_to"] else None,
                evaluator_name=r["evaluator_name"] or None,
                selector_path=r["selector_path"] or None, **common)
        else:
            logger.warning("Skipping unsupported span type %r (%s)", kind, name)

    # ---- one trace -------------------------------------------------------- #
    def replay_trace(self, plan: TracePlan, t0: datetime, trace_dur_ns: int) -> None:
        # Controls are siblings of the agent span at trace level, but their
        # timestamps fall inside the agent's run, so add them once the agent
        # span is concluded.
        main = [n for n in plan.roots if n.type != "control"]
        controls = [n for n in plan.roots if n.type == "control"]

        first = main[0]
        trace_input = self._text(self._val(first.row["input"]))
        last = max(main, key=lambda n: n.offset_ns + n.dur_ns)
        trace_output = self._text(self._val(last.row["output"]))
        agent_root = next((n for n in main if n.type == "agent"), None)
        trace_name = agent_root.row["name"] if agent_root else FALLBACK_TRACE_NAME

        self.log.start_trace(input=trace_input, name=trace_name, created_at=t0,
                             duration_ns=trace_dur_ns)
        for n in main:
            self.emit(n, t0)
        for n in controls:
            self.emit(n, t0)
        self.log.conclude(output=trace_output, duration_ns=trace_dur_ns, status_code=200)


# --------------------------------------------------------------------------- #
# Dry run (no SDK needed)
# --------------------------------------------------------------------------- #
def print_plan(plan: TracePlan, t0: datetime, trace_dur_ns: int) -> None:
    print(f"\nTRACE (source {plan.source_trace_id[:8]}) start={t0.isoformat()} "
          f"dur={trace_dur_ns/1e9:.2f}s")

    def show(nodes: list[Node], depth: int) -> None:
        for n in nodes:
            print(f"{'  ' * depth}- {n.type:9s} {n.row['name'][:60]:60s} "
                  f"+{n.offset_ns/1e9:6.2f}s  {n.dur_ns/1e9:6.2f}s")
            show(n.children, depth + 1)

    show(plan.roots, 1)


# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="span CSV (default: input.csv)")
    ap.add_argument("--dry-run", action="store_true", help="print the plan; don't send anything")
    ap.add_argument("--jitter", type=float, default=0.15,
                    help="max +/- fraction of timing jitter per trace (default 0.15)")
    ap.add_argument("--seed", type=int, default=None, help="random seed (for reproducible jitter)")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")

    rng = random.Random(args.seed)
    plans = load_traces(args.input)
    logger.info("Loaded %d traces (%d spans) from %s", len(plans),
                sum(1 for p in plans for _ in _walk(p.roots)), args.input)

    # Timing: lay the traces out back-to-back (small random gaps) ending at "now".
    durations = [apply_jitter(p, rng, args.jitter) for p in plans]
    gaps = [int(rng.uniform(2, 8) * 1e9) for _ in plans]
    total = sum(durations) + sum(gaps)
    cursor = datetime.now(timezone.utc) - timedelta(microseconds=total / 1000)
    starts = []
    for d, g in zip(durations, gaps):
        starts.append(cursor)
        cursor += timedelta(microseconds=(d + g) / 1000)

    if args.dry_run:
        for p, t0, d in zip(plans, starts, durations):
            print_plan(p, t0, d)
        return 0

    project = os.getenv("SPLUNK_AO_PROJECT")
    stream = os.getenv("SPLUNK_AO_AGENT_STREAM", "default")
    if not project:
        logger.error("SPLUNK_AO_PROJECT is not set")
        return 2

    from splunk_ao import SplunkAOLogger

    sao = SplunkAOLogger(project=project, agent_stream=stream)
    replayer = Replayer(sao, rng)
    run_id = uuid.uuid4().hex[:8]
    sessions: dict[str, str] = {}  # source conversation id -> new session id

    for p, t0, d in zip(plans, starts, durations):
        key = p.conversation_id or p.source_trace_id
        # Traces that shared a conversation in the source share a (new) session.
        # start_session() with a known external_id re-selects that session.
        external_id = sessions.setdefault(key, str(uuid.uuid4()))
        sao.start_session(name=f"SAO Trace Generator {run_id}", external_id=external_id)
        replayer.replay_trace(p, t0, d)
        logger.info("Replayed trace %s", p.source_trace_id[:8])

    sao.flush()
    logger.info("Sent %d traces to project=%s stream=%s", len(plans), project, stream)
    return 0


if __name__ == "__main__":
    sys.exit(main())
