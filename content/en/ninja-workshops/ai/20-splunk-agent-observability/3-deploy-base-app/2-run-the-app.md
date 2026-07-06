---
title: Run the Application
linkTitle: 2. Run the Application
weight: 2
time: 5 minutes
---

With the database loaded and secrets in place, start the app and exercise the two main
agent paths.

{{< exercise title="Run and try the assistant" >}}

{{< step title="Stop the k3d cluster" >}}

Stop the `k3d` cluster, since we're not using it in this workshop, and we need
to free up port 81 for the healthcare assistant application:

```bash
k3d cluster stop shw-987d-cluster
```

{{< /step >}}


{{< step title="Start the app" >}}

From the `1-base-app` directory (with your virtual environment active), run:

```bash
sudo --preserve-env=OPENAI_API_KEY,OPENAI_BASE_URL \
  $(which python) -m streamlit run app.py \
  --server.port 81 \
  --server.address 0.0.0.0
```

Streamlit will print an external URL. Open it in your browser:

```text
  LExternal URL: http://98.86.181.9:81
```

![Healthcare assistant home screen](../../images/healthcare-assistant-ui.png?width=750px)

{{< /step >}}

{{< step title="Try the RAG path" >}}

Click the example button (or type) for the medicine question:

> What is the dosage and common side effects of Lisinopril?

The agent calls the `search_medicine_qa` tool, which retrieves matching chunks from
pgvector, and returns a grounded answer.

![Healthcare assistant home screen](../../images/healthcare-assistant-dosage.png?width=750px)

{{< /step >}}

{{< step title="Try the text-to-SQL path" >}}

Now ask the patient-lookup question:

> Can you look up information for patient P001?

The agent calls `get_patient_info`, which generates SQL against the `healthcare_patient`
table and returns the patient's details.

![Healthcare assistant home screen](../../images/healthcare-assistant-patient.png?width=750px)

{{< /step >}}

{{< /exercise >}}

{{% notice title="Notice what's missing" style="info" %}}

The app works, but right now you have **no record** of what the agent did. You can't see
which tool was called, what was retrieved, how many tokens were used, or whether the answer
was even correct. If the assistant told a patient to take double their dose right now, you'd
find out from social media, not from your tooling. That's exactly the gap you'll close in the
next chapter by instrumenting the app with Splunk Agent Observability.

{{% /notice %}}

{{< checkpoint title="Knowledge Check" >}}

When you ask the patient-lookup question, which tool does the agent invoke, and what backend
does it hit?

{{< details summary="Click here to see the answer" >}}
The agent invokes **`get_patient_info`**, which uses text-to-SQL to generate a `SELECT`
against the **`healthcare_patient`** table in PostgreSQL and returns the matching row.
{{< /details >}}
