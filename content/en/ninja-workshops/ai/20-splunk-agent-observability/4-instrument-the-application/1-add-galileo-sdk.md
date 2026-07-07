---
title: Add the Galileo SDK and Configuration
linkTitle: 1. Add the Galileo SDK
weight: 1
time: 5 minutes
---


First, add the Galileo package and the configuration the SDK needs to know *where* to send
traces.

{{< exercise title="Add the SDK and configuration" >}}

{{< step title="Add the Galileo package" >}}

Galileo's LangChain callback ships in the `galileo` package. 

Open the `~/workshop/healthcare-assistant/2-app-with-instrumentation/requirements.txt` 
file for editing and add the following to the end of the file: 

````
galileo
````

{{< /step >}}

{{< step title="Set Environment Variables" >}}

Run the commands provided by your workshop instructor to set environment variables 
on your EC2 instance. They'll look like the following: 

````
export PARTICIPANT_NUMBER=<your participant number>  
export GALILEO_API_KEY=<provided by workshop instructor>  
export GALILEO_CONSOLE_URL=<provided by workshop instructor>
````

{{< /step >}}

{{< step title="Create a Galileo Secret" >}}

Run the following command to create a Kubernetes secret, which stores the Galileo API key: 

```bash
kubectl create secret generic galileo-secret \
  --from-literal=GALILEO_API_KEY="$GALILEO_API_KEY"
```

{{< /step >}}

{{< step title="Create a Galileo Config Map" >}}

Run the following command to create a Kubernetes config map, which the application will use to
determine how to send traces to Galileo: 

```bash
kubectl create configmap galileo-config \
  --from-literal=GALILEO_CONSOLE_URL="$GALILEO_CONSOLE_URL" \
  --from-literal=GALILEO_PROJECT="project-$PARTICIPANT_NUMBER" \
  --from-literal=GALILEO_LOG_STREAM="default"
```

{{% notice title="Project and log stream" style="info" %}}

`GALILEO_PROJECT` and `GALILEO_LOG_STREAM` decide where your traces appear in the Galileo
console. If you leave them blank, the SDK falls back to a project and log stream both named
`default`. 

{{% /notice %}}

{{< /step >}}


{{< /exercise >}}

{{< checkpoint title="Knowledge Check" >}}

If you remove `GALILEO_PROJECT` and `GALILEO_LOG_STREAM` from the `galileo-config` config map, where will
your traces show up?

{{< details summary="Click here to see the answer" >}}
In a project named `default` and a log stream named `default`. With those keys empty,
`setup_env.py` exports empty `GALILEO_PROJECT` / `GALILEO_LOG_STREAM` values, and the Galileo
SDK falls back to its built-in `default` project and `default` log stream.
{{< /details >}}
