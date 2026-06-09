#!/usr/bin/env bash
set -euo pipefail

APP_NAMESPACE="${APP_NAMESPACE:-otel-demo}"
SCENARIO="${1:-}"

usage() {
  cat <<'EOF'
Usage:
  ./scripts/set-flag.sh <scenario>

Scenarios:
  healthy          Clear workshop failure flags
  checkout         Fail payment requests for checkout impact
  cart             Fail cart service
  catalog          Fail product catalog service
  recommendation   Fail recommendation cache
  flood            Increase frontend request load
  image-slow       Slow frontend image loading
EOF
}

if [[ -z "$SCENARIO" || "$SCENARIO" == "help" || "$SCENARIO" == "--help" ]]; then
  usage
  exit 0
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "jq is required to update the flagd ConfigMap." >&2
  exit 1
fi

tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT
flag_file="$tmp_dir/demo.flagd.json"

kubectl -n "$APP_NAMESPACE" get configmap flagd-config -o jsonpath='{.data.demo\.flagd\.json}' > "$flag_file"

reset_filter='
  .flags.productCatalogFailure.defaultVariant = "off" |
  .flags.recommendationCacheFailure.defaultVariant = "off" |
  .flags.cartFailure.defaultVariant = "off" |
  .flags.paymentFailure.defaultVariant = "off" |
  .flags.paymentUnreachable.defaultVariant = "off" |
  .flags.loadGeneratorFloodHomepage.defaultVariant = "off" |
  .flags.imageSlowLoad.defaultVariant = "off" |
  .flags.failedReadinessProbe.defaultVariant = "off" |
  .flags.emailMemoryLeak.defaultVariant = "off"
'

flag_name=""
variant=""

case "$SCENARIO" in
  healthy)
    jq "$reset_filter" "$flag_file" > "$flag_file.next"
    ;;
  checkout|payment)
    flag_name="paymentFailure"
    variant="100%"
    ;;
  cart)
    flag_name="cartFailure"
    variant="on"
    ;;
  catalog|product-catalog)
    flag_name="productCatalogFailure"
    variant="on"
    ;;
  recommendation)
    flag_name="recommendationCacheFailure"
    variant="on"
    ;;
  flood)
    flag_name="loadGeneratorFloodHomepage"
    variant="on"
    ;;
  image-slow)
    flag_name="imageSlowLoad"
    variant="5sec"
    ;;
  *)
    echo "Unknown scenario: $SCENARIO" >&2
    usage >&2
    exit 1
    ;;
esac

if [[ "$SCENARIO" != "healthy" ]]; then
  jq -e --arg flag "$flag_name" '.flags[$flag]' "$flag_file" >/dev/null
  jq --arg flag "$flag_name" --arg variant "$variant" \
    "$reset_filter | .flags[\$flag].defaultVariant = \$variant" \
    "$flag_file" > "$flag_file.next"
fi

mv "$flag_file.next" "$flag_file"

patch_payload="$(jq -Rs '{data: {"demo.flagd.json": .}}' < "$flag_file")"
kubectl -n "$APP_NAMESPACE" patch configmap flagd-config --type merge -p "$patch_payload"
kubectl -n "$APP_NAMESPACE" rollout restart deployment/flagd
kubectl -n "$APP_NAMESPACE" rollout status deployment/flagd --timeout=2m

echo "Scenario set: $SCENARIO"
if [[ "$SCENARIO" == "healthy" ]]; then
  echo "All workshop failure flags are off."
else
  echo "$flag_name defaultVariant=$variant"
fi
