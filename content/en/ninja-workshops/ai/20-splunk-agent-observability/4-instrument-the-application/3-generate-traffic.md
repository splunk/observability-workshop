---
title: Generate Traffic
linkTitle: 3. Generate Traffic
weight: 3
time: 5 minutes
---

With the callback attached, run the instrumented app and send a few requests. Every turn now
produces a trace in Splunk Agent Observability. You'll explore those traces in detail in the
next chapter.

{{< exercise title="Run the app and generate traces" >}}

{{< step title="Build a New Docker Image" >}}

Change into the base app directory, then run the following command to build a new Docker image
for the application that includes our recent changes: 

```bash
cd ~/workshop/healthcare-assistant
docker build --platform linux/amd64 -f 2-app-with-instrumentation/Dockerfile -t localhost:9999/healthcare-assistant:app-with-instrumentation .
docker push localhost:9999/healthcare-assistant:app-with-instrumentation
```

{{< /step >}}


{{< step title="Deploy the healthcare assistant app" >}}

Run the following command to deploy the healthcare assistant app:

```bash
cd ~/workshop/healthcare-assistant/2-app-with-instrumentation
kubectl apply -f k8s.yaml
```

Ensure that the new application pod is running:

```bash
kubectl get pods -l app=healthcare-assistant
NAME                                   READY   STATUS    RESTARTS   AGE
healthcare-assistant-d764fc757-l9fxt   1/1     Running   0          20s
```

Using the IP address of your EC2 instance and port 81, open the healthcare assistant app using your browser.
For example: 

```text
  External URL: http://98.86.181.9:81
```

{{< /step >}}

{{< step title="Send a few requests" >}}

Exercise both tool paths so you generate a RAG trace and a text-to-SQL trace:

> What is the dosage and common side effects of Lisinopril?

> Can you look up information for patient P001?

Then send a trickier medical question to give yourself something interesting to investigate
later:

> Is it safe to double my dose of Lisinopril if I miss a day?

Each message returns a normal answer; the callback doesn't change the app's behavior, it
just records it.

{{< /step >}}

{{< step title="Review the application logs" >}}

Use the following command to view the application logs: 

```bash
kubectl logs -l app=healthcare-assistant
```

If everything is working as expected, you should see the following in the logs: 

````
Collecting usage statistics. To deactivate, set browser.gatherUsageStats to false.

2026-07-07 17:52:39.433 Uvicorn server started on :::8501

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://10.42.0.18:8501
  External URL: http://98.92.157.71:8501
````

{{% notice title="Tip" style="tip" icon="exclamation-triangle" %}}

To see exactly what the SDK is doing, you can temporarily add the following near the top of
`agent.py`:

```python
from galileo.utils.log_config import enable_console_logging

enable_console_logging()
```

Then rebuild the Docker image and redeploy the application. 

{{% /notice %}}

{{< /step >}}

{{< /exercise >}}

{{% notice title="What you just unlocked" style="info" %}}

In one small change you went from a black box to full capture: every prompt, response, tool
call, retrieval, token count, and latency for every turn is now recorded. In the next chapter
you'll put that to work and investigate exactly what the agent did.

{{% /notice %}}

{{< checkpoint title="Knowledge Check" >}}

You sent three messages. Roughly how many traces did you create, and what determines that?

{{< details summary="Click here to see the answer" >}}
**Three traces, one per user turn.** A fresh callback is attached per call, and the whole
LangGraph turn runs as a single root run, so each message becomes one trace containing nested
LLM and tool spans. You'll review the traces in more detail in the next section.
{{< /details >}}
