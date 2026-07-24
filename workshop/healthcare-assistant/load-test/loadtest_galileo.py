#!/usr/bin/env python3
"""
Galileo console load test using headless Playwright/Chromium.

For each user in users.csv, drives the following flow concurrently:

  1. Sign in to the Galileo console
  2. Click their assigned project  (project-{participant_number})
  3. Click the "default" log stream
  4. Click "Configure Metrics", enable Correctness + Context Adherence, click Apply
  5. Click "Compute" on the confirmation dialog
  6. Measure how long it takes for metric values to appear (i.e. "Computing" clears)
  7. Click into the first trace in the list

Credentials:
  Users:    --users-csv  (email + participant_number columns)
  Password: GALILEO_USER_PASSWORD in --env-file  (shared across all users)
  Console:  GALILEO_CONSOLE_URL   in --env-file

SETUP
-----
    pip install playwright
    playwright install chromium

USAGE
-----
    # Full run
    python loadtest_galileo.py --users-csv ../workshop-setup/users.csv

    # Preview without opening any browsers
    python loadtest_galileo.py --users-csv ../workshop-setup/users.csv --dry-run

    # Show the browser for debugging selector issues
    python loadtest_galileo.py --users-csv ../workshop-setup/users.csv --headed --max-concurrency 1

SELECTOR NOTES
--------------
Galileo's console UI is a React SPA. The selectors below use ARIA roles and
visible text where possible, which survive minor DOM restructuring. If the script
fails partway through a step, run with --headed --max-concurrency 1 to visually
inspect the page and adjust the relevant helper function.
"""

import argparse
import asyncio
import csv
import os
import sys
import time

from playwright.async_api import Browser, BrowserContext, Page, async_playwright

# ── Timeouts ──────────────────────────────────────────────────────────────────
SIGNIN_TIMEOUT_MS = 45_000
NAV_TIMEOUT_MS = 30_000
METRICS_COMPUTE_TIMEOUT_MS = 300_000  # 5 min — server-side computation can be slow


# ── .env loader (same pattern as workshop-setup scripts) ──────────────────────
def load_env_file(path: str) -> None:
    if not os.path.exists(path):
        return
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


# ── Logging ───────────────────────────────────────────────────────────────────

def make_logger(row_num: int, email: str):
    """Return a log(msg) callable that prefixes every line with the row/email."""
    prefix = f"[row {row_num:>3}][{email}]"
    def log(msg: str) -> None:
        print(f"{prefix} {msg}", flush=True)
    return log


# ── Retry helper ──────────────────────────────────────────────────────────────

async def retry_click(
    locator,
    page: Page,
    success_selector: str,
    *,
    log=None,
    retries: int = 4,
    retry_delay_ms: int = 1500,
    success_timeout_ms: int = 8_000,
    force: bool = False,
) -> None:
    """Click `locator` and wait for `success_selector` to appear, retrying if it doesn't.

    SPAs often attach React event handlers asynchronously after an element becomes
    visible, so a click that lands too early does nothing. Retrying with a short
    delay between attempts handles this reliably without arbitrary fixed sleeps.
    """
    last_exc: Exception | None = None
    for attempt in range(retries):
        if attempt > 0 and log:
            log(f"  retrying (attempt {attempt + 1}/{retries})...")
        try:
            await locator.click(force=force, timeout=NAV_TIMEOUT_MS)
            await page.wait_for_selector(success_selector, timeout=success_timeout_ms)
            return
        except Exception as exc:
            last_exc = exc
            if attempt < retries - 1:
                await page.wait_for_timeout(retry_delay_ms)
    raise last_exc  # all attempts exhausted


# ── Individual UI steps ────────────────────────────────────────────────────────

async def sign_in(page: Page, console_url: str, email: str, password: str, log) -> None:
    log(f"navigating to {console_url}")
    await page.goto(console_url, timeout=SIGNIN_TIMEOUT_MS)

    log("filling sign-in form")
    await page.locator(
        'input[type="email"], input[name="email"], input[placeholder*="email" i]'
    ).first.fill(email)
    await page.locator('input[type="password"]').first.fill(password)

    log("submitting sign-in form")
    await page.locator(
        'button[type="submit"], button:has-text("Sign in"), button:has-text("Log in")'
    ).first.click()

    # wait_for_selector only accepts plain CSS; use locator().or_() to also
    # match by visible text without mixing selector syntaxes.
    await (
        page.locator('[data-testid*="project"], [class*="project"]')
        .or_(page.get_by_text("Projects", exact=True))
    ).first.wait_for(state="visible", timeout=SIGNIN_TIMEOUT_MS)
    log("sign-in successful, projects list visible")


async def open_project(page: Page, project_name: str, log) -> None:
    log(f"clicking project '{project_name}'")
    await retry_click(
        page.get_by_text(project_name, exact=True).first,
        page,
        "tr[data-with-row-border]",
        log=log,
    )
    log(f"project '{project_name}' opened")


async def open_log_stream(page: Page, log, stream_name: str = "default") -> None:
    first_td = (
        page.locator("tr[data-with-row-border]")
        .filter(has_text=stream_name)
        .first.locator("td")
        .first
    )
    log(f"waiting for '{stream_name}' log stream row to be visible")
    await first_td.wait_for(state="visible", timeout=NAV_TIMEOUT_MS)

    log(f"clicking '{stream_name}' log stream row")
    await retry_click(
        first_td,
        page,
        'button:has-text("Configure Metrics")',
        log=log,
        force=True,
    )
    log(f"log stream '{stream_name}' opened")


async def _enable_toggle(page: Page, label: str, log) -> None:
    """Enable a metric toggle by its display name if it is not already on.

    Mantine Switch hides the native <input> off-screen with CSS, so Playwright's
    is_checked() and click(force=True) both fail. We read .checked via JS (which
    ignores visibility) and click the parent <label> (the visible element that
    the browser uses to toggle the underlying checkbox).
    """
    log(f"  waiting for '{label}' toggle to attach")
    toggle = page.locator(f'input[aria-label="Enable {label} metric"]')
    await toggle.wait_for(state="attached", timeout=NAV_TIMEOUT_MS)

    is_checked = await toggle.evaluate("el => el.checked")
    if is_checked:
        log(f"  '{label}' already enabled, skipping")
        return

    log(f"  enabling '{label}'")
    await toggle.locator("xpath=..").click()

    # Confirm the toggle actually flipped before moving on
    await page.wait_for_function(
        f"() => !!document.querySelector('input[aria-label=\"Enable {label} metric\"]')?.checked",
        timeout=5_000,
    )
    log(f"  '{label}' enabled")


async def configure_metrics(page: Page, log) -> None:
    # One-way navigation — do not use retry_click here. Retrying would try to
    # re-click "Configure Metrics" after we've already navigated away from it.
    log("clicking 'Configure Metrics' button")
    await page.get_by_role("button", name="Configure Metrics").click(timeout=NAV_TIMEOUT_MS)

    # Wait for the page heading — "Configure metrics for default" is unique to this page.
    # wait_for_selector only takes CSS, so we use get_by_text().wait_for() instead.
    log("waiting for metrics configuration page to load")
    await page.get_by_text("Configure metrics for", exact=False).wait_for(
        state="visible", timeout=NAV_TIMEOUT_MS
    )
    log("metrics configuration page loaded")

    await _enable_toggle(page, "Correctness", log)
    await _enable_toggle(page, "Context Adherence", log)

    log("clicking 'Apply'")
    await page.get_by_role("button", name="Apply").click(timeout=NAV_TIMEOUT_MS)

    # The dialog appears on top of the metrics page, so the "Configure metrics for"
    # heading is still visible in the background — we can't wait for it to disappear.
    # Wait for the dialog itself instead.
    await page.wait_for_selector(
        '[role="dialog"], [role="alertdialog"]', timeout=NAV_TIMEOUT_MS
    )
    log("Compute dialog visible")


async def compute_and_measure(page: Page, log) -> float:
    """Click Compute in the confirmation dialog and measure how long metrics take to resolve."""
    log("waiting for 'Compute' button inside dialog")
    dialog = page.locator('[role="dialog"], [role="alertdialog"]').first
    compute_btn = dialog.get_by_role("button", name="Compute")
    await compute_btn.wait_for(state="visible", timeout=NAV_TIMEOUT_MS)
    log("clicking 'Compute'")
    # force=True bypasses any Mantine overlay that sits above the button
    await compute_btn.click(force=True, timeout=NAV_TIMEOUT_MS)
    log("'Compute' clicked — waiting for 'Computing' status to appear")
    t0 = time.monotonic()

    # Step 1: wait for "computing" to appear on the page (confirms the job started).
    # Allow up to 15s; if it never appears the job may have completed instantly.
    try:
        await page.wait_for_function(
            "() => document.body.innerText.toLowerCase().includes('computing')",
            timeout=15_000,
        )
        log("'Computing' status visible, waiting for it to resolve...")
    except Exception:
        log("'Computing' status never appeared — may have resolved immediately")

    # Step 2: wait for "computing" to clear
    await page.wait_for_function(
        "() => !document.body.innerText.toLowerCase().includes('computing')",
        timeout=METRICS_COMPUTE_TIMEOUT_MS,
    )

    elapsed = time.monotonic() - t0
    log(f"metrics resolved in {elapsed:.1f}s")
    return elapsed


async def click_first_trace(page: Page, log) -> None:
    log("clicking first trace")
    url_before = page.url
    first_row = page.locator(
        'table tbody tr, [data-testid*="trace-row"], [role="row"]:not([role="columnheader"])'
    ).first
    await first_row.click(timeout=NAV_TIMEOUT_MS)
    # Wait for the URL to change — trace detail pages have a unique URL with a trace ID.
    # This avoids networkidle, which never settles on this WebSocket-heavy SPA.
    await page.wait_for_url(lambda url: url != url_before, timeout=NAV_TIMEOUT_MS)
    log(f"trace detail view loaded: {page.url}")


# ── Per-user orchestration ─────────────────────────────────────────────────────

async def run_scenario(
    browser: Browser,
    console_url: str,
    email: str,
    password: str,
    project_name: str,
    row_num: int,
    sem: asyncio.Semaphore,
    headed: bool,
) -> dict:
    result: dict = {
        "row": row_num,
        "email": email,
        "project": project_name,
        "status": "failed",
        "compute_time_s": "",
        "total_duration_s": 0.0,
        "error": "",
    }
    wall_start = time.monotonic()

    async with sem:
        context: BrowserContext = await browser.new_context()
        page: Page = await context.new_page()

        log = make_logger(row_num, email)

        # Surface console errors in --headed / debug mode
        if headed:
            page.on("console", lambda msg: print(f"  [browser] {msg.type}: {msg.text}") if msg.type == "error" else None)

        try:
            await sign_in(page, console_url, email, password, log)
            await open_project(page, project_name, log)
            await open_log_stream(page, log)
            await configure_metrics(page, log)
            compute_s = await compute_and_measure(page, log)
            result["compute_time_s"] = round(compute_s, 1)
            await click_first_trace(page, log)
            result["status"] = "success"

        except Exception as exc:
            result["error"] = str(exc)
            if headed:
                # Pause so the developer can inspect the page before it closes
                await page.pause()
        finally:
            await page.close()
            await context.close()

    result["total_duration_s"] = round(time.monotonic() - wall_start, 1)
    label = "OK  " if result["status"] == "success" else "FAIL"
    compute_info = (
        f"  compute={result['compute_time_s']}s" if result["compute_time_s"] != "" else ""
    )
    print(
        f"[{label}] row {row_num:>3}  {email}  {project_name}{compute_info}"
        + (f"\n       {result['error']}" if result["error"] else "")
    )
    return result


# ── Main ───────────────────────────────────────────────────────────────────────

async def main_async(
    rows: list[dict],
    console_url: str,
    password: str,
    max_concurrency: int,
    output_csv: str,
    headed: bool,
) -> int:
    sem = asyncio.Semaphore(max_concurrency)

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=not headed)
        tasks = [
            run_scenario(
                browser,
                console_url,
                row["email"],
                password,
                f"project-{row['participant_number']}",
                i + 1,
                sem,
                headed,
            )
            for i, row in enumerate(rows)
        ]
        results = await asyncio.gather(*tasks)
        await browser.close()

    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "row", "email", "project", "status",
                "compute_time_s", "total_duration_s", "error",
            ],
        )
        writer.writeheader()
        writer.writerows(results)

    passed = sum(1 for r in results if r["status"] == "success")
    failed = len(results) - passed

    compute_times = [
        r["compute_time_s"] for r in results
        if isinstance(r["compute_time_s"], (int, float))
    ]
    if compute_times:
        avg_s = round(sum(compute_times) / len(compute_times), 1)
        max_s = round(max(compute_times), 1)
        min_s = round(min(compute_times), 1)
        print(f"\nMetric compute time — min: {min_s}s  avg: {avg_s}s  max: {max_s}s")

    print(f"Done: {passed}/{len(results)} passed, {failed} failed.")
    print(f"Results written to {output_csv}.")
    return 0 if not failed else 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--users-csv",
        default="../workshop-setup/users.csv",
        metavar="FILE",
        help="CSV with email and participant_number columns (default: ../workshop-setup/users.csv)",
    )
    parser.add_argument(
        "--output-csv",
        default="galileo_loadtest_results.csv",
        help="Where to write per-user results (default: galileo_loadtest_results.csv)",
    )
    parser.add_argument(
        "--env-file",
        default=".env",
        help="Path to .env with GALILEO_CONSOLE_URL and GALILEO_USER_PASSWORD (default: .env)",
    )
    parser.add_argument(
        "--max-concurrency",
        type=int,
        default=20,
        help="Max simultaneous browser sessions (default: 20)",
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Run with a visible browser window (use with --max-concurrency 1 for debugging)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be tested without opening any browsers",
    )
    args = parser.parse_args()

    load_env_file(args.env_file)
    console_url = os.environ.get("GALILEO_CONSOLE_URL", "").rstrip("/")
    password = os.environ.get("GALILEO_USER_PASSWORD", "")

    if not console_url:
        print("GALILEO_CONSOLE_URL is required (set it in .env).", file=sys.stderr)
        return 1
    if not password:
        print("GALILEO_USER_PASSWORD is required (set it in .env).", file=sys.stderr)
        return 1

    rows: list[dict] = []
    with open(args.users_csv, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            email = row.get("email", "").strip()
            participant_number = row.get("participant_number", "").strip()
            if email and participant_number:
                rows.append({"email": email, "participant_number": participant_number})

    if not rows:
        print("No valid rows (email + participant_number) found in users CSV.", file=sys.stderr)
        return 1

    if args.dry_run:
        print(f"[dry run] Would test {len(rows)} user(s) against {console_url}:")
        for i, row in enumerate(rows, 1):
            print(f"  {i:>3}. {row['email']}  →  project-{row['participant_number']}")
        return 0

    print(
        f"Running Galileo load test: {len(rows)} user(s), "
        f"max_concurrency={args.max_concurrency}, console={console_url}"
    )
    return asyncio.run(
        main_async(rows, console_url, password, args.max_concurrency, args.output_csv, args.headed)
    )


if __name__ == "__main__":
    raise SystemExit(main())
