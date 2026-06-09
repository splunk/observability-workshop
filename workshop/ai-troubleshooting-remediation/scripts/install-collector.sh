#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSHOP_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

: "${SPLUNK_ACCESS_TOKEN:?Set SPLUNK_ACCESS_TOKEN before installing the collector.}"
: "${SPLUNK_REALM:?Set SPLUNK_REALM before installing the collector.}"

CLUSTER_NAME="${CLUSTER_NAME:-ai-remediation-cluster}"
ENVIRONMENT="${ENVIRONMENT:-ai-remediation-workshop}"
SPLUNK_OTEL_CHART_VERSION="${SPLUNK_OTEL_CHART_VERSION:-0.149.0}"
read -r -a HELM <<< "${HELM_CMD:-helm}"
read -r -a KUBECTL <<< "${KUBECTL_CMD:-kubectl}"

"${HELM[@]}" repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart >/dev/null
"${HELM[@]}" repo update >/dev/null

"${HELM[@]}" upgrade --install splunk-otel-collector \
  --version "$SPLUNK_OTEL_CHART_VERSION" \
  --set="splunkObservability.realm=$SPLUNK_REALM" \
  --set="splunkObservability.accessToken=$SPLUNK_ACCESS_TOKEN" \
  --set="clusterName=$CLUSTER_NAME" \
  --set="environment=$ENVIRONMENT" \
  --set="agent.service.enabled=true" \
  -f "$WORKSHOP_DIR/k8s/collector-values.yaml" \
  splunk-otel-collector-chart/splunk-otel-collector

"${KUBECTL[@]}" rollout status daemonset/splunk-otel-collector-agent --timeout=5m
"${KUBECTL[@]}" rollout status deployment/splunk-otel-collector-k8s-cluster-receiver --timeout=5m

echo "Splunk OpenTelemetry Collector installed for cluster=$CLUSTER_NAME environment=$ENVIRONMENT realm=$SPLUNK_REALM"
