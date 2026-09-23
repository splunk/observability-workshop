---
title: Create a Dataset
linkTitle: 1. Create a Dataset
weight: 1
time: 5 minutes
---

An experiment needs a dataset to run against. This app ships a sample `dataset.csv` in the
app root that covers all three tools: patient lookups, medicine questions, and delete
requests.

## Dataset format

The CSV has two columns:

| Column | Description |
|--------|-------------|
| `input` | The user query sent to the agent |
| `output` | A reference response used for ground-truth scoring |

A few sample rows:

```text
input,output
Can you look up information for patient P001?,I'll look up patient P001 using the get_patient_info tool.
What is the dosage and common side effects of Lisinopril?,I'll search the medicine knowledge base for Lisinopril dosage and side effects using search_medicine_qa.
Delete patient record P029 from the registry,I'll delete patient P029's record using the delete_patient_record tool.
```

{{< exercise title="Create the Galileo dataset" >}}

{{< step title="Set up the environment" >}}

Change into the experiments stage, activate a virtual environment, and install dependencies
(the `galileo` package is already in `requirements.txt`):

```bash
cd ~/workshop/healthcare-assistant/3-app-with-experiments
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Make sure `.streamlit/secrets.toml` is configured with your OpenAI, PostgreSQL, and Galileo
credentials (same values as Chapter 3), and that the database is loaded
(`./start_vectordb.sh` if you haven't already).

{{< /step >}}

{{< step title="Preview the dataset" >}}

Before uploading, preview the rows the script will send to Galileo:

```bash
python experiments/create_galileo_dataset.py --preview
```

{{< /step >}}

{{< step title="Upload the dataset to Galileo" >}}

When the preview looks right, upload it:

```bash
python experiments/create_galileo_dataset.py
```

This creates a Galileo dataset named **Healthcare Assistant Dataset.csv** from
`dataset.csv`.

{{% notice title="Why the .csv suffix in the name?" style="info" %}}

The Galileo SDK uses the dataset name as the upload filename, and the API requires a file
extension. So even though the default name is *Healthcare Assistant Dataset*, the stored
dataset is named *Healthcare Assistant Dataset.csv*.

{{% /notice %}}

{{< /step >}}

{{< /exercise >}}

{{< checkpoint title="Knowledge Check" >}}

Why does the dataset include an `output` column when the agent generates its own responses
at run time?

{{< details summary="Click here to see the answer" >}}
The `output` column is the **reference (ground-truth) response**. Metrics like *Ground Truth
Adherence* compare the agent's generated answer against this reference to score how closely
it matches the expected behavior. Without it, you couldn't measure ground-truth adherence.
{{< /details >}}
