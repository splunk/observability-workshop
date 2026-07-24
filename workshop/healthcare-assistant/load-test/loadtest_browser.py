#!/usr/bin/env python3
"""
Headless browser load test for the healthcare assistant workshop.

For each instance listed in the CSV, opens a headless browser concurrently and
drives the standard workshop flow:

  1. Navigate to the app (http://host:81)
  2. Click the "What is the dosage and common side effects of Lisinopril?" button
  3. Wait for the assistant's response
  4. Click the "Can you look up information for patient P001?" button
  5. Wait for the assistant's response
  6. Click "Log Hallucination" in the sidebar and wait for it to complete

The two questions match the built-in example-query buttons in the Streamlit UI,
so they are triggered via button clicks rather than typed into the chat input —
this is more reliable since it avoids timing issues with the chat input submit.

CSV format (comma-separated with header row, same as loadtest-install-app.sh):
  adminUsername,sshPass,sshUrl,sshPassword,ssh,o11yCloudID,url,adminPassword

The `url` column supplies the app endpoint (e.g. http://i-xxx.splunk.show:81).

SETUP
-----
    pip install playwright
    playwright install chromium

USAGE
-----
    python loadtest_browser.py --csv instances.csv
    python loadtest_browser.py --csv instances.csv --max-concurrency 25
    python loadtest_browser.py --csv instances.csv --dry-run
"""

import argparse
import asyncio
import csv
import sys
import time

from playwright.async_api import Browser, BrowserContext, Page, async_playwright

# Partial text used to locate the two example query buttons in the UI
BUTTON_Q1 = "Lisinopril"
BUTTON_Q2 = "P001"

APP_LOAD_TIMEOUT_MS = 30_000   # time to wait for the app to be ready on page load
RESPONSE_TIMEOUT_MS = 120_000  # time to wait for each LLM response (2 min)
HALLUCINATION_TIMEOUT_MS = 30_000


async def wait_for_chat_messages(page: Page, min_count: int, timeout_ms: int) -> None:
    """
    Poll until the page has at least `min_count` stChatMessage elements
    and 'Thinking...' is no longer visible (response is complete, not in-progress).
    """
    await page.wait_for_function(
        f"""() => {{
            const msgs = document.querySelectorAll('[data-testid="stChatMessage"]');
            return msgs.length >= {min_count} && !document.body.innerText.includes('Thinking...');
        }}""",
        timeout=timeout_ms,
    )


async def run_scenario(
    browser: Browser, url: str, row_num: int, sem: asyncio.Semaphore
) -> dict:
    result: dict = {
        "row": row_num,
        "url": url,
        "status": "failed",
        "duration_s": 0.0,
        "error": "",
    }
    start = time.monotonic()

    async with sem:
        context: BrowserContext = await browser.new_context()
        page: Page = await context.new_page()
        try:
            # ── Step 1: load the app ──────────────────────────────────────────
            await page.goto(url, timeout=APP_LOAD_TIMEOUT_MS)
            await page.wait_for_selector(
                f'button:has-text("{BUTTON_Q1}")', timeout=APP_LOAD_TIMEOUT_MS
            )

            # ── Step 2 & 3: question 1 → wait for response ───────────────────
            # Initial message count is 0; after Q1 completes: 2 (user + assistant).
            # The combined condition (count >= 2 AND no "Thinking...") correctly
            # waits through the intermediate "Thinking..." rerun state.
            await page.click(f'button:has-text("{BUTTON_Q1}")')
            await wait_for_chat_messages(page, min_count=2, timeout_ms=RESPONSE_TIMEOUT_MS)

            # ── Step 4 & 5: question 2 → wait for response ───────────────────
            # After Q2 completes: 4 messages total (2 more user + assistant).
            await page.click(f'button:has-text("{BUTTON_Q2}")')
            await wait_for_chat_messages(page, min_count=4, timeout_ms=RESPONSE_TIMEOUT_MS)

            # ── Step 6: log the hallucination ────────────────────────────────
            # "Log Hallucination" is in the sidebar. On success, the app appends
            # a hallucinated Q&A pair to the chat (2 more messages → total 6).
            await page.click('button:has-text("Log Hallucination")')
            await wait_for_chat_messages(
                page, min_count=6, timeout_ms=HALLUCINATION_TIMEOUT_MS
            )

            result["status"] = "success"

        except Exception as exc:
            result["error"] = str(exc)
        finally:
            await page.close()
            await context.close()

    result["duration_s"] = round(time.monotonic() - start, 1)
    label = "OK  " if result["status"] == "success" else "FAIL"
    print(
        f"[{label}] row {row_num:>3}  {url}  ({result['duration_s']}s)"
        + (f"\n       {result['error']}" if result["error"] else "")
    )
    return result


async def main_async(urls: list[str], max_concurrency: int, output_csv: str) -> int:
    sem = asyncio.Semaphore(max_concurrency)

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        tasks = [
            run_scenario(browser, url, i + 1, sem) for i, url in enumerate(urls)
        ]
        results = await asyncio.gather(*tasks)
        await browser.close()

    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["row", "url", "status", "duration_s", "error"]
        )
        writer.writeheader()
        writer.writerows(results)

    passed = sum(1 for r in results if r["status"] == "success")
    failed = len(results) - passed
    print(f"\nDone: {passed}/{len(results)} passed, {failed} failed.")
    print(f"Results written to {output_csv}.")
    return 0 if not failed else 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--csv", required=True, metavar="FILE",
        help="Instance CSV (same format as loadtest-install-app.sh)"
    )
    parser.add_argument(
        "--output-csv", default="loadtest_results.csv",
        help="Where to write per-instance results (default: loadtest_results.csv)"
    )
    parser.add_argument(
        "--max-concurrency", type=int, default=50,
        help="Max simultaneous browser sessions (default: 50; tune down if memory-constrained)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print the URLs that would be tested without opening any browsers"
    )
    args = parser.parse_args()

    urls: list[str] = []
    with open(args.csv, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            url = row.get("url", "").strip()
            if url:
                urls.append(url)

    if not urls:
        print("No URLs found in the 'url' column of the CSV.", file=sys.stderr)
        return 1

    if args.dry_run:
        print(f"[dry run] Would test {len(urls)} instance(s):")
        for i, url in enumerate(urls, 1):
            print(f"  {i:>3}. {url}")
        return 0

    print(
        f"Running load test: {len(urls)} instance(s), "
        f"max_concurrency={args.max_concurrency}"
    )
    return asyncio.run(main_async(urls, args.max_concurrency, args.output_csv))


if __name__ == "__main__":
    raise SystemExit(main())
