---
title: Setup Users
linkTitle: 6. Setup Users
weight: 6
time: 2 minutes
---

In this section, we'll create users for each workshop participant, with a namespace and resource 
quota for each. 

## Create User Namespaces and Resource Quotas

``` bash
cd user-setup
./create-namespaces.sh
```

## Create Users

Create an HTPasswd file with participant credentials, then replace 
the ROSA-managed HTPasswd IdP with a custom one:

``` bash
./create-users.sh
```

## Re-create the cluster-admin user then login again

Re-create the cluster-admin user then login again:

``` bash
rosa create admin -c rosa-test
oc login <Cluster API URL> --username cluster-admin --password <cluster admin password>
```

## Add Role to Users

Grant each user access to their namespace only:

``` bash
./add-role-to-users.sh
```


## Test Login

### Install the OpenShift CLI

To test the logins from our local machine, we'll need to install the OpenShift CLI. 

For MacOS, we can install the OpenShift CLI using the Homebrew package manager: 

``` bash
brew install openshift-cli
```

For other installation options, please revfr to the [OpenShift documentation](https://docs.redhat.com/en/documentation/openshift_container_platform/4.8/html/cli_tools/openshift-cli-oc). 

### Login as Workshop User 

Try logging in as one of the workshop users from your local machine: 

``` bash
oc login https://api.<cluster-domain>:443 -u participant1 -p 'TempPass123!'
```

It should say something like: 

````
Login successful.

You have one project on this server: "workshop-participant-1"
````

### Confirm Access to the LLM 

Let's ensure we can access the LLM from the workshop user account. 

Start a pod that has access to the curl command:

``` bash
oc run --rm -it curl --image=curlimages/curl:latest -- sh
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