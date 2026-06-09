# AI Tokenomics and GPU Chargeback Workshop Assets

These files support the workshop at:

```text
content/en/ninja-workshops/ai/14-ai-tokenomics-chargeback
```

The assets are intentionally small. They show the telemetry contract and local
throughput benchmark needed for chargeback without requiring a Kubernetes cluster.
The Cisco AI Pods path remains useful when you have shared GPU infrastructure
telemetry.

## Files

* `instrumentation/tokenomics_instrumentation.py` - Python helper for custom
  OpenTelemetry token and cost metrics.
* `k8s/llm-app-chargeback-patch.yaml` - Kubernetes patch that adds default owner
  metadata to the sample `llm-app` deployment.
* `collector/otel-collector-chargeback-values.yaml` - Collector processor additions
  and metric allowlist examples for chargeback dimensions.
* `dashboards/signalflow-examples.md` - SignalFlow snippets for dashboards and
  detectors.
* `rate-card-example.yaml` - Public-source-backed workshop rate card examples for
  token and GPU-hour pricing.
* `scripts/benchmark_ollama.py` - Local Ollama benchmark that derives input, output,
  and blended token rates from observed throughput and an hourly cost model.

## Recommended Flow

### Local Model Path

1. Install Ollama and pull a small model, for example `ollama pull llama3.2:1b`.
2. Run `scripts/benchmark_ollama.py` against the local model.
3. Choose an hourly cost model: market proxy, hardware amortization, or energy-only.
4. Use the derived token rates as the workshop rate card.
5. Add the custom instrumentation helper to a local app or use the benchmark output as
   sample chargeback data.

### Shared GPU Path

1. Deploy the Cisco AI Pods workshop collector and LLM application.
2. Confirm DCGM, NIM, Kubernetes, and APM data in Splunk Observability Cloud.
3. Add the attribution defaults from `k8s/llm-app-chargeback-patch.yaml`.
4. Add the custom instrumentation helper to the application.
5. If your collector has custom filters, merge the chargeback metric names from
   `collector/otel-collector-chargeback-values.yaml`.
6. Confirm the `ai.tokens.*`, `ai.request.count`, and
   `ai.request.estimated_cost_usd` metrics in Metric Finder.
7. Build dashboards and detectors with the SignalFlow examples.

The rate card values in these files are fictional workshop values. Replace them with an
approved internal rate card before using the pattern for production chargeback.
