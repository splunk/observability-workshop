---
title: Troubleshoot OpenTelemetry Collector Issues
linkTitle: 10. Troubleshoot OpenTelemetry Collector Issues
weight: 10
time: 20 minutes
---

In the previous section, we added the debug exporter to the collector configuration, 
and made it part of the pipeline for traces and logs.  We see the debug output 
written to the agent collector logs as expected.  

However, traces are no longer sent to o11y cloud.  Let's figure out why and fix it. 

## Review the Collector Config 

Whenever a change to the collector config is made via a `values.yaml` file, it's helpful 
to review the actual configuration applied to the collector by looking at the config map: 

``` bash
kubectl describe cm splunk-otel-collector-otel-agent
```

Let's review the pipelines for logs and traces in the agent collector config.  They should look 
like this: 

``` yaml
  pipelines:
    logs:
      exporters:
      - debug
      processors:
      - memory_limiter
      - k8sattributes
      - filter/logs
      - batch
      - resourcedetection
      - resource
      - resource/logs
      - resource/add_environment
      receivers:
      - filelog
      - fluentforward
      - otlp
    ...
    traces:
      exporters:
      - debug
      processors:
      - memory_limiter
      - k8sattributes
      - batch
      - resourcedetection
      - resource
      - resource/add_environment
      receivers:
      - otlp
      - jaeger
      - smartagent/signalfx-forwarder
      - zipkin
```

Do you see the problem?  Only the debug exporter is included in the traces and logs pipelines. 
The `otlphttp` and `signalfx` exporters that were present in the traces pipeline configuration previously are gone.
This is why we no longer see traces in o11y cloud.  And for the logs pipeline, the `splunk_hec/platform_logs` 
exporter has been removed. 

> How did we know what specific exporters were included before?  To find out,
> we could have reverted our earlier customizations and then checked the config
> map to see what was in the traces pipeline originally.  Alternatively, we can refer
> to the examples in the [GitHub repo for splunk-otel-collector-chart](https://github.com/signalfx/splunk-otel-collector-chart/blob/main/examples/default/rendered_manifests/configmap-agent.yaml)
> which shows us what default agent config is used by the Helm chart.

## How did these exporters get removed?

Let's review the customizations we added to the `values.yaml` file: 

``` yaml
logsEngine: otel
splunkObservability:
  infrastructureMonitoringEventsEnabled: true
agent:
  config:
    receivers:
     ...
    exporters:
      debug:
        verbosity: detailed
    service:
      pipelines:
        traces:
          exporters:
            - debug
        logs:
          exporters:
            - debug
```

When we applied the `values.yaml` file to the collector using `helm upgrade`, the 
custom configuration got merged with the previous collector configuration. 
When this happens, the sections of the `yaml` configuration that contain lists, 
such as the list of exporters in the pipeline section, get replaced with what we 
included in the `values.yaml` file (which was only the debug exporter). 

## Let's Fix the Issue

So when customizing an existing pipeline, we need to fully redefine that part of the configuration. 
Our `values.yaml` file should thus be updated as follows: 

``` yaml
logsEngine: otel
splunkObservability:
  infrastructureMonitoringEventsEnabled: true
agent:
  config:
    receivers:
     ...
    exporters:
      debug:
        verbosity: detailed
    service:
      pipelines:
        traces:
          exporters:
            - otlphttp
            - signalfx
            - debug
        logs:
          exporters:
            - splunk_hec/platform_logs
            - debug
```

Let's apply the changes:

``` bash
helm upgrade splunk-otel-collector \
  --set="splunkObservability.realm=$REALM" \
  --set="splunkObservability.accessToken=$ACCESS_TOKEN" \
  --set="clusterName=$INSTANCE-cluster" \
  --set="environment=otel-$INSTANCE" \
  --set="splunkPlatform.token=$HEC_TOKEN" \
  --set="splunkPlatform.endpoint=$HEC_URL" \
  --set="splunkPlatform.index=splunk4rookies-workshop" \
  -f values.yaml \
splunk-otel-collector-chart/splunk-otel-collector
```

And then check the agent config map: 

``` bash
kubectl describe cm splunk-otel-collector-otel-agent
```

This time, we should see a fully defined exporters pipeline for both logs and traces: 

``` bash
  pipelines:
    logs:
      exporters:
      - splunk_hec/platform_logs
      - debug
      processors:
      ...
    traces:
      exporters:
      - otlphttp
      - signalfx
      - debug
      processors:
      ...
```

## Reviewing the Log Output

The **Splunk Distribution of OpenTelemetry .NET** automatically exports logs enriched with tracing context 
from applications that use `Microsoft.Extensions.Logging` for logging (which our sample app does). 

Application logs are enriched with tracing metadata and then exported to a local instance of 
the OpenTelemetry Collector in OTLP format.

Let's take a closer look at the logs that were captured by the debug exporter to see if that's happening.  
To tail the collector logs, we can use the following command: 

``` bash
kubectl logs -l component=otel-collector-agent -f
```

Once we're tailing the logs, we can use curl to generate some more traffic.  Then we should see 
something like the following: 

````
2024-12-20T21:56:30.858Z	info	Logs	{"kind": "exporter", "data_type": "logs", "name": "debug", "resource logs": 1, "log records": 1}
2024-12-20T21:56:30.858Z	info	ResourceLog #0
Resource SchemaURL: https://opentelemetry.io/schemas/1.6.1
Resource attributes:
     -> splunk.distro.version: Str(1.8.0)
     -> telemetry.distro.name: Str(splunk-otel-dotnet)
     -> telemetry.distro.version: Str(1.8.0)
     -> os.type: Str(linux)
     -> os.description: Str(Debian GNU/Linux 12 (bookworm))
     -> os.build_id: Str(6.8.0-1021-aws)
     -> os.name: Str(Debian GNU/Linux)
     -> os.version: Str(12)
     -> host.name: Str(derek-1)
     -> process.owner: Str(app)
     -> process.pid: Int(1)
     -> process.runtime.description: Str(.NET 8.0.11)
     -> process.runtime.name: Str(.NET)
     -> process.runtime.version: Str(8.0.11)
     -> container.id: Str(5bee5b8f56f4b29f230ffdd183d0367c050872fefd9049822c1ab2aa662ba242)
     -> telemetry.sdk.name: Str(opentelemetry)
     -> telemetry.sdk.language: Str(dotnet)
     -> telemetry.sdk.version: Str(1.9.0)
     -> service.name: Str(helloworld)
     -> deployment.environment: Str(otel-derek-1)
     -> k8s.node.name: Str(derek-1)
     -> k8s.cluster.name: Str(derek-1-cluster)
ScopeLogs #0
ScopeLogs SchemaURL: 
InstrumentationScope HelloWorldController 
LogRecord #0
ObservedTimestamp: 2024-12-20 21:56:28.486804 +0000 UTC
Timestamp: 2024-12-20 21:56:28.486804 +0000 UTC
SeverityText: Information
SeverityNumber: Info(9)
Body: Str(/hello endpoint invoked by {name})
Attributes:
     -> name: Str(Kubernetes)
Trace ID: 78db97a12b942c0252d7438d6b045447
Span ID: 5e9158aa42f96db3
Flags: 1
	{"kind": "exporter", "data_type": "logs", "name": "debug"}
````

In this example, we can see that the Trace ID and Span ID were automatically written to the log output
by the OpenTelemetry .NET instrumentation.  This allows us to correlate logs with traces in 
Splunk Observability Cloud. 

You might remember though that if we deploy the OpenTelemetry collector in a K8s cluster using Helm, 
and we include the log collection option, then the OpenTelemetry collector will use the File Log receiver 
to automatically capture any container logs.  

This would result in duplicate logs being captured for our application.  For example, in the following screenshot we 
can see two log entries for each request made to our service: 

![Duplicate Log Entries](../images/duplicate_logs.png)

How do we avoid this? 

## Avoiding Duplicate Logs in K8s 

To avoid capturing duplicate logs, we have one of two options: 

1. We can set the `OTEL_LOGS_EXPORTER` environment variable to `none`, to tell the Splunk Distribution of OpenTelemetry .NET to avoid exporting logs to the collector using OTLP. 
2. We can manage log ingestion using annotations. 

### Option 1 

Setting the `OTEL_LOGS_EXPORTER` environment variable to `none` is straightforward. However, the Trace ID and Span ID are not written to the stdout logs generated by the application,
which would prevent us from correlating logs with traces. 

To resolve this, we could define a custom logger, such as the example defined in  
`/home/splunk/workshop/docker-k8s-otel/helloworld/SplunkTelemetryConfigurator.cs`. 

We could include this in our application by updating the `Program.cs` file as follows: 

``` cs
using SplunkTelemetry;
using Microsoft.Extensions.Logging.Console;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();

SplunkTelemetryConfigurator.ConfigureLogger(builder.Logging);

var app = builder.Build();

app.MapControllers();

app.Run();
```

### Option 2

Option 2 requires updating the deployment manifest for the application 
to include an annotation.  In our case, we would edit the `deployment.yaml` file to add the 
`splunk.com/exclude` annotation as follows: 

``` yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: helloworld
spec:
  selector:
    matchLabels:
      app: helloworld
  replicas: 1
  template:
    metadata:
      labels:
        app: helloworld
      annotations:
        splunk.com/exclude: "true"
    spec:
      containers:
      ...  
```

Please refer to [Managing Log Ingestion by Using Annotations](https://docs.splunk.com/observability/en/gdi/opentelemetry/collector-kubernetes/kubernetes-config-logs.html#manage-log-ingestion-using-annotations) 
for further details on this option. 