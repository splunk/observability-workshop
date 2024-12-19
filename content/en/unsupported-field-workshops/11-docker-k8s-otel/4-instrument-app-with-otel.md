---
title: Instrument a .NET Application with OpenTelemetry
linkTitle: 4. Instrument a .NET Application with OpenTelemetry
weight: 4
time: 20 minutes
---

## Download the Splunk Distribution of OpenTelemetry

For this workshop, we'll install the Splunk Distribution of OpenTelemetry manually rather than 
using the NuGet packages.  

We'll start by downloading the latest `splunk-otel-dotnet-install.sh` file, 
which we'll use to instrument our .NET application:

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
curl -sSfL https://github.com/signalfx/splunk-otel-dotnet/releases/latest/download/splunk-otel-dotnet-install.sh -O
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
TBD
```

{{% /tab %}}
{{< /tabs >}}

Refer to [Install the Splunk Distribution of OpenTelemetry .NET manually](https://docs.splunk.com/observability/en/gdi/get-data-in/application/otel-dotnet/instrumentation/instrument-dotnet-application.html#install-the-splunk-distribution-of-opentelemetry-net-manually)
for further details on the installation process.

## Install the Distribution

In the terminal, install the distribution as follows

``` bash
sh ./splunk-otel-dotnet-install.sh
```

> Note: we may need to include the ARCHITECTURE environment when running the command above: 
> ``` bash
> ARCHITECTURE=x64 sh ./splunk-otel-dotnet-install.sh
> ```

## Activate the Instrumentation

Next, we can activate the OpenTelemetry instrumentation: 

``` bash
. $HOME/.splunk-otel-dotnet/instrument.sh
```

## Set the Deployment Environment

Let's set the deployment environment, to ensure our data flows into its own 
environment within Splunk Observability Cloud: 

``` bash 
export OTEL_RESOURCE_ATTRIBUTES='deployment.environment='otel-$INSTANCE'
```

## A Challenge For You 

Before starting our .NET application with the instrumentation, there's a challenge for you. 

How can we see what traces are being exported by the .NET application?  (i.e. on our Linux instance
rather than within Observability Cloud)? 

<details>
  <summary><b>Click here to see the answer</b></summary>

There are two ways we can do this: 

1. We could add `OTEL_TRACES_EXPORTER=otlp,console` at the start of the `dotnet run` command, which ensures that traces are both written to collector via OTLP as well as the console.
``` bash
OTEL_TRACES_EXPORTER=otlp,console dotnet run 
```
2. Alternatively, we could add the debug exporter to the collector configuration, and add it to the traces pipeline, which ensures the traces are written to the collector logs. 

``` yaml
exporters:
  debug:
    verbosity: detailed
service:
  pipelines:
    traces:
      receivers: [jaeger, otlp, zipkin]
      processors:
      - memory_limiter
      - batch
      - resourcedetection
      exporters: [otlphttp, signalfx, debug]
```
</details>


## Run the Application with Instrumentation

We can run the application as follows: 

```
dotnet run
```

Once it's running, use a second SSH terminal and access the application using curl:

``` bash
curl http://localhost:8080/hello
```

As before, it should return `Hello, World!`. 

If you enabled trace logging, you should see a trace written the console or collector logs such as the following: 

````
TODO
````

## View your application in Splunk Observability Cloud

Now that the setup is complete, let's confirm that it's sending data to **Splunk Observability Cloud**.  Note that when the application is deployed for the first time, it may take a few minutes for the data to appear.

Navigate to APM, then use the Environment dropdown to select your environment (i.e. `otel-instancename`).

If everything was deployed correctly, you should see `helloworld` displayed in the list of services:

![APM Overview](../images/apm_overview.png)

Click on **Explore** on the right-hand side to view the service map.  

![Service Map](../images/service_map.png)

Next, click on **Traces** on the right-hand side to see the traces captured for this application. 

![Traces](../images/traces.png)
