---
title: Add the Splunk Agent Observability SDK and Configuration
linkTitle: 1. Add the Splunk Agent Observability SDK
weight: 1
time: 3 minutes
---


First, add the Splunk Agent Observability SDK to the Python application. Then, add configuration
so that the SDK knows *where* to send traces.

{{< exercise title="Add the SDK and configuration" >}}

{{< step title="Add the Splunk Agent Observability package" >}}

If you open the `~/workshop/healthcare-assistant/2-app-with-instrumentation/requirements.txt` 
file, you'll see that this package has already been added: 

````
splunk-ao
````

{{< /step >}}

{{< step title="Set the Participant Number Environment Variable" >}}

Run the following command to set the `PARTICIPANT_NUMBER` environment variable 
on your EC2 instance: 

> **Be sure to add the participant number assigned to you in the sign-up sheet before
> running the following command**

````
export PARTICIPANT_NUMBER=<your participant number>  
````

{{< /step >}}

{{< step title="Create a Kubernetes Secret" >}}

Run the following command to create a Kubernetes secret, which stores the Splunk Agent Observability API key: 

```bash
kubectl create secret generic splunk-ao-secret \
  --from-literal=SPLUNK_AO_API_KEY="$GALILEO_API_KEY"
```

> If you're using Splunk Agent Observability within Splunk Observability Cloud for this workshop, 
> please use the following command instead: 
> ```bash 
> kubectl create secret generic splunk-ao-secret \
> --from-literal=SPLUNK_AO_O11Y_TOKEN="$ACCESS_TOKEN"
> ```

{{< /step >}}

{{< step title="Create a Config Map" >}}

Run the following command to create a Kubernetes config map, which the application will use to
determine how to send traces to Splunk Agent Observability: 

```bash
kubectl create configmap splunk-ao-config \
  --from-literal=SPLUNK_AO_CONSOLE_URL="$GALILEO_CONSOLE_URL" \
  --from-literal=SPLUNK_AO_PROJECT="project-$PARTICIPANT_NUMBER" \
  --from-literal=SPLUNK_AO_AGENT_STREAM="default"
```

> If you're using Splunk Agent Observability within Splunk Observability Cloud for this workshop,
> please use the following command instead:
> ```bash 
> kubectl create configmap splunk-ao-config \
> --from-literal=SPLUNK_AO_REALM="$REALM" \
> --from-literal=SPLUNK_AO_PROJECT="project-$PARTICIPANT_NUMBER" \
> --from-literal=SPLUNK_AO_AGENT_STREAM="default"
> ```

{{% notice title="Project and agent stream" style="info" %}}

`SPLUNK_AO_PROJECT` and `SPLUNK_AO_AGENT_STREAM` decide where your traces appear in the Splunk Agent Observability
console. If you leave them blank, the SDK falls back to a project and agent stream both named
`default`. 

{{% /notice %}}

{{< /step >}}


{{< /exercise >}}

{{< checkpoint title="Knowledge Check" >}}

If you remove `SPLUNK_AO_PROJECT` and `SPLUNK_AO_AGENT_STREAM` from the `splunk-ao-config` config map, where will
your traces show up?

{{< details summary="Click here to see the answer" >}}
In a project named `default` and an agent stream named `default`. With those keys empty,
`setup_env.py` exports empty `SPLUNK_AO_PROJECT` / `SPLUNK_AO_AGENT_STREAM` values, and the Splunk AO
SDK falls back to its built-in `default` project and `default` agent stream.
{{< /details >}}
