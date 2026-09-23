#!/usr/bin/env python3
"""
Create a dataset from dataset.csv in the app root.

Usage:
    python experiments/create_galileo_dataset.py
    python experiments/create_galileo_dataset.py --preview
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from setup_env import setup_environment
from experiments.experiment_helpers import (
    DEFAULT_DATASET_FILE,
    DEFAULT_DATASET_NAME,
    create_dataset_from_csv,
    format_dataset_name,
    read_dataset_csv,
)


def main():
    parser = argparse.ArgumentParser(description="Create a dataset from dataset.csv")
    parser.add_argument(
        "--dataset-file",
        default=str(DEFAULT_DATASET_FILE),
        help="Path to CSV file (default: dataset.csv in app root)",
    )
    parser.add_argument(
        "--name",
        default=DEFAULT_DATASET_NAME,
        help=f"Dataset name (default: {DEFAULT_DATASET_NAME})",
    )
    parser.add_argument(
        "--preview",
        "-p",
        action="store_true",
        help="Preview the dataset without uploading",
    )
    args = parser.parse_args()

    setup_environment()

    dataset = read_dataset_csv(args.dataset_file)
    if not dataset:
        print(f"No data found in {args.dataset_file}")
        sys.exit(1)

    if args.preview:
        print(f"Found {len(dataset)} samples in {args.dataset_file}")
        for i, sample in enumerate(dataset[:3]):
            print(f"\nSample {i + 1}:")
            print(f"Input: {sample['input']}")
            print(f"Output: {sample['output'][:100]}...")
        return

    dataset_obj = create_dataset_from_csv(args.dataset_file, dataset_name=args.name)
    dataset_name = format_dataset_name(args.name, Path(args.dataset_file))
    print(f"Dataset created: {dataset_name}")
    print(f"ID: {dataset_obj.id}")


if __name__ == "__main__":
    main()
