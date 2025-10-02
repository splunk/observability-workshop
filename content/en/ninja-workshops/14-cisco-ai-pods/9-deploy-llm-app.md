---
title: Deploy the LLM Application
linkTitle: 9. Deploy the LLM Application
weight: 9
time: 10 minutes
---

In the final step of the workshop, we'll deploy an application to our Cisco AI POD 
that uses the instruct and embeddings models that we deployed earlier using the 
NVIDIA NIM operator. 

## Deploy the LLM Application

Let's deploy an application to our OpenShift cluster that answers questions 
using the context that we loaded into the Weaviate vector database earlier. 

``` bash
oc apply -f ./llm-app/k8s-manifest.yaml
```

> Note: to build a Docker image for this Python application, we executed the following commands:
> ``` bash
> cd workshop/cisco-ai-pods/llm-app
> docker build --platform linux/amd64 -t derekmitchell399/llm-app:1.0 .
> docker push derekmitchell399/llm-app:1.0
> ```

## Test the LLM Application

Let's ensure the application is working as expected.

Start a pod that has access to the curl command:

``` bash
oc run --rm -it -n default curl --image=curlimages/curl:latest -- sh
```

Then run the following command to send a question to the LLM:

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
curl -X "POST" \
 'http://llm-app.llm-app.svc.cluster.local:8080/askquestion' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "question": "How much memory does the NVIDIA H200 have?"
  }'
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
The NVIDIA H200 has 141GB of HBM3e memory, which is twice the capacity of the NVIDIA H100 Tensor Core GPU with 1.4X more memory bandwidth.
```

{{% /tab %}}
{{< /tabs >}}

## View Trace Data in Splunk Observability Cloud

In Splunk Observability Cloud, navigate to `APM` and then select `Service Map`. 
Ensure the `llm-app` environment is selected.  You should see a service map 
that looks like the following: 

![Service Map](../images/ServiceMap.png)

Click on `Traces` on the right-hand side menu.  Then select one of the slower running 
traces. It should look like the following example: 

![Trace](../images/Trace.png)

The trace shows all the interactions that our application executed to return an answer 
to the users question (i.e. "How much memory does the NVIDIA H200 have?")

For example, we can see where our application performed a similarity search to look 
for documents related to the question at hand in the Weaviate vector database: 

![Document Retrieval](../images/DocumentRetrieval.png)

We can also see how the application created a prompt to send to the LLM, including the 
context that was retrieved from the vector database: 

![Prompt Template](../images/PromptTemplate.png)

Finally, we can see the response from the LLM, the time it took, and the number of 
input and output tokens utilized: 

![LLM Response](../images/LLMResponse.png)

## Wrap-Up 

We hope you enjoyed this workshop, which provided hands-on experience deploying and working 
with several of the technologies that are used to monitor Cisco AI PODs with 
Splunk Observability Cloud. Specifically, you had the opportunity to: 

* Deploy a RedHat OpenShift cluster with GPU-based worker nodes. 
* Deploy the NVIDIA NIM Operator and NVIDIA GPU Operator. 
* Deploy Large Language Models (LLMs) using NVIDIA NIM to the cluster. 
* Deploy the OpenTelemetry Collector in the Red Hat OpenShift cluster.
* Add Prometheus receivers to the collector to ingest infrastructure metrics.
* Deploy the Weaviate vector database to the cluster. 
* Instrument Python services that interact with Large Language Models (LLMs) with OpenTelemetry. 
* Understand which details which OpenTelemetry captures in the trace from applications that interact with LLMs. 
