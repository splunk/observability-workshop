#!/usr/bin/env python3
"""
Batch-create Galileo users with a single admin-assigned password.

Galileo has no native "create user" endpoint for admins - users are normally invited
by email and pick their own password. This script chains together existing, real
Galileo API endpoints to create users in bulk AND set the same password for all of
them, without requiring the end user to click anything:

  1. POST /signup_link      (admin auth)  -> creates the user, returns a signup URL
                                             containing a one-time signup token
                                             (requires the `show_invitation_link_and_
                                             reset_password` feature flag to be enabled
                                             for your environment - confirmed enabled).
  2. POST /system_users     (no auth,      -> completes signup using the token, setting
                              token-gated)    the shared password.
  3. POST /users/all        (admin auth)  -> looks up the new user's org-scoped id.
  4. PUT  /users/{user_id}  (admin auth)  -> sets the role, if different from default.
  5. POST /groups/{id}/members (admin auth) -> adds the user to any requested groups.
  6. POST /projects         (admin auth)  -> creates a new project named after the user
                                             (the admin is auto-added as its owner).
  7. POST /projects/{id}/users (admin auth) -> adds the new user as Owner of that project.

IMPORTANT CAVEATS
-----------------
* Step 1 (/signup_link) ALWAYS sends a real signup/invite email to the user - there is
  no way to suppress it. If you don't want these emails going out, this approach is not
  suitable; use POST /invite_users instead and skip password-setting.
* Every user gets the SAME password (from .env). Treat that value as sensitive, and
  have users change it after first login if that matters for your use case.
* Signup tokens expire in 14 days; this script uses them immediately so that's a non-issue.

ERROR HANDLING
--------------
Results are written to --output-csv incrementally, one row at a time (flushed to
disk immediately), so a crash partway through a large batch doesn't lose progress
already made. Any row whose user was NOT created at all (status "failed" - e.g. a
transient network error, a duplicate email, or signup_link/system_users rejecting
the request) is also written, in the original input CSV format, to --failed-csv.
Rows that WERE created but hit a problem in a later step (role/group/project) are
marked "partial" in --output-csv and are NOT included in --failed-csv, since the
account already exists and blindly re-running creation for them would fail with a
duplicate-email error - check those rows manually instead.

To retry, just re-run this script with the failed-users file as the input:

    python batch_create_users.py --input-csv failed-users.csv --output-csv retry_results.csv

A handful of transient HTTP failures (connection errors, timeouts, 5xx responses)
are retried automatically with backoff before a row is given up on as failed.

SETUP
-----
    pip install requests
    cp .env.example .env    # then fill in your values

.env FILE
---------
    GALILEO_BASE_URL=https://api.your-galileo-instance.com
    GALILEO_USER_PASSWORD=SomeSharedStr0ng_Pass!

    # Auth option A: admin email/password (script logs in to get a bearer token)
    GALILEO_ADMIN_EMAIL=admin@yourorg.com
    GALILEO_ADMIN_PASSWORD=...

    # Auth option B: an already-obtained admin bearer token (skips login)
    # GALILEO_ADMIN_TOKEN=eyJhbGciOi...

    # Optional
    GALILEO_DEFAULT_ROLE=user   # applied when a CSV row doesn't specify a role

USAGE
-----
    python batch_create_users.py --input-csv users.csv --output-csv results.csv

INPUT CSV FORMAT
----------------
Required column: email
Optional columns: first_name, last_name, role, group_ids

- role: one of admin, manager, user, read_only. Defaults to GALILEO_DEFAULT_ROLE.
- group_ids: semicolon-separated group UUIDs to add the user to (find these via the
  console or GET /groups). Leave blank to skip group assignment.

For every user, a new project is also created (named "project-{participant_number}",
falling back to the email local-part if participant_number is absent) and the user is
added to it as Owner. The project is created under the admin's identity (the admin is
auto-added as owner at creation time), then the new user is separately granted the
Owner role on it.

See sample_users.csv in this folder for an example.
"""

import argparse
import csv
import os
import sys
import time
from urllib.parse import parse_qs, urlparse

import requests

REQUEST_DELAY_SECONDS = 0.3  # be gentle with the rate limiter on /signup_link and /system_users
ROW_DELAY_SECONDS = 1  # pause between users so a large batch doesn't hammer the server
MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 2


def request_with_retry(method: str, url: str, **kwargs) -> requests.Response:
    """requests.request(), retrying transient failures (connection errors, timeouts, 5xx) with backoff."""
    last_exc = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.request(method, url, **kwargs)
        except requests.exceptions.RequestException as exc:
            last_exc = exc
        else:
            if resp.status_code < 500:
                return resp
            last_exc = None
        if attempt < MAX_RETRIES:
            time.sleep(RETRY_BACKOFF_SECONDS * attempt)
    if last_exc:
        raise last_exc
    return resp


def load_env_file(path: str) -> None:
    """Load KEY=VALUE pairs from a .env file into os.environ (without overriding real env vars)."""
    if not os.path.exists(path):
        return
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)


def get_admin_token(base_url: str, admin_email: str, admin_password: str) -> str:
    resp = request_with_retry(
        "POST",
        f"{base_url}/login",
        data={"username": admin_email, "password": admin_password},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def create_signup_link(base_url: str, admin_headers: dict, email: str) -> tuple[str | None, str]:
    """Returns (signup_token, message). signup_token is None if creation failed."""
    resp = request_with_retry(
        "POST",
        f"{base_url}/signup_link",
        params={"user_email": email},
        headers=admin_headers,
        timeout=30,
    )
    if resp.status_code != 200:
        return None, f"signup_link failed ({resp.status_code}): {resp.text}"

    body = resp.json()
    signup_url = body.get("signup_url")
    if not signup_url:
        return None, (
            "signup_link succeeded but returned no signup_url - the "
            "show_invitation_link_and_reset_password feature flag may not be enabled "
            "for this environment."
        )

    query = parse_qs(urlparse(signup_url).query)
    tokens = query.get("token")
    if not tokens:
        return None, f"signup_url had no token query param: {signup_url}"

    return tokens[0], body.get("message", "")


def complete_signup(
    base_url: str, signup_token: str, email: str, password: str, first_name: str, last_name: str
) -> tuple[bool, str]:
    json={
        "email": email,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
        "auth_method": "email",
    }
    resp = request_with_retry(
        "POST",
        f"{base_url}/system_users",
        params={"signup_token": signup_token},
        json=json,
        timeout=30,
    )
    if resp.status_code != 200:
        return False, f"system_users failed ({resp.status_code}): {resp.text}"
    return True, ""


def find_org_user_id(base_url: str, admin_headers: dict, email: str) -> str | None:
    resp = request_with_retry(
        "POST",
        f"{base_url}/users/all",
        params={"limit": 1, "starting_token": 0},
        headers=admin_headers,
        json={"filters": [{"name": "email", "value": email, "operator": "eq"}]},
        timeout=30,
    )
    resp.raise_for_status()
    users = resp.json().get("users", [])
    return users[0]["id"] if users else None


def set_role(base_url: str, admin_headers: dict, user_id: str, role: str) -> tuple[bool, str]:
    resp = request_with_retry(
        "PUT",
        f"{base_url}/users/{user_id}",
        headers=admin_headers,
        json={"role": role},
        timeout=30,
    )
    if resp.status_code != 200:
        return False, f"role update failed ({resp.status_code}): {resp.text}"
    return True, ""


def add_to_groups(base_url: str, admin_headers: dict, user_id: str, group_ids: list[str]) -> tuple[bool, str]:
    errors = []
    for group_id in group_ids:
        resp = request_with_retry(
            "POST",
            f"{base_url}/groups/{group_id}/members",
            headers=admin_headers,
            json=[{"user_id": user_id, "role": "member"}],
            timeout=30,
        )
        if resp.status_code != 200:
            errors.append(f"group {group_id} failed ({resp.status_code}): {resp.text}")
    if errors:
        return False, "; ".join(errors)
    return True, ""


def create_project(base_url: str, admin_headers: dict, name: str) -> tuple[str | None, str]:
    resp = request_with_retry(
        "POST",
        f"{base_url}/projects",
        headers=admin_headers,
        json={"name": name},
        timeout=30,
    )
    if resp.status_code != 200:
        return None, f"project creation failed ({resp.status_code}): {resp.text}"
    return resp.json()["id"], ""


def add_project_owner(base_url: str, admin_headers: dict, project_id: str, user_id: str) -> tuple[bool, str]:
    resp = request_with_retry(
        "POST",
        f"{base_url}/projects/{project_id}/users",
        headers=admin_headers,
        json=[{"user_id": user_id, "role": "owner"}],
        timeout=30,
    )
    if resp.status_code != 200:
        return False, f"project owner assignment failed ({resp.status_code}): {resp.text}"
    return True, ""


def process_row(base_url: str, admin_headers: dict, default_role: str, shared_password: str, row: dict) -> dict:
    email = row["email"].strip().lower()
    first_name = row.get("first_name", "").strip()
    last_name = row.get("last_name", "").strip()
    role = (row.get("role") or default_role).strip()
    group_ids = [g.strip() for g in (row.get("group_ids") or "").split(";") if g.strip()]
    participant_number = row.get("participant_number", "").strip()
    project_name = f"project-{participant_number}" if participant_number else email.split("@")[0]

    result = {
        "email": email,
        "status": "failed",
        "user_id": "",
        "role": role,
        "project_id": "",
        "error": "",
    }

    # Anything unexpected here (network blips, a bug, an unexpected response shape) is
    # recorded as a failure for this one row instead of crashing the whole batch run.
    try:
        errors = []

        signup_token, message = create_signup_link(base_url, admin_headers, email)
        if not signup_token:
            result["error"] = message
            return result
        time.sleep(REQUEST_DELAY_SECONDS)

        ok, error = complete_signup(base_url, signup_token, email, shared_password, first_name, last_name)
        if not ok:
            result["error"] = error
            return result
        time.sleep(REQUEST_DELAY_SECONDS)

        user_id = find_org_user_id(base_url, admin_headers, email)
        if not user_id:
            result["error"] = "user created but could not be found afterwards via /users/all"
            return result
        result["user_id"] = user_id

        if role != "read_only":
            ok, error = set_role(base_url, admin_headers, user_id, role)
            if not ok:
                errors.append(error)

        if group_ids:
            ok, error = add_to_groups(base_url, admin_headers, user_id, group_ids)
            if not ok:
                errors.append(error)

        project_id, error = create_project(base_url, admin_headers, project_name)
        if not project_id:
            errors.append(error)
        else:
            result["project_id"] = project_id
            ok, error = add_project_owner(base_url, admin_headers, project_id, user_id)
            if not ok:
                errors.append(error)

        result["status"] = "created" if not errors else "partial"
        result["error"] = "; ".join(errors)
        return result
    except Exception as exc:
        # A row that already got as far as creating the user (user_id set) is "partial",
        # not "failed" - the account exists, so it must not go into failed-users.csv.
        result["status"] = "partial" if result["user_id"] else "failed"
        result["error"] = f"unexpected error: {exc}"
        return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input-csv", default="users.csv", help="CSV with columns: email,first_name,last_name,role,group_ids")
    parser.add_argument("--output-csv", default="results.csv", help="Where to write per-user results")
    parser.add_argument(
        "--failed-csv",
        default="failed-users.csv",
        help="Where to write the original rows for users that were NOT created, for easy retrying",
    )
    parser.add_argument("--env-file", default=".env", help="Path to the .env file with credentials")
    args = parser.parse_args()

    load_env_file(args.env_file)

    base_url = os.environ.get("GALILEO_BASE_URL", "").rstrip("/")
    admin_token = os.environ.get("GALILEO_ADMIN_TOKEN")
    admin_email = os.environ.get("GALILEO_ADMIN_EMAIL")
    admin_password = os.environ.get("GALILEO_ADMIN_PASSWORD")
    shared_password = os.environ.get("GALILEO_USER_PASSWORD")
    default_role = os.environ.get("GALILEO_DEFAULT_ROLE", "read_only")

    if not base_url:
        parser.error("GALILEO_BASE_URL is required (set it in your .env file)")
    if not shared_password:
        parser.error("GALILEO_USER_PASSWORD is required (set it in your .env file)")
    if not admin_token and not (admin_email and admin_password):
        parser.error("Set GALILEO_ADMIN_TOKEN, or both GALILEO_ADMIN_EMAIL and GALILEO_ADMIN_PASSWORD, in your .env file")

    token = admin_token or get_admin_token(base_url, admin_email, admin_password)
    admin_headers = {"Authorization": f"Bearer {token}"}

    with open(args.input_csv, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        input_fieldnames = reader.fieldnames or ["email", "first_name", "last_name", "role", "group_ids"]
        rows = list(reader)

    if not rows:
        print("Input CSV has no rows.", file=sys.stderr)
        return 1

    counts = {"created": 0, "partial": 0, "failed": 0}
    processed = 0

    with (
        open(args.output_csv, "w", newline="") as out_f,
        open(args.failed_csv, "w", newline="") as failed_f,
    ):
        results_writer = csv.DictWriter(out_f, fieldnames=["email", "status", "user_id", "role", "project_id", "error"])
        results_writer.writeheader()
        out_f.flush()

        failed_writer = csv.DictWriter(failed_f, fieldnames=input_fieldnames)
        failed_writer.writeheader()
        failed_f.flush()

        try:
            for i, row in enumerate(rows, start=1):
                email = row.get("email", "").strip()
                if not email:
                    print(f"Row {i}: missing email, skipping", file=sys.stderr)
                    continue
                print(f"[{i}/{len(rows)}] creating {email} ...")
                result = process_row(base_url, admin_headers, default_role, shared_password, row)
                processed += 1
                counts[result["status"]] += 1

                results_writer.writerow(result)
                out_f.flush()
                if result["status"] == "failed":
                    failed_writer.writerow(row)
                    failed_f.flush()

                print(f"    -> {result['status']}" + (f" ({result['error']})" if result["error"] else ""))

                if i < len(rows):
                    time.sleep(ROW_DELAY_SECONDS)
        except KeyboardInterrupt:
            print(
                f"\nInterrupted after {processed}/{len(rows)} rows - results so far are saved "
                f"in {args.output_csv} and {args.failed_csv}.",
                file=sys.stderr,
            )
            return 130

    print(
        f"\nDone: {counts['created']} created, {counts['partial']} partial, "
        f"{counts['failed']} failed (out of {processed} processed)."
    )
    print(f"Results written to {args.output_csv}. All created users share the password set in {args.env_file}.")
    if counts["failed"]:
        print(f"{counts['failed']} row(s) that failed to create a user were written to {args.failed_csv}.")
        print(f"Retry them with: python {os.path.basename(__file__)} --input-csv {args.failed_csv}")
    if counts["partial"]:
        print(
            f"{counts['partial']} row(s) were created but hit a problem afterward (role/group/project) - "
            f"see the 'partial' rows in {args.output_csv} and fix those manually, they are not in {args.failed_csv}."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
