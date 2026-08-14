# Splunk AO Experiments

Run Splunk AO experiments against the healthcare assistant using the sample dataset in `dataset.csv`.

## Overview

- Create a dataset from `dataset.csv`
- Run experiments that invoke `HealthcareAgent` for each row
- Evaluate responses with default Splunk AO metrics

## File structure

```
experiments/
├── experiment_helpers.py      # Shared helpers for CLI (and future UI)
├── create_galileo_dataset.py  # Upload dataset.csv to Splunk AO
├── run_experiment.py            # Run an experiment
└── README.md
```

## Dataset format

`dataset.csv` lives in the app root (`3-app-with-experiments/dataset.csv`) and must have `input` and `output` columns:

| Column | Description |
|--------|-------------|
| `input` | User query sent to the agent |
| `output` | Reference response for ground-truth scoring |

The sample dataset covers the three tools available in this app:

- `get_patient_info` — patient lookups (e.g. P001, P005)
- `search_medicine_qa` — medicine questions (dosage, side effects, interactions)
- `delete_patient_record` — explicit delete requests

## CLI usage

Run commands from the `3-app-with-experiments` directory.

### Step 1: Create the dataset (one-time)

```bash
# Preview rows before uploading
python experiments/create_galileo_dataset.py --preview

# Upload to Splunk AO
python experiments/create_galileo_dataset.py
```

This reads `dataset.csv` and creates a dataset named **Healthcare Assistant Dataset.csv**.

> **Note:** The SDK uses the dataset name as the upload filename. The API requires a file extension (`.csv`, `.jsonl`, etc.), so the stored name includes `.csv` even though you pass `--name "Healthcare Assistant Dataset"`.

### Step 2: Run an experiment

```bash
# Default experiment name and dataset
python experiments/run_experiment.py

# Custom name and model
python experiments/run_experiment.py --experiment-name "lisinopril-eval" --model gpt-4o-mini
```

For each row, the script:

1. Sends the `input` to `HealthcareAgent`
2. Collects the agent response
3. Scores it with the default metrics

### Default metrics

- Ground Truth Adherence
- Prompt Injection
- Chunk Attribution Utilization
- Context Adherence

## Prerequisites

- PostgreSQL with pgvector set up (`python helpers/setup_vectordb.py local`)
- `.streamlit/secrets.toml` configured with OpenAI and Splunk AO credentials
- `splunk-ao` package installed (`pip install -r requirements.txt`)

## Integration notes

Experiments use the same `HealthcareAgent` as the Streamlit chat app. When `run_experiment` provides an experiment trace context, the agent detects it **before** opening a log-stream `splunk_ao_context` and uses `SplunkAOAsyncCallback(start_new_trace=False)` so LangGraph spans nest under the experiment trace. Do not wrap experiment runs in `splunk_ao_context(project=..., agent_stream=...)` — that switches to a different logger and collapses the trace to a single span.
