"""Embedded orchestrator: provisions a back-end per (agent_stream, target).

Lives inside the front-end pod. Given a stream name + target, it ensures a
Deployment + ClusterIP Service exist, waits for readiness, and returns the
in-cluster URL the front-end should POST queries to. Creation is idempotent:
the object name is derived deterministically from (stream, target), so the same
presenter returning gets the same back-end, and concurrent creates collapse via
AlreadyExists.

Requires a ServiceAccount with create/get/delete on deployments + services in
the pod's namespace (see k8s-demo-local.yaml).
"""
from __future__ import annotations

import hashlib
import logging
import os
import re
import sys
import time

from targets import COMMON_CONFIG_MAPS, get_target

logger = logging.getLogger("healthcare.orchestrator")

# The front-end (Streamlit) never configures logging, so attach our own stdout
# handler once so orchestrator activity shows up in `kubectl logs`.
if not logger.handlers:
    _h = logging.StreamHandler(sys.stdout)
    _h.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
    logger.addHandler(_h)
    logger.setLevel(logging.INFO)
    logger.propagate = False

# Container "waiting" reasons that won't resolve on their own within a demo —
# fail fast and report them instead of waiting out the whole readiness timeout.
_FATAL_WAITING_REASONS = frozenset({
    "ImagePullBackOff", "ErrImagePull", "InvalidImageName",
    "CrashLoopBackOff", "CreateContainerConfigError", "CreateContainerError",
})

# The back-end image. Defaults to the published tag but is overridable so a
# locally built image can be used for testing.
BACKEND_IMAGE = os.getenv(
    "BACKEND_IMAGE", "ghcr.io/splunk/healthcare-assistant:demo-v1"
)
BACKEND_PORT = 8000
BACKEND_IDLE_TTL_SECONDS = os.getenv("BACKEND_IDLE_TTL_SECONDS", "7200")
READY_TIMEOUT_SECONDS = int(os.getenv("BACKEND_READY_TIMEOUT_SECONDS", "180"))
# Image pull: published images exist in the registry; a locally built tag won't,
# so allow IfNotPresent for local testing.
IMAGE_PULL_POLICY = os.getenv("BACKEND_IMAGE_PULL_POLICY", "IfNotPresent")

_DNS_LABEL_MAX = 63
_SLUG_BODY_MAX = 40  # leaves room for the "backend-<target>-" prefix + hash suffix


def _namespace() -> str:
    path = "/var/run/secrets/kubernetes.io/serviceaccount/namespace"
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return f.read().strip()
    return os.getenv("POD_NAMESPACE", "default")


def slug(stream: str) -> str:
    """Slugify a stream name to a stable DNS-1123 fragment with a hash suffix."""
    base = re.sub(r"[^a-z0-9]+", "-", stream.strip().lower()).strip("-")
    base = re.sub(r"-{2,}", "-", base)[:_SLUG_BODY_MAX].strip("-") or "stream"
    digest = hashlib.sha1(stream.strip().encode("utf-8")).hexdigest()[:6]
    return f"{base}-{digest}"


def backend_name(stream: str, target_key: str) -> str:
    name = f"backend-{target_key}-{slug(stream)}"
    return name[:_DNS_LABEL_MAX].strip("-")


def backend_url(name: str, namespace: str | None = None) -> str:
    ns = namespace or _namespace()
    return f"http://{name}.{ns}.svc.cluster.local:{BACKEND_PORT}"


def _load_clients():
    from kubernetes import client, config as k8s_config

    try:
        k8s_config.load_incluster_config()
    except Exception:
        k8s_config.load_kube_config()
    return client.AppsV1Api(), client.CoreV1Api()


def _deployment_manifest(name: str, stream: str, target_key: str) -> dict:
    target = get_target(target_key)
    labels = {
        "app": name,
        "component": "healthcare-backend",
        "demo.splunk/target": target_key,
    }
    env_from = [
        {"configMapRef": {"name": cm}}
        for cm in (*COMMON_CONFIG_MAPS, *target.config_maps)
    ]
    env = [
        # User-entered stream overrides the ConfigMap default (direct env wins).
        {"name": "SPLUNK_AO_AGENT_STREAM", "value": stream},
        {"name": "BACKEND_NAME", "value": name},
        {"name": "BACKEND_IDLE_TTL_SECONDS", "value": str(BACKEND_IDLE_TTL_SECONDS)},
        {"name": "POD_NAMESPACE",
         "valueFrom": {"fieldRef": {"fieldPath": "metadata.namespace"}}},
        {"name": "OPENAI_BASE_URL",
         "valueFrom": {"secretKeyRef": {"name": "openai-api", "key": "openai-api-endpoint"}}},
        {"name": "OPENAI_API_KEY",
         "valueFrom": {"secretKeyRef": {"name": "openai-api", "key": "openai-api-key"}}},
        {"name": "POSTGRES_PASSWORD",
         "valueFrom": {"secretKeyRef": {"name": "postgres-credentials", "key": "POSTGRES_PASSWORD"}}},
        {"name": target.auth_env,
         "valueFrom": {"secretKeyRef": {"name": target.secret_name, "key": target.auth_secret_key}}},
    ]
    return {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {"name": name, "labels": labels,
                     "annotations": {"demo.splunk/stream": stream}},
        "spec": {
            "replicas": 1,
            "selector": {"matchLabels": {"app": name}},
            "template": {
                "metadata": {"labels": labels},
                "spec": {
                    "serviceAccountName": os.getenv("BACKEND_SERVICE_ACCOUNT", "healthcare-demo"),
                    "containers": [{
                        "name": "backend",
                        "image": BACKEND_IMAGE,
                        "imagePullPolicy": IMAGE_PULL_POLICY,
                        "command": ["uvicorn", "server:app", "--host", "0.0.0.0",
                                    "--port", str(BACKEND_PORT)],
                        "ports": [{"containerPort": BACKEND_PORT, "name": "http"}],
                        "envFrom": env_from,
                        "env": env,
                        "readinessProbe": {
                            "httpGet": {"path": "/ready", "port": BACKEND_PORT},
                            "initialDelaySeconds": 5, "periodSeconds": 5,
                        },
                        "resources": {
                            "requests": {"memory": "256Mi", "cpu": "100m"},
                            "limits": {"memory": "1Gi", "cpu": "500m"},
                        },
                        "securityContext": {
                            "allowPrivilegeEscalation": False,
                            "runAsNonRoot": True,
                            "runAsUser": 1000,
                            "capabilities": {"drop": ["ALL"]},
                        },
                    }],
                },
            },
        },
    }


def _service_manifest(name: str, target_key: str) -> dict:
    return {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {"name": name,
                     "labels": {"component": "healthcare-backend",
                                "demo.splunk/target": target_key}},
        "spec": {
            "selector": {"app": name},
            "ports": [{"port": BACKEND_PORT, "targetPort": BACKEND_PORT, "protocol": "TCP"}],
            "type": "ClusterIP",
        },
    }


def ensure_backend(stream: str, target_key: str, *, wait: bool = True) -> dict:
    """Ensure a back-end exists for (stream, target); return {name, url, ready, detail}.

    Idempotent and self-healing: if the Deployment already exists it is *patched*
    to the desired spec, so an upgraded app image/config rolls out instead of
    serving stale code (a no-op when nothing changed). When wait=True, blocks
    until the Deployment reports a ready replica or READY_TIMEOUT_SECONDS elapses,
    failing fast on fatal pod states (e.g. ImagePullBackOff).
    """
    from kubernetes.client.rest import ApiException

    get_target(target_key)  # validate early
    apps, core = _load_clients()
    ns = _namespace()
    name = backend_name(stream, target_key)

    dep = _deployment_manifest(name, stream, target_key)
    try:
        apps.create_namespaced_deployment(ns, dep)
        logger.info("Created Deployment/%s", name)
    except ApiException as e:
        if e.status == 409:
            # Reconcile an existing back-end to the desired spec. A rolling update
            # happens only if the pod template actually changed.
            apps.patch_namespaced_deployment(name, ns, dep)
            logger.info("Reconciled existing Deployment/%s to desired spec", name)
        else:
            raise

    svc = _service_manifest(name, target_key)
    try:
        core.create_namespaced_service(ns, svc)
        logger.info("Created Service/%s", name)
    except ApiException as e:
        if e.status == 409:
            logger.info("Service/%s already exists; reusing", name)
        else:
            raise

    ready, detail = _wait_ready(apps, core, ns, name) if wait else (False, "not waited")
    return {"name": name, "url": backend_url(name, ns), "ready": ready, "detail": detail}


def _pod_failure_reason(core, namespace: str, name: str) -> str | None:
    """Return a human-readable reason a back-end pod is stuck, if any."""
    try:
        pods = core.list_namespaced_pod(namespace, label_selector=f"app={name}").items
    except Exception as e:  # pragma: no cover - transient API error
        logger.debug("list pods %s: %s", name, e)
        return None
    for pod in pods:
        for cs in (pod.status.container_statuses or []):
            waiting = cs.state.waiting if cs.state else None
            reason = getattr(waiting, "reason", None)
            if reason and reason not in ("ContainerCreating", "PodInitializing"):
                return f"{reason}: {waiting.message}" if waiting.message else reason
    return None


def _wait_ready(apps, core, namespace: str, name: str) -> tuple[bool, str]:
    deadline = time.monotonic() + READY_TIMEOUT_SECONDS
    last = "waiting for the back-end pod to schedule"
    while time.monotonic() < deadline:
        try:
            dep = apps.read_namespaced_deployment_status(name, namespace)
            if (dep.status.ready_replicas or 0) >= 1:
                logger.info("Back-end %s is ready", name)
                return True, "ready"
        except Exception as e:  # transient during scheduling
            logger.debug("read status %s: %s", name, e)
        reason = _pod_failure_reason(core, namespace, name)
        if reason:
            last = reason
            fatal = reason.split(":", 1)[0] in _FATAL_WAITING_REASONS
            if fatal:
                logger.warning("Back-end %s not starting: %s", name, reason)
                return False, reason
        time.sleep(3)
    logger.warning("Back-end %s not ready within %ss (%s)", name, READY_TIMEOUT_SECONDS, last)
    return False, f"timed out after {READY_TIMEOUT_SECONDS}s — {last}"
