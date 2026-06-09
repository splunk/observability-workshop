---
title: 2. Review Out-of-the-Box AI Monitoring
weight: 2
---

Start with the telemetry Splunk Observability Cloud can already use. The goal is to
avoid custom instrumentation for signals that already exist, and to identify exactly
where custom attribution is required.

## Built-In Data Sources

The Cisco AI Pods collector examples already scrape key GPU and NIM metrics through
Prometheus receivers. The important metric groups for this workshop are:

* **GPU utilization and capacity** - `DCGM_FI_DEV_GPU_UTIL`, `DCGM_FI_DEV_FB_USED`,
  `DCGM_FI_DEV_FB_FREE`, `DCGM_FI_PROF_GR_ENGINE_ACTIVE`, and
  `DCGM_FI_PROF_PIPE_TENSOR_ACTIVE`.
* **GPU power and energy** - `DCGM_FI_DEV_POWER_USAGE` and
  `DCGM_FI_DEV_TOTAL_ENERGY_CONSUMPTION`.
* **NIM request and token metrics** - `prompt_tokens_total`,
  `generation_tokens_total`, `request_prompt_tokens`, `request_generation_tokens`,
  `time_to_first_token_seconds`, and `time_per_output_token_seconds`.
* **Kubernetes placement** - namespace, pod, container, node, and cluster dimensions.
* **APM and AI traces** - spans that show LLM calls, model names, prompts, responses,
  latency, and token details when AI instrumentation is enabled.

{{% notice title="Exercise" style="green" icon="running" %}}

Open the built-in views that already describe your AI stack:

1. Go to **Dashboards** and search for `Cisco AI PODs Dashboard`.
2. Filter the dashboard to your `k8s.cluster.name`.
3. Review the **AI POD Overview** and **NIM FOR LLMS** tabs.
4. Go to **Infrastructure** and review the Kubernetes or OpenShift view for the same
   cluster.
5. Go to **APM** and open the service map for the AI application.
6. Open a trace that includes an LLM request and confirm that model, token, and latency
   details are visible.

<!-- TODO screenshot: Cisco AI PODs Dashboard filtered to the workshop cluster, showing GPU utilization and NIM token charts. -->
![Cisco AI POD dashboard filtered to a cluster](images/cisco-ai-pod-dashboard-chargeback.png)

<!-- TODO screenshot: Trace details for an LLM request showing model, prompt tokens, completion tokens, and latency. -->
![LLM trace details with token usage](images/llm-trace-token-details.png)

{{% /notice %}}

## Identify the Gap

Out-of-the-box monitoring answers operational questions:

* Are GPUs healthy and utilized?
* Is the NIM model serving requests?
* Which services call the model?
* How many tokens were processed?
* Which traces are slow or failing?

Chargeback adds business questions:

* Which tenant, team, product, or cost center drove the tokens?
* Which workload consumed shared GPU capacity?
* What did each request cost under the current rate card?
* Which model choice changed cost per successful answer?
* Which team is burning budget faster than expected?

Those business questions require custom attributes and metrics from the application.
