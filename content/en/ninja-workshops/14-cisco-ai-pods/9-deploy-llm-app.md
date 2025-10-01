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
cd workshop/cisco-ai-pods/llm-app
oc apply -f k8s-manifest.yaml
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
The NVIDIA H200 graphics card has 5536 MB of GDDR6 memory.
```

{{% /tab %}}
{{< /tabs >}}

## View Trace Data in Splunk Observability Cloud

In Splunk Observability Cloud, navigate to `APM` and then select `Service Map`. 
Ensure the `llm-app` environment is selected.  You should see a service map 
that looks like the following: 

Click on `Traces` on the right-hand side menu.  Then select one of the slower running 
traces. 


