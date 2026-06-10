# GitHub And Splunk References

## Goal

Use these references when you want to understand where the lab patterns came from or when you need the authoritative syntax behind a collector or instrumentation setting.

## Collector References

| Reference | Use it for |
| --- | --- |
| [Splunk OpenTelemetry Collector](https://github.com/signalfx/splunk-otel-collector) | Splunk distribution of the OpenTelemetry Collector, supported components, releases, and base behavior |
| [Splunk OpenTelemetry Collector Helm chart](https://github.com/signalfx/splunk-otel-collector-chart) | Kubernetes Helm values, chart configuration, install and upgrade patterns |
| [Splunk OpenTelemetry examples: Cisco AI-ready PODs](https://github.com/signalfx/splunk-opentelemetry-examples/tree/main/collector/cisco-ai-ready-pods) | Cisco AI POD-style collector examples and metric allowlist patterns |
| [Cisco AI-ready PODs collector values](https://github.com/signalfx/splunk-opentelemetry-examples/blob/main/collector/cisco-ai-ready-pods/otel-collector/values.yaml) | Prometheus receivers, NVIDIA/NIM scrape examples, and dashboard-oriented metric filtering |
| [OpenTelemetry Collector contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) | Upstream receiver, processor, and exporter implementation details |
| [Prometheus receiver](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/prometheusreceiver) | Collector-side Prometheus scraping for DCGM and NIM endpoints |
| [Filter processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/filterprocessor) | Metric allowlists and drops used to control duplicate lab ingest |

## AI Agent Monitoring References

| Reference | Use it for |
| --- | --- |
| [Set up Splunk AI Agent Monitoring](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-agent-monitoring/set-up-ai-agent-monitoring) | Product setup flow and required telemetry path |
| [Zero-code instrumentation](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-agent-monitoring/set-up-ai-agent-monitoring/zero-code-instrumentation) | Running Python agent apps with `opentelemetry-instrument` |
| [Configure the Python agent for AI applications](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-agent-monitoring/configure-ai-agent-monitoring/configure-the-python-agent-for-ai-applications-0.1.14-and-higher) | GenAI environment variables, prompt capture settings, and Python agent behavior |
| [Splunk OpenTelemetry Python](https://github.com/signalfx/splunk-otel-python) | Splunk Python distribution package and release context |
| [OpenTelemetry Python GenAI instrumentation](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation-genai) | Source for GenAI instrumentation packages used by agent frameworks |
| [splunk-otel-instrumentation-openai-agents on PyPI](https://pypi.org/project/splunk-otel-instrumentation-openai-agents/) | OpenAI Agents SDK instrumentation package behavior and package requirements |

## Cisco AI POD And GPU References

| Reference | Use it for |
| --- | --- |
| [Cisco AI PODs data sheet](https://www.cisco.com/c/en/us/products/collateral/servers-unified-computing/ucs-x-series-modular-system/ai-pods-ds.html) | Product-level Cisco AI POD platform description |
| [Cisco AI POD for Enterprise Training and Fine-Tuning Design Guide](https://www.cisco.com/c/en/us/td/docs/unified_computing/ucs/UCS_CVDs/cisco_ai_pod_for_training_design.html) | Production hardware architecture, scale unit, compute, and fabric design context |
| [AI Defense on Cisco AI PODs Reference Architecture](https://www.cisco.com/c/en/us/td/docs/unified_computing/ucs/UCS_CVDs/AI_defense_on_Cisco_AI_PODs_reference_architecture.html) | Reference architecture context for AI POD deployment patterns |
| [Monitor Cisco AI PODs](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-infrastructure-monitoring/set-up-ai-infrastructure-monitoring/cisco-ai-pods) | Supported Cisco AI POD components and setup sequence |
| [Monitor the performance of Cisco AI PODs](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-infrastructure-monitoring/monitor-and-troubleshoot-your-ai-infrastructure/monitor-the-performance-of-cisco-ai-pods) | Built-in dashboard and AI POD monitoring workflow |
| [Splunk Cisco AI Pods workshop](https://splunk.github.io/observability-workshop/en/ninja-workshops/14-cisco-ai-pods/) | Public workshop pattern for participant collectors, Prometheus scraping, and dashboard review |
| [Cisco AI POD GitHub repository](https://github.com/ucs-compute-solutions/Cisco-AI-POD) | Cisco AI POD reference architecture material |
| [Appendix: AI POD Hardware Docs](appendix-ai-pod-hardware.md) | Student-facing hardware doc links and explanation |

## How These References Map To This Lab

| Lab area | Primary references |
| --- | --- |
| Student collector deployment | Splunk collector Helm chart, Splunk collector GitHub |
| Collector config file changes | Splunk collector examples, Prometheus receiver, filter processor |
| App instrumentation | Splunk AI Agent Monitoring docs, Splunk Python distribution, GenAI instrumentation source |
| Agent trace review | Splunk AI Agent Monitoring setup and Python configuration docs |
| GPU and NIM scraping | Cisco AI POD examples, Prometheus receiver, Cisco AI POD setup docs |
| AI POD-style drilldown | Cisco AI POD performance docs and Splunk Cisco AI Pods workshop |

!!! note "Lab To Production"
    This workshop uses app telemetry, AI agent traces, token metrics, NIM metrics, GPU metrics, Kubernetes health, and Splunk dashboards to practice the Cisco AI POD monitoring workflow. A full Cisco AI POD observability deployment can extend the same investigation path with UCS, Nexus, storage, vector database, Intersight, Nexus Dashboard, and AI Defense telemetry.
