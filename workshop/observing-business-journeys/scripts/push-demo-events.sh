#!/usr/bin/env bash
set -euo pipefail

HEC_URL="${SPLUNK_HEC_URL:-}"
HEC_TOKEN="${SPLUNK_HEC_TOKEN:-}"
HEC_INDEX="${SPLUNK_HEC_INDEX:-o11y_alerts}"
HEC_SOURCE="${SPLUNK_HEC_SOURCE:-o11y-business-journey-demo}"
HEC_SOURCETYPE="${SPLUNK_HEC_SOURCETYPE:-splunk:o11y:detector}"
SESSION_ID="${WORKSHOP_SESSION:-business-journey-workshop}"

usage() {
  cat <<'EOF'
Push demo Observability Cloud-like alert events to Splunk HEC.

Required environment:
  SPLUNK_HEC_URL      HEC URL, either https://host:8088 or https://host:8088/services/collector/event
  SPLUNK_HEC_TOKEN    HEC token

Optional environment:
  SPLUNK_HEC_INDEX       default: o11y_alerts
  SPLUNK_HEC_INSECURE    true to skip TLS verification for lab certs
  WORKSHOP_SESSION       default: business-journey-workshop

Usage:
  ./scripts/push-demo-events.sh print checkout
  ./scripts/push-demo-events.sh trigger checkout
  ./scripts/push-demo-events.sh clear checkout
  ./scripts/push-demo-events.sh sequence checkout
  ./scripts/push-demo-events.sh demo

Actions:
  print      Print one trigger payload without sending it.
  trigger    Send one active detector event.
  clear      Send one clear event for the same scenario.
  sequence   Send trigger, wait, then clear.
  demo       Send active events for checkout, cart, and catalog.

Scenarios:
  checkout | cart | catalog | confirm-order
EOF
}

require_env() {
  local name="$1"
  if [[ -z "${!name:-}" ]]; then
    echo "Missing required environment variable: $name" >&2
    exit 1
  fi
}

normalize_hec_url() {
  local url="$1"
  url="${url%/}"
  case "$url" in
    */services/collector/event)
      printf '%s\n' "$url"
      ;;
    */services/collector)
      printf '%s/event\n' "$url"
      ;;
    *)
      printf '%s/services/collector/event\n' "$url"
      ;;
  esac
}

scenario_fields() {
  local scenario="$1"
  case "$scenario" in
    checkout)
      printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
        "Complete Checkout" "checkout" "critical" "payment" \
        "Astronomy Shop - checkout payment failures" "Critical" "500" \
        "Customers cannot place orders; revenue capture is directly at risk."
      ;;
    cart)
      printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
        "Manage Cart" "cart" "high" "cart" \
        "Astronomy Shop - cart operation failures" "Major" "250" \
        "Customers cannot build or maintain an order."
      ;;
    catalog)
      printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
        "Browse Catalog" "catalog" "medium" "product-catalog" \
        "Astronomy Shop - catalog browse failures" "Minor" "100" \
        "Customers cannot reliably discover products or recommendations."
      ;;
    confirm-order|confirm_order|post-order)
      printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
        "Confirm Order" "post-order" "high" "email" \
        "Astronomy Shop - order confirmation lag" "Major" "200" \
        "Customers might not receive confirmation and downstream order records can lag."
      ;;
    *)
      echo "Unknown scenario: $scenario" >&2
      usage >&2
      exit 1
      ;;
  esac
}

build_payload() {
  local action="$1"
  local scenario="$2"
  local now event_type state incident_id
  local transaction capability criticality service detector severity revenue impact

  IFS=$'\t' read -r transaction capability criticality service detector severity revenue impact < <(scenario_fields "$scenario")

  now="$(date +%s)"
  incident_id="business-journey-${scenario//_/-}"

  if [[ "$action" == "clear" ]]; then
    event_type="detector_cleared"
    state="clear"
  else
    event_type="detector_triggered"
    state="active"
  fi

  jq -n \
    --argjson time "$now" \
    --arg index "$HEC_INDEX" \
    --arg source "$HEC_SOURCE" \
    --arg sourcetype "$HEC_SOURCETYPE" \
    --arg host "$SESSION_ID" \
    --arg event_type "$event_type" \
    --arg state "$state" \
    --arg incident_id "$incident_id" \
    --arg detector "$detector" \
    --arg severity "$severity" \
    --arg application "astronomy-shop" \
    --arg transaction "$transaction" \
    --arg capability "$capability" \
    --arg criticality "$criticality" \
    --arg service "$service" \
    --arg environment "business-journey-workshop" \
    --argjson revenue "$revenue" \
    --arg impact "$impact" \
    '{
      time: $time,
      index: $index,
      source: $source,
      sourcetype: $sourcetype,
      host: $host,
      event: {
        sflo_event_type: $event_type,
        sflo_state: $state,
        sflo_incident_id: $incident_id,
        sflo_detector: $detector,
        sflo_severity: $severity,
        sflo_current_value: (if $state == "active" then 1 else 0 end),
        business_application: $application,
        business_transaction: $transaction,
        business_capability: $capability,
        business_criticality: $criticality,
        impacted_service: $service,
        sf_service: $service,
        sf_environment: $environment,
        estimated_revenue_per_minute: $revenue,
        business_impact: $impact,
        demo_event: true,
        sflo_dimensions: {
          "business.application": $application,
          "business.transaction": $transaction,
          "business.capability": $capability,
          "business.criticality": $criticality,
          "sf_service": $service,
          "sf_environment": $environment,
          "service.name": $service
        }
      }
    }'
}

send_event() {
  local action="$1"
  local scenario="$2"
  local curl_args=()
  local url

  url="$(normalize_hec_url "$HEC_URL")"
  if [[ "${SPLUNK_HEC_INSECURE:-false}" == "true" ]]; then
    curl_args+=(-k)
  fi

  build_payload "$action" "$scenario" | curl "${curl_args[@]}" -sS \
    -H "Authorization: Splunk $HEC_TOKEN" \
    -H "Content-Type: application/json" \
    "$url" \
    -d @-

  echo ""
  echo "sent: $action $scenario"
}

main() {
  local action="${1:-}"
  local scenario="${2:-checkout}"

  if [[ -z "$action" || "$action" == "help" || "$action" == "--help" ]]; then
    usage
    exit 0
  fi

  require_env HEC_URL
  require_env HEC_TOKEN

  if ! command -v jq >/dev/null 2>&1; then
    echo "jq is required." >&2
    exit 1
  fi

  if ! command -v curl >/dev/null 2>&1; then
    echo "curl is required." >&2
    exit 1
  fi

  case "$action" in
    print)
      build_payload trigger "$scenario"
      ;;
    trigger|clear)
      send_event "$action" "$scenario"
      ;;
    sequence)
      send_event trigger "$scenario"
      sleep "${DEMO_CLEAR_DELAY_SECONDS:-20}"
      send_event clear "$scenario"
      ;;
    demo)
      send_event trigger checkout
      send_event trigger cart
      send_event trigger catalog
      ;;
    *)
      echo "Unknown action: $action" >&2
      usage >&2
      exit 1
      ;;
  esac
}

main "$@"
