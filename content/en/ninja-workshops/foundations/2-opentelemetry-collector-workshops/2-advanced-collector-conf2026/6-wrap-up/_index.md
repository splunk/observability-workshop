---
title: 6. Wrap-up and Take-home Exercises
linkTitle: 6. Take-home Exercises
weight: 9
time: 3 minutes
---

![Well done](../images/welldone.png)

You started with Splunk Distribution's default Agent pipelines, validated
telemetry locally, used Config Builder to add filtering, sensitive-data
controls, and log transformation, and deployed the completed configuration.

## Continue learning

1. **Send logs to a non-production Splunk instance.** Create a HEC token and
   endpoint in your own Splunk Enterprise or Splunk Cloud Platform lab, update
   `SPLUNK_HEC_TOKEN` and `SPLUNK_HEC_URL`, and validate the `splunk_hec`
   exporter. Start with Splunk's
   [Collector-to-Splunk configuration guide](https://help.splunk.com/en/splunk-observability-cloud/manage-data/splunk-distribution-of-the-opentelemetry-collector/get-started-with-the-splunk-distribution-of-the-opentelemetry-collector/get-started-understand-and-use-the-collector/use-the-collector-to-send-container-logs-to-splunk-enterprise/part-2-configure-the-collector-and-splunk-enterprise-instance).
   Do not send workshop data or credentials to a production instance.

2. **Deploy Collectors at scale.** Replace one-host manual setup with Splunk's
   supported Ansible collection. Follow
   [Deploy the Collector for Linux with Ansible](https://help.splunk.com/en/splunk-observability-cloud/manage-data/splunk-distribution-of-the-opentelemetry-collector/get-started-with-the-splunk-distribution-of-the-opentelemetry-collector/collector-for-linux/install-the-collector-for-linux-tools/ansible-for-linux).

3. **Try zero-code discovery and instrumentation.** Continue with the
   [Automatic Discovery workshops](/en/ninja-workshops/foundations/1-automatic-discovery/)
   and the
   [Zero-Code APM with OBI and eBPF workshop](/en/ninja-workshops/instrumentation/4-obi-ebpf/).

4. **Adopt OpenTelemetry from AppDynamics.** Use the
   [AppDynamics Dual Ingest workshop](/en/ninja-workshops/appdynamics/2-appd-ingest/)
   to send OpenTelemetry traces from an AppDynamics-instrumented application to
   Splunk Observability Cloud and build navigation between the platforms.

5. **Explore Always-On Profiling.** Work through the
   [profiling section of Debug Problems in Microservices](/en/scenarios/debug-problems/profiling/)
   to enable CPU and memory profiling and investigate application code with
   call stacks and flame graphs.

{{% notice title="Keep your Config Builder result" style="note" %}}
Save the final downloaded `agent_config.yaml` without secrets. It is a useful
starting point for these exercises, but review component support, credentials,
network exposure, and processor ordering before treating a workshop config as
production configuration.
{{% /notice %}}
