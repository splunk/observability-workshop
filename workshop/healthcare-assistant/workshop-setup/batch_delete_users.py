#!/usr/bin/env python3
"""
De-provision users created by batch_create_users.py.

Reads the SAME input CSV used for creation (columns: email, first_name, last_name,
role, group_ids - only `email` is used here) and, for each row:

  1. POST /projects/paginated (admin auth) -> finds the project named after the user
                                              (email local-part, e.g. "participant1"
                                              for participant1@galileo.ai).
  2. DELETE /projects/{project_id}          -> deletes the project (synchronous;
                                              also removes its runs/logs/data).
  3. POST /users/all           (admin auth) -> looks up the user's org-scoped id.
  4. DELETE /users/{user_id}                -> deletes the user.

Project is deleted BEFORE the user (matches the reverse of the creation order, and
sidesteps any project-ownership FK dependency on the user row).

IMPORTANT CAVEATS
-----------------
* This is DESTRUCTIVE and NOT REVERSIBLE. Projects are deleted synchronously along
  with their runs/logs/data. You will be asked to confirm before anything happens
  (pass --yes to skip the prompt, e.g. for unattended/scripted use).
* Deleting a user via DELETE /users/{user_id} removes their organization membership
  AND, if this was their only organization, deletes their global account entirely -
  they could not sign back in or be re-invited with that email without being created
  from scratch.
* If more than one project matches the expected name (not supposed to happen for
  projects created by batch_create_users.py, but possible if names collide), that
  row is skipped and flagged as ambiguous rather than guessing which one to delete.

SETUP
-----
Reuses the same .env file as batch_create_users.py:
    GALILEO_BASE_URL
    GALILEO_ADMIN_TOKEN, or GALILEO_ADMIN_EMAIL + GALILEO_ADMIN_PASSWORD

USAGE
-----
    python batch_delete_users.py --input-csv users.csv --output-csv delete_results.csv

    # Preview what would happen without deleting anything:
    python batch_delete_users.py --input-csv users.csv --dry-run
"""

import argparse
import csv
import os
import sys
import time

import requests

from batch_create_users import find_org_user_id, get_admin_token, load_env_file

REQUEST_DELAY_SECONDS = 0.3
ROW_DELAY_SECONDS = 1  # pause between users so a large batch doesn't hammer the server


def find_project_id_by_name(base_url: str, admin_headers: dict, name: str) -> tuple[str | None, str]:
    resp = requests.post(
        f"{base_url}/projects/paginated",
        params={"limit": 10, "starting_token": 0},
        headers=admin_headers,
        json={"filters": [{"name": "name", "value": name, "operator": "eq"}]},
        timeout=30,
    )
    if resp.status_code != 200:
        return None, f"project lookup failed ({resp.status_code}): {resp.text}"

    projects = resp.json().get("projects", [])
    if not projects:
        return None, "no project found with that name"
    if len(projects) > 1:
        return None, f"ambiguous: {len(projects)} projects found with that name"
    return projects[0]["id"], ""


def delete_project(base_url: str, admin_headers: dict, project_id: str) -> tuple[bool, str]:
    resp = requests.delete(f"{base_url}/projects/{project_id}", headers=admin_headers, timeout=60)
    if resp.status_code != 200:
        return False, f"project delete failed ({resp.status_code}): {resp.text}"
    return True, ""


def delete_user(base_url: str, admin_headers: dict, user_id: str) -> tuple[bool, str]:
    print(f"--> Deleting user: {user_id}")
    resp = requests.delete(f"{base_url}/users/{user_id}", headers=admin_headers, timeout=30)
    if resp.status_code != 200:
        return False, f"user delete failed ({resp.status_code}): {resp.text}"
    return True, ""


def process_row(base_url: str, admin_headers: dict, row: dict, dry_run: bool = False) -> dict:
    email = row["email"].strip().lower()
    project_name = email.split("@")[0]

    result = {
        "email": email,
        "project_status": "skipped",
        "project_id": "",
        "user_status": "skipped",
        "user_id": "",
        "error": "",
    }
    errors = []

    project_id, error = find_project_id_by_name(base_url, admin_headers, project_name)
    if project_id:
        result["project_id"] = project_id
        if dry_run:
            result["project_status"] = "would_delete"
        else:
            ok, error = delete_project(base_url, admin_headers, project_id)
            result["project_status"] = "deleted" if ok else "failed"
            if not ok:
                errors.append(error)
    else:
        result["project_status"] = "not_found"
        errors.append(f"project: {error}")
    time.sleep(REQUEST_DELAY_SECONDS)

    user_id = find_org_user_id(base_url, admin_headers, email)
    if user_id:
        result["user_id"] = user_id
        if dry_run:
            result["user_status"] = "would_delete"
        else:
            ok, error = delete_user(base_url, admin_headers, user_id)
            result["user_status"] = "deleted" if ok else "failed"
            if not ok:
                errors.append(error)
    else:
        result["user_status"] = "not_found"
        errors.append("user: no user found with that email")

    result["error"] = "; ".join(errors)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input-csv", default="users.csv", help="Same CSV used with batch_create_users.py")
    parser.add_argument("--output-csv", default="delete_results.csv", help="Where to write per-user results")
    parser.add_argument("--env-file", default=".env", help="Path to the .env file with credentials")
    parser.add_argument("--yes", action="store_true", help="Skip the confirmation prompt")
    parser.add_argument(
        "--dry-run", action="store_true", help="Look up what would be deleted without deleting anything"
    )
    args = parser.parse_args()

    load_env_file(args.env_file)

    base_url = os.environ.get("GALILEO_BASE_URL", "").rstrip("/")
    admin_token = os.environ.get("GALILEO_ADMIN_TOKEN")
    admin_email = os.environ.get("GALILEO_ADMIN_EMAIL")
    admin_password = os.environ.get("GALILEO_ADMIN_PASSWORD")

    if not base_url:
        parser.error("GALILEO_BASE_URL is required (set it in your .env file)")
    if not admin_token and not (admin_email and admin_password):
        parser.error("Set GALILEO_ADMIN_TOKEN, or both GALILEO_ADMIN_EMAIL and GALILEO_ADMIN_PASSWORD, in your .env file")

    token = admin_token or get_admin_token(base_url, admin_email, admin_password)
    admin_headers = {"Authorization": f"Bearer {token}"}

    with open(args.input_csv, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        print("Input CSV has no rows.", file=sys.stderr)
        return 1

    emails = [row["email"].strip().lower() for row in rows if row.get("email", "").strip()]
    if args.dry_run:
        print(f"[dry run] Looking up {len(emails)} project(s) and user(s) against {base_url} - nothing will be deleted.")
    elif not args.yes:
        print(f"This will PERMANENTLY delete {len(emails)} project(s) and user(s) against {base_url}:")
        for email in emails:
            print(f"  - {email} (project: {email.split('@')[0]})")
        confirmation = input("Type 'delete' to proceed: ")
        if confirmation.strip().lower() != "delete":
            print("Aborted.")
            return 1

    results = []
    for i, row in enumerate(rows, start=1):
        email = row.get("email", "").strip()
        if not email:
            print(f"Row {i}: missing email, skipping", file=sys.stderr)
            continue
        print(f"[{i}/{len(rows)}] {'checking' if args.dry_run else 'deleting'} {email} ...")
        result = process_row(base_url, admin_headers, row, dry_run=args.dry_run)
        results.append(result)
        print(
            f"    -> project: {result['project_status']}, user: {result['user_status']}"
            + (f" ({result['error']})" if result["error"] else "")
        )

        if i < len(rows):
            time.sleep(ROW_DELAY_SECONDS)

    with open(args.output_csv, "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["email", "project_status", "project_id", "user_status", "user_id", "error"]
        )
        writer.writeheader()
        writer.writerows(results)

    if args.dry_run:
        would_delete = sum(
            1 for r in results if r["project_status"] == "would_delete" and r["user_status"] == "would_delete"
        )
        print(f"\n[dry run] {would_delete}/{len(results)} would be fully deleted (project + user).")
    else:
        fully_deleted = sum(1 for r in results if r["project_status"] == "deleted" and r["user_status"] == "deleted")
        print(f"\nDone: {fully_deleted}/{len(results)} fully deleted (project + user).")
    print(f"Results written to {args.output_csv}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
