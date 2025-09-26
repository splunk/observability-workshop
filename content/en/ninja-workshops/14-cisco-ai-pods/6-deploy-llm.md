---
title: Deploy an LLM
linkTitle: 6. Deploy an LLM
weight: 6
time: 20 minutes
---

In this section, we'll use the NVIDIA NIM Operator to deploy a Large Language Model 
to our OpenShift Cluster. 

## Create a Namespace

``` bash
oc create namespace nim-service
```

## Add Secrets with NGC API Key

Add a Docker registry secret for downloading container images from NVIDIA NGC:

``` bash
oc create secret -n nim-service docker-registry ngc-secret \
    --docker-server=nvcr.io \
    --docker-username='$oauthtoken' \
    --docker-password=$NGC_API_KEY
```

Add a generic secret that model puller containers use to download the model from NVIDIA NGC:

``` bash
oc create secret -n nim-service generic ngc-api-secret \
    --from-literal=NGC_API_KEY=$NGC_API_KEY
```

## Deploy an LLM

Run the following command to create the NIMCache and NIMService: 

``` bash
oc apply -n nim-service -f nvidia-llm.yaml
```

Confirm that the Persistent Volume was created and the Persistent Volume Claim 
was bound to is successfully: 

> Note: this can take several minutes to occur 

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
oc get pv,pvc -n nim-service
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
NAME                                                        CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                                                   STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
persistentvolume/pvc-1af12c04-29ad-497f-b018-7d9a3aea3019   100Gi      RWO            Delete           Bound    openshift-monitoring/prometheus-data-prometheus-k8s-1   gp3-csi        <unset>                          4h15m
persistentvolume/pvc-9c389d79-13fb-4169-9d99-a77efd6e7919   100Gi      RWO            Delete           Bound    openshift-monitoring/prometheus-data-prometheus-k8s-0   gp3-csi        <unset>                          4h15m
persistentvolume/pvc-a603b8a7-1445-4b03-945a-3ed68338834c   50Gi       RWO            Delete           Bound    nim-service/meta-llama-3-2-1b-instruct-pvc              gp3-csi        <unset>                          114s

NAME                                                   STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
persistentvolumeclaim/meta-llama-3-2-1b-instruct-pvc   Bound    pvc-a603b8a7-1445-4b03-945a-3ed68338834c   50Gi       RWO            gp3-csi        <unset>                 7m8s
```

{{% /tab %}}
{{< /tabs >}}

Confirm that the NIMCache is Ready: 

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
oc get nimcache.apps.nvidia.com -n nim-service
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
NAME                         STATUS   PVC                              AGE
meta-llama-3-2-1b-instruct   Ready    meta-llama-3-2-1b-instruct-pvc   9m50s
```

{{% /tab %}}
{{< /tabs >}}

Confirm that the NIMService is Ready:

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
oc get nimservices.apps.nvidia.com -n nim-service
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
NAME                         STATUS   AGE
meta-llama-3-2-1b-instruct   Ready    11m
```

{{% /tab %}}
{{< /tabs >}}

## Test the LLM 

Let's ensure the LLM is working as expected. 

Start a pod that has access to the curl command: 

``` bash
oc run --rm -it -n default curl --image=curlimages/curl:latest -- sh
```

Then run the following command to send a prompt to the LLM: 

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
curl -X "POST" \
 'http://meta-llama-3-2-1b-instruct.nim-service:8000/v1/chat/completions' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
        "model": "meta/llama-3.2-1b-instruct",
        "messages": [
        {
          "content":"What is the capital of Canada?",
          "role": "user"
        }],
        "top_p": 1,
        "n": 1,
        "max_tokens": 1024,
        "stream": false,
        "frequency_penalty": 0.0,
        "stop": ["STOP"]
      }'
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
{
  "id": "chatcmpl-2ccfcd75a0214518aab0ef0375f8ca21",
  "object": "chat.completion",
  "created": 1758919002,
  "model": "meta/llama-3.2-1b-instruct",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "reasoning_content": null,
        "content": "The capital of Canada is Ottawa.",
        "tool_calls": []
      },
      "logprobs": null,
      "finish_reason": "stop",
      "stop_reason": null
    }
  ],
  "usage": {
    "prompt_tokens": 42,
    "total_tokens": 50,
    "completion_tokens": 8,
    "prompt_tokens_details": null
  },
  "prompt_logprobs": null
}
```

{{% /tab %}}
{{< /tabs >}}