"""Smoke test for the multi-tenant split (targets + orchestrator logic).

Exercises the pure, cluster-free logic that guarantees per-stream / per-target
isolation — the core of the CLAUDE.md design. No Kubernetes API or network
access required. Run from the app directory:

    python smoke_test.py
"""
import re
import sys

import orchestrator as o
import targets as t

DNS_1123 = re.compile(r"^[a-z0-9]([-a-z0-9]*[a-z0-9])?$")
failures: list[str] = []


def check(cond: bool, msg: str) -> None:
    status = "OK " if cond else "FAIL"
    print(f"{status} {msg}")
    if not cond:
        failures.append(msg)


def env_map(manifest: dict) -> dict:
    container = manifest["spec"]["template"]["spec"]["containers"][0]
    return {e["name"]: e for e in container["env"]}


def config_maps(manifest: dict) -> set[str]:
    container = manifest["spec"]["template"]["spec"]["containers"][0]
    return {ref["configMapRef"]["name"] for ref in container["envFrom"]}


# --- targets -----------------------------------------------------------------
check(set(t.TARGETS) == {"standalone", "us-splunk-show", "eu-splunk-show"},
      "three targets defined")
check(t.DEFAULT_TARGET in t.TARGETS, "default target is valid")

secrets = {tg.secret_name for tg in t.TARGETS.values()}
check(len(secrets) == 3, "each target uses a distinct secret")

# --- naming is DNS-1123 safe and deterministic ------------------------------
messy = "  Derek Mitchell!! (US) --  "
name = o.backend_name(messy, "us-splunk-show")
check(bool(DNS_1123.match(name)), f"backend name is DNS-1123 safe: {name}")
check(len(name) <= 63, f"backend name <= 63 chars: {len(name)}")
check(o.backend_name(messy, "us-splunk-show") == name, "naming is deterministic")
check(len(o.backend_name("x" * 300, "standalone")) <= 63, "overlong stream truncated")

distinct = {o.backend_name("shared-stream", k) for k in t.TARGETS}
check(len(distinct) == 3, "same stream on different targets → distinct names")

# --- deployment manifest wires each target correctly ------------------------
STREAM = "derek-demo"

dep_std = o._deployment_manifest(o.backend_name(STREAM, "standalone"), STREAM, "standalone")
env_std = env_map(dep_std)
check(config_maps(dep_std) >= {"healthcare-assistant-config", "postgres-config",
                               "splunk-ao-config", "splunk-agent-control-config"},
      "standalone mounts common + standalone config maps")
check(env_std["SPLUNK_AO_AGENT_STREAM"]["value"] == STREAM,
      "standalone overrides SPLUNK_AO_AGENT_STREAM with the user stream (not the slug)")
check(env_std["SPLUNK_AO_API_KEY"]["valueFrom"]["secretKeyRef"]["name"] == "splunk-ao-secret",
      "standalone auth comes from splunk-ao-secret / SPLUNK_AO_API_KEY")
container_std = dep_std["spec"]["template"]["spec"]["containers"][0]
check(container_std["command"][:2] == ["uvicorn", "server:app"], "back-end runs uvicorn server:app")
check("resources" in container_std and container_std["resources"]["limits"]["memory"] == "1Gi",
      "back-end resources tuned (1Gi mem limit)")
check(dep_std["spec"]["template"]["spec"].get("serviceAccountName"),
      "back-end runs under a service account (for self-termination)")

dep_us = o._deployment_manifest(o.backend_name(STREAM, "us-splunk-show"), STREAM, "us-splunk-show")
env_us = env_map(dep_us)
check(config_maps(dep_us) >= {"splunk-ao-config-us-splunk-show",
                              "splunk-agent-control-config-us-splunk-show"},
      "US target mounts US config maps")
check(env_us["SPLUNK_AO_O11Y_TOKEN"]["valueFrom"]["secretKeyRef"]["name"]
      == "splunk-ao-secret-us-splunk-show",
      "US auth comes from the US o11y secret / SPLUNK_AO_O11Y_TOKEN")
check("SPLUNK_AO_API_KEY" not in env_us, "US target does not inject the standalone API key")

# --- service selector matches the deployment pod labels ---------------------
svc = o._service_manifest(o.backend_name(STREAM, "standalone"), "standalone")
check(svc["spec"]["selector"] == {"app": o.backend_name(STREAM, "standalone")},
      "service selector matches the deployment's pod label")

print()
if failures:
    print(f"SMOKE TEST FAILED — {len(failures)} check(s) failed")
    sys.exit(1)
print("SMOKE TEST PASSED")
