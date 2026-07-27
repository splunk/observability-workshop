#!/usr/bin/env python3
"""
Generate a users.csv file for workshop participant provisioning.

Creates users-{N}.csv with N rows in the same format as users.csv:
  participant1@galileo.ai through participant{N}@galileo.ai

USAGE
-----
    python generate_users_csv.py 100
    python generate_users_csv.py 100 --output-dir .
"""

import argparse
import csv
import sys

FIELDNAMES = [
    "email",
    "first_name",
    "last_name",
    "role",
    "group_ids",
    "participant_number",
]


def generate_rows(count: int) -> list[dict[str, str]]:
    return [
        {
            "email": f"participant{n}@galileo.ai",
            "first_name": f"Participant {n}",
            "last_name": "Workshop",
            "role": "user",
            "group_ids": "",
            "participant_number": str(n),
        }
        for n in range(1, count + 1)
    ]


def write_users_csv(path: str, count: int) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(generate_rows(count))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a users-{N}.csv file for workshop participants.",
    )
    parser.add_argument(
        "participants",
        type=int,
        metavar="N",
        help="Number of participants to generate (e.g. 100)",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory to write the CSV file (default: current directory)",
    )
    args = parser.parse_args()

    if args.participants < 1:
        print("Participant count must be at least 1.", file=sys.stderr)
        return 1

    output_path = f"{args.output_dir.rstrip('/')}/users-{args.participants}.csv"
    write_users_csv(output_path, args.participants)
    print(f"Wrote {args.participants} participant(s) to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
