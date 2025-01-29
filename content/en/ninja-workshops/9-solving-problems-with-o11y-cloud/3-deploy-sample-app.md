---
title: Deploy the Sample Application and Instrument with OpenTelemetry
linkTitle: 3. Deploy the Sample Application and Instrument with OpenTelemetry
weight: 3
time: 15 minutes
---

At this point, we've deployed an OpenTelemetry collector in our K8s cluster, and it's
successfully collecting infrastructure metrics.  

The next step is to deploy a sample application and instrument 
with OpenTelemetry to capture traces. 

We'll use a microservices-based application written in Python. To keep the workshop simple, 
we'll focus on two services: a credit check service and a credit processor service.

## Deploy the Application

To save time, we've built Docker images for both of these services already which are available in Docker Hub.
We can deploy the credit check service in our K8s cluster with the following command: 

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl apply -f /home/splunk/workshop/tagging/creditcheckservice-py-with-tags/creditcheckservice-dockerhub.yaml
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
deployment.apps/creditcheckservice created
service/creditcheckservice created
```

{{% /tab %}}
{{< /tabs >}}

Next, let's deploy the credit processor service:

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl apply -f /home/splunk/workshop/tagging/creditprocessorservice/creditprocessorservice-dockerhub.yaml
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
deployment.apps/creditprocessorservice created
service/creditprocessorservice created
```

{{% /tab %}}
{{< /tabs >}}

Finally, let's deploy a load generator to generate traffic: 

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl apply -f /home/splunk/workshop/tagging/loadgenerator/loadgenerator-dockerhub.yaml
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
deployment.apps/loadgenerator created
```

{{% /tab %}}
{{< /tabs >}}

## Explore the Application

We'll provide an overview of the application in this section.  If you'd like to see the complete source 
code for the application, refer to the [Observability Workshop repository in GitHub](https://github.com/splunk/observability-workshop/tree/main/workshop/tagging)

### OpenTelemetry Instrumentation

If we look at the Dockerfile's used to build the credit check and credit processor services, we 
can see that they've already been instrumented with OpenTelemetry.  For example, let's look at 
`/home/splunk/workshop/tagging/creditcheckservice-py-with-tags/Dockerfile`: 

``` dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements over
COPY requirements.txt .

RUN apt-get update && apt-get install --yes gcc python3-dev

ENV PIP_ROOT_USER_ACTION=ignore

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy main app
COPY main.py .

# Bootstrap OTel
RUN splunk-py-trace-bootstrap

# Set the entrypoint command to run the application
CMD ["splunk-py-trace", "python3", "main.py"]
```

We can see that `splunk-py-trace-bootstrap` was included, which installs OpenTelemetry instrumentation
for supported packages used by our applications.  We can also see that `splunk-py-trace` is used as part
of the command to start the application. 

And if we review the `/home/splunk/workshop/tagging/creditcheckservice-py-with-tags/requirements.txt` file, 
we can see that `splunk-opentelemetry[all]` was included in the list of packages. 

Finally, if we review the Kubernetes manifest that we used to deploy this service (`/home/splunk/workshop/tagging/creditcheckservice-py-with-tags/creditcheckservice-dockerhub.yaml`),
we can see that environment variables were set in the container to tell OpenTelemetry 
where to export OTLP data to: 

``` yaml
  env:
    - name: PORT
      value: "8888"
    - name: NODE_IP
      valueFrom:
        fieldRef:
          fieldPath: status.hostIP
    - name: OTEL_EXPORTER_OTLP_ENDPOINT
      value: "http://$(NODE_IP):4317"
    - name: OTEL_SERVICE_NAME
      value: "creditcheckservice"
    - name: OTEL_PROPAGATORS
      value: "tracecontext,baggage"
```

This is all that's needed to instrument the service with OpenTelemetry! 

### Explore the Application 

We've captured several custom tags with our application, which we'll explore shortly. Before we do that, let's
introduce the concept of tags and why they're important. 

### What are tags?

Tags are key-value pairs that provide additional metadata about spans in a trace, allowing you to enrich the context of the spans you send to **Splunk APM**.

For example, a payment processing application would find it helpful to track:

* The payment type used (i.e. credit card, gift card, etc.)
* The ID of the customer that requested the payment

This way, if errors or performance issues occur while processing the payment, we have the context we need for troubleshooting.

While some tags can be added with the OpenTelemetry collector, the ones we’ll be working with in this workshop are more granular, and are added by application developers using the OpenTelemetry SDK.

### Why are tags so important? 

Tags are essential for an application to be truly observable. They add the context to the traces to help us
understand why some users get a great experience and others don't.  And powerful features in
**Splunk Observability Cloud** utilize tags to help you jump quickly to root cause.

> A note about terminology before we proceed. While we discuss **tags** in this workshop,
> and this is the terminology we use in **Splunk Observability Cloud**, OpenTelemetry
> uses the term **attributes** instead. So when you see tags mentioned throughout this
> workshop, you can treat them as synonymous with attributes.

### How are tags captured? 

To capture tags in a Python application, we start by importing the trace module by adding an
import statement to the top of the `/home/splunk/workshop/tagging/creditcheckservice-py-with-tags/main.py` file:

```` python
import requests
from flask import Flask, request
from waitress import serve
from opentelemetry import trace  # <--- ADDED BY WORKSHOP
...
````

Next, we need to get a reference to the current span so we can add an attribute (aka tag) to it:

```` python
def credit_check():
    current_span = trace.get_current_span()  # <--- ADDED BY WORKSHOP
    customerNum = request.args.get('customernum')
    current_span.set_attribute("customer.num", customerNum)  # <--- ADDED BY WORKSHOP
...
````

That was pretty easy, right?  We've captured a total of four tags in the credit check service, with the final result looking like this:

```` python
def credit_check():
    current_span = trace.get_current_span()  # <--- ADDED BY WORKSHOP
    customerNum = request.args.get('customernum')
    current_span.set_attribute("customer.num", customerNum)  # <--- ADDED BY WORKSHOP

    # Get Credit Score
    creditScoreReq = requests.get("http://creditprocessorservice:8899/getScore?customernum=" + customerNum)
    creditScoreReq.raise_for_status()
    creditScore = int(creditScoreReq.text)
    current_span.set_attribute("credit.score", creditScore)  # <--- ADDED BY WORKSHOP

    creditScoreCategory = getCreditCategoryFromScore(creditScore)
    current_span.set_attribute("credit.score.category", creditScoreCategory)  # <--- ADDED BY WORKSHOP

    # Run Credit Check
    creditCheckReq = requests.get("http://creditprocessorservice:8899/runCreditCheck?customernum=" + str(customerNum) + "&score=" + str(creditScore))
    creditCheckReq.raise_for_status()
    checkResult = str(creditCheckReq.text)
    current_span.set_attribute("credit.check.result", checkResult)  # <--- ADDED BY WORKSHOP

    return checkResult
````

## Review Trace Data 

Before looking at the trace data in Splunk Observability Cloud, 
let's review what the debug exporter has captured by tailing the agent collector logs with the following command:

``` bash
kubectl logs -l component=otel-collector-agent -f
```

Hint: use `CTRL+C` to stop tailing the logs. 

You should see traces written to the agent collector logs such as the following:

````
InstrumentationScope opentelemetry.instrumentation.flask 0.44b0
Span #0
    Trace ID       : 9f9fc109903f25ba57bea9b075aa4833
    Parent ID      : 
    ID             : 6d71519f454f6059
    Name           : /check
    Kind           : Server
    Start time     : 2024-12-23 19:55:25.815891965 +0000 UTC
    End time       : 2024-12-23 19:55:27.824664949 +0000 UTC
    Status code    : Unset
    Status message : 
Attributes:
     -> http.method: Str(GET)
     -> http.server_name: Str(waitress.invalid)
     -> http.scheme: Str(http)
     -> net.host.port: Int(8888)
     -> http.host: Str(creditcheckservice:8888)
     -> http.target: Str(/check?customernum=30134241)
     -> net.peer.ip: Str(10.42.0.19)
     -> http.user_agent: Str(python-requests/2.31.0)
     -> net.peer.port: Str(47248)
     -> http.flavor: Str(1.1)
     -> http.route: Str(/check)
     -> customer.num: Str(30134241)
     -> credit.score: Int(443)
     -> credit.score.category: Str(poor)
     -> credit.check.result: Str(OK)
     -> http.status_code: Int(200)
````

Notice how the trace includes the tags (aka attributes) that we captured in the code, such as
`credit.score` and `credit.score.category`.  We'll use these in the next section, when 
we analyze the traces in Splunk Observability Cloud to find the root cause of a performance issue. 
