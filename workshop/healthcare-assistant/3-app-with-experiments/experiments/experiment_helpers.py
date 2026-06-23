"""
Helper functions for running Galileo experiments against the healthcare assistant.
"""
import os
import csv
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

from galileo.datasets import create_dataset, get_dataset, list_datasets
from galileo.experiments import run_experiment
from galileo_core.schemas.shared.scorers.scorer_name import ScorerName as GalileoScorers

from agent import HealthcareAgent
from config import APP_ROOT

DEFAULT_DATASET_FILE = APP_ROOT / "dataset.csv"
DEFAULT_DATASET_NAME = "Healthcare Assistant Dataset"

_SUPPORTED_DATASET_EXTENSIONS = (".csv", ".jsonl", ".json", ".feather")


def galileo_dataset_name(name: str = DEFAULT_DATASET_NAME, dataset_file: Path = DEFAULT_DATASET_FILE) -> str:
    """Return the dataset name Galileo stores, with a required file extension.

    The Galileo SDK sends ``name`` as the multipart upload filename. The API
  rejects uploads unless that filename ends with .csv, .jsonl, .json, or .feather.
    """
    if name.endswith(_SUPPORTED_DATASET_EXTENSIONS):
        return name
    return f"{name}{Path(dataset_file).suffix or '.csv'}"

DEFAULT_METRICS = [
    GalileoScorers.ground_truth_adherence,
    GalileoScorers.prompt_injection,
    GalileoScorers.chunk_attribution_utilization,
    GalileoScorers.context_adherence,
]

AVAILABLE_METRICS = {
    "Ground Truth Adherence": GalileoScorers.ground_truth_adherence,
    "Prompt Injection": GalileoScorers.prompt_injection,
    "Chunk Attribution Utilization": GalileoScorers.chunk_attribution_utilization,
    "Context Adherence": GalileoScorers.context_adherence,
}


def read_dataset_csv(dataset_file: str | Path = DEFAULT_DATASET_FILE) -> List[Dict[str, str]]:
    """Read a CSV file and return input/output pairs."""
    dataset = []
    with Path(dataset_file).open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if "input" in row and "output" in row:
                dataset.append({
                    "input": row["input"].strip(),
                    "output": row["output"].strip(),
                })
    return dataset


def create_dataset_from_csv(
    dataset_file: str | Path = DEFAULT_DATASET_FILE,
    dataset_name: Optional[str] = None,
) -> Any:
    """Create a Galileo dataset from the local CSV file."""
    dataset_path = Path(dataset_file)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset file not found: {dataset_path}")

    dataset_content = read_dataset_csv(dataset_path)
    if not dataset_content:
        raise ValueError("No data found in dataset file")

    name = galileo_dataset_name(dataset_name or DEFAULT_DATASET_NAME, dataset_path)
    return create_dataset(name=name, content=dataset_path)


def get_dataset_by_name(name: str) -> Any:
    """Get a Galileo dataset by name."""
    return get_dataset(name=name)


def get_dataset_by_id(dataset_id: str) -> Any:
    """Get a Galileo dataset by ID."""
    return get_dataset(id=dataset_id)


def get_all_datasets() -> List[Any]:
    """List all Galileo datasets."""
    return list_datasets()


def create_experiment_function(model_name: Optional[str] = None):
    """Build the per-row function passed to ``run_experiment``."""

    def experiment_function(input_data):
        agent = HealthcareAgent(
            session_id=str(uuid.uuid4()),
            model_override=model_name,
        )

        if isinstance(input_data, str):
            user_input = input_data
        else:
            user_input = input_data.get("input", "")

        messages = [{"role": "user", "content": user_input}]
        return agent.process_query(messages)

    return experiment_function


def run_healthcare_experiment(
    experiment_name: str,
    dataset: Any,
    metrics: Optional[List] = None,
    project: Optional[str] = None,
    model_name: Optional[str] = None,
) -> Any:
    """Run an experiment against the healthcare assistant."""
    if metrics is None:
        metrics = DEFAULT_METRICS

    if project is None:
        project = os.environ.get("GALILEO_PROJECT", "default")

    experiment_function = create_experiment_function(model_name=model_name)

    return run_experiment(
        experiment_name,
        dataset=dataset,
        function=experiment_function,
        metrics=metrics,
        project=project,
    )
