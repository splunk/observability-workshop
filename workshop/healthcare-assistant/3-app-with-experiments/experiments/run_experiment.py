#!/usr/bin/env python3
"""
Run a Galileo experiment against the healthcare assistant.

Usage:
    python experiments/run_experiment.py
    python experiments/run_experiment.py --experiment-name my-experiment
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from setup_env import setup_environment
from experiments.experiment_helpers import (
    DEFAULT_DATASET_NAME,
    DEFAULT_METRICS,
    galileo_dataset_name,
    get_dataset_by_name,
    run_healthcare_experiment,
)


def main():
    parser = argparse.ArgumentParser(description="Run a Galileo experiment for the healthcare assistant")
    parser.add_argument(
        "--experiment-name",
        default="healthcare-experiment",
        help="Experiment name (default: healthcare-experiment)",
    )
    parser.add_argument(
        "--dataset-name",
        default=DEFAULT_DATASET_NAME,
        help=f"Galileo dataset name (default: {DEFAULT_DATASET_NAME}; stored as name + .csv)",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="OpenAI model override (default: model from config.yaml)",
    )
    args = parser.parse_args()

    setup_environment()

    galileo_name = galileo_dataset_name(args.dataset_name)

    try:
        dataset = get_dataset_by_name(galileo_name)
        print(f"Found dataset: {galileo_name}")
    except Exception as e:
        print(f"Error loading dataset '{galileo_name}': {e}")
        print("Create it first with: python experiments/create_galileo_dataset.py")
        sys.exit(1)

    print(f"Running experiment: {args.experiment_name}")
    print(f"Dataset Name: {galileo_name}")
    print(f"Dataset: {dataset}")
    print(f"Metrics: {[m.name for m in DEFAULT_METRICS]}")

    try:
        results = run_healthcare_experiment(
            experiment_name=args.experiment_name,
            dataset=dataset,
            model_name=args.model,
        )
        print("Experiment completed successfully!")
        print(f"Results: {results}")
    except Exception as e:
        print(f"Error running experiment: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
