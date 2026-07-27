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
import os
import sys
import time

from playwright.async_api import Browser, BrowserContext, Page, async_playwright

# Partial text used to locate the two example query buttons in the UI
BUTTON_Q1 = "Lisinopril"
BUTTON_Q2 = "P001"
BUTTON_Q1_LABEL = "What is the dosage and common side effects of Lisinopril?"
BUTTON_Q2_LABEL = "Can you look up information for patient P001?"
BUTTON_HALLUCINATION = "Log Hallucination"

APP_LOAD_TIMEOUT_MS = 30_000   # time to wait for the app to be ready on page load
RESPONSE_TIMEOUT_MS = 120_000  # time to wait for each LLM response (2 min)
HALLUCINATION_TIMEOUT_MS = 30_000
CLICK_ACK_TIMEOUT_MS = 15_000  # time to wait for a click to register in the UI

STEP_RETRIES = 4
STEP_RETRY_DELAY_MS = 1_500

RESULT_FIELDS = [
    "row", "url", "status", "failed_step", "duration_s", "error", "screenshot",
]

_BROWSER_ARGS = [
    "--disable-dev-shm-usage",
    "--disable-gpu",
]


def make_logger(row_num: int, url: str):
    """Return a log(msg) callable that prefixes every line with row/url."""
    prefix = f"[row {row_num:>3}][{url}]"
    def log(msg: str) -> None:
        print(f"{prefix} {msg}", flush=True)
    return log


async def count_chat_messages(page: Page) -> int:
    return await page.locator('[data-testid="stChatMessage"]').count()


async def wait_for_app_idle(page: Page, timeout_ms: int = APP_LOAD_TIMEOUT_MS) -> None:
    """Wait until Streamlit is not mid-rerun (no in-progress indicators)."""
    await page.wait_for_function(
        """() => {
            const text = document.body.innerText;
            return !text.includes('Thinking...')
                && !text.includes('Logging hallucination');
        }""",
        timeout=timeout_ms,
    )


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


async def _verify_button_ready(page: Page, locator, label: str, log) -> None:
    await locator.wait_for(state="visible", timeout=APP_LOAD_TIMEOUT_MS)
    if not await locator.is_enabled():
        raise RuntimeError(f"button not enabled: {label}")
    log(f"button ready: {label}")


async def _verify_click_registered(
    page: Page, count_before: int, log, *, allow_thinking: bool = True,
) -> None:
    """Confirm the UI reacted to a click (rerun started or message count increased)."""
    await page.wait_for_function(
        f"""() => {{
            const text = document.body.innerText;
            const msgs = document.querySelectorAll('[data-testid="stChatMessage"]').length;
            const thinking = text.includes('Thinking...');
            const logging = text.includes('Logging hallucination');
            if (msgs > {count_before}) return true;
            if (logging) return true;
            return {'true' if allow_thinking else 'false'} && thinking;
        }}""",
        timeout=CLICK_ACK_TIMEOUT_MS,
    )
    log("click registered — app is processing")


async def click_example_query(
    page: Page,
    button_subtext: str,
    button_label: str,
    log,
    *,
    expect_min_messages: int,
) -> None:
    """Click an example-query button and verify the assistant response completes."""
    await wait_for_app_idle(page)

    count_before = await count_chat_messages(page)
    log(
        f"step: {button_label} — {count_before} message(s) before click "
        f"(expect >={expect_min_messages} after response)"
    )

    btn = page.locator("button").filter(has_text=button_subtext).first
    last_exc: Exception | None = None

    for attempt in range(STEP_RETRIES):
        if attempt > 0:
            log(f"  retrying {button_label} (attempt {attempt + 1}/{STEP_RETRIES})...")
            await wait_for_app_idle(page, timeout_ms=RESPONSE_TIMEOUT_MS)

        try:
            await _verify_button_ready(page, btn, button_label, log)
            await btn.click(force=True, timeout=APP_LOAD_TIMEOUT_MS)
            log(f"clicked: {button_label}")

            await _verify_click_registered(page, count_before, log)
            await wait_for_chat_messages(
                page, expect_min_messages, timeout_ms=RESPONSE_TIMEOUT_MS,
            )

            count_after = await count_chat_messages(page)
            if count_after < expect_min_messages:
                raise RuntimeError(
                    f"expected >={expect_min_messages} messages after response, got {count_after}"
                )
            log(
                f"verified: {button_label} — response complete "
                f"({count_after} message(s))"
            )
            return
        except Exception as exc:
            last_exc = exc
            if attempt < STEP_RETRIES - 1:
                await page.wait_for_timeout(STEP_RETRY_DELAY_MS)

    raise last_exc or RuntimeError(f"failed to complete step: {button_label}")


async def click_log_hallucination(
    page: Page, log, *, expect_min_messages: int = 6,
) -> None:
    """Click Log Hallucination and verify new chat messages appear."""
    await wait_for_app_idle(page)

    count_before = await count_chat_messages(page)
    log(
        f"step: {BUTTON_HALLUCINATION} — {count_before} message(s) before click "
        f"(expect >={expect_min_messages} after)"
    )

    btn = page.get_by_role("button", name=BUTTON_HALLUCINATION, exact=True)
    last_exc: Exception | None = None

    for attempt in range(STEP_RETRIES):
        if attempt > 0:
            log(
                f"  retrying {BUTTON_HALLUCINATION} "
                f"(attempt {attempt + 1}/{STEP_RETRIES})..."
            )
            await wait_for_app_idle(page, timeout_ms=HALLUCINATION_TIMEOUT_MS)

        try:
            await _verify_button_ready(page, btn, BUTTON_HALLUCINATION, log)
            await btn.click(force=True, timeout=APP_LOAD_TIMEOUT_MS)
            log(f"clicked: {BUTTON_HALLUCINATION}")

            await _verify_click_registered(
                page, count_before, log, allow_thinking=False,
            )
            await page.wait_for_function(
                f"""() => {{
                    const text = document.body.innerText;
                    if (text.includes('Logging hallucination')) return false;
                    const msgs = document.querySelectorAll(
                        '[data-testid="stChatMessage"]'
                    ).length;
                    return msgs >= {expect_min_messages};
                }}""",
                timeout=HALLUCINATION_TIMEOUT_MS,
            )

            count_after = await count_chat_messages(page)
            if count_after < expect_min_messages:
                raise RuntimeError(
                    f"expected >={expect_min_messages} messages after hallucination, "
                    f"got {count_after}"
                )
            log(
                f"verified: {BUTTON_HALLUCINATION} — complete "
                f"({count_after} message(s))"
            )
            return
        except Exception as exc:
            last_exc = exc
            if attempt < STEP_RETRIES - 1:
                await page.wait_for_timeout(STEP_RETRY_DELAY_MS)

    raise last_exc or RuntimeError(f"failed to complete step: {BUTTON_HALLUCINATION}")


async def save_failure_screenshot(
    page: Page, screenshot_dir: str, row_num: int, step: str, log,
) -> str:
    os.makedirs(screenshot_dir, exist_ok=True)
    path = os.path.join(screenshot_dir, f"row-{row_num:03d}-{step}.png")
    try:
        await page.screenshot(path=path, full_page=True)
        log(f"screenshot saved: {path}")
        return path
    except Exception as exc:
        log(f"screenshot failed: {exc}")
        return ""


async def run_scenario(
    browser: Browser,
    url: str,
    row_num: int,
    sem: asyncio.Semaphore,
    headed: bool,
    screenshot_dir: str | None,
) -> dict:
    result: dict = {
        "row": row_num,
        "url": url,
        "status": "failed",
        "failed_step": "",
        "duration_s": 0.0,
        "error": "",
        "screenshot": "",
    }
    start = time.monotonic()
    failed_step = ""
    log = make_logger(row_num, url)

    async with sem:
        context: BrowserContext = await browser.new_context()
        page: Page = await context.new_page()

        if headed:
            page.on(
                "console",
                lambda msg: print(f"  [browser] {msg.type}: {msg.text}")
                if msg.type == "error" else None,
            )

        try:
            failed_step = "load_app"
            log("navigating to app")
            await page.goto(url, timeout=APP_LOAD_TIMEOUT_MS)
            await page.locator("button").filter(has_text=BUTTON_Q1).first.wait_for(
                state="visible", timeout=APP_LOAD_TIMEOUT_MS,
            )
            await wait_for_app_idle(page)
            log("app loaded — example query buttons visible")

            failed_step = "query_lisinopril"
            await click_example_query(
                page, BUTTON_Q1, BUTTON_Q1_LABEL, log, expect_min_messages=2,
            )

            failed_step = "query_p001"
            await click_example_query(
                page, BUTTON_Q2, BUTTON_Q2_LABEL, log, expect_min_messages=4,
            )

            failed_step = "log_hallucination"
            await click_log_hallucination(page, log, expect_min_messages=6)

            result["status"] = "success"
            log("all 3 actions completed successfully")

        except Exception as exc:
            result["failed_step"] = failed_step
            result["error"] = str(exc)
            if screenshot_dir:
                result["screenshot"] = await save_failure_screenshot(
                    page, screenshot_dir, row_num, failed_step or "error", log,
                )
            if headed:
                await page.pause()
        finally:
            await page.close()
            await context.close()

    result["duration_s"] = round(time.monotonic() - start, 1)
    label = "OK  " if result["status"] == "success" else "FAIL"
    step_info = f"  step={result['failed_step']}" if result["failed_step"] else ""
    print(
        f"[{label}] row {row_num:>3}  {url}  ({result['duration_s']}s){step_info}"
        + (f"\n       {result['error'][:200]}" if result["error"] else "")
    )
    return result


async def main_async(
    urls: list[str],
    max_concurrency: int,
    output_csv: str,
    headed: bool,
    screenshot_dir: str | None,
) -> int:
    sem = asyncio.Semaphore(max_concurrency)

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=not headed,
            args=_BROWSER_ARGS,
        )
        tasks = [
            run_scenario(browser, url, i + 1, sem, headed, screenshot_dir)
            for i, url in enumerate(urls)
        ]
        results = await asyncio.gather(*tasks)
        await browser.close()

    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=RESULT_FIELDS)
        writer.writeheader()
        writer.writerows(results)

    passed = sum(1 for r in results if r["status"] == "success")
    failed = len(results) - passed

    if failed:
        by_step: dict[str, int] = {}
        for r in results:
            if r["status"] == "failed" and r["failed_step"]:
                by_step[r["failed_step"]] = by_step.get(r["failed_step"], 0) + 1
        if by_step:
            print("Failures by step:", ", ".join(f"{k}={v}" for k, v in sorted(by_step.items())))

    print(f"\nDone: {passed}/{len(results)} passed, {failed} failed.")
    print(f"Results written to {output_csv}.")
    if screenshot_dir and failed:
        print(f"Failure screenshots in {screenshot_dir}/")
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
        "--headed", action="store_true",
        help="Run browsers in headed mode (visible window) for debugging"
    )
    parser.add_argument(
        "--screenshot-dir",
        default="browser_failure_screenshots",
        metavar="DIR",
        help=(
            "Directory for PNG screenshots on failure "
            "(default: browser_failure_screenshots). Pass empty string to disable."
        ),
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

    screenshot_dir = args.screenshot_dir.strip() or None

    if args.dry_run:
        print(f"[dry run] Would test {len(urls)} instance(s):")
        for i, url in enumerate(urls, 1):
            print(f"  {i:>3}. {url}")
        return 0

    print(
        f"Running load test: {len(urls)} instance(s), "
        f"max_concurrency={args.max_concurrency}, headed={args.headed}"
    )
    return asyncio.run(
        main_async(urls, args.max_concurrency, args.output_csv, args.headed, screenshot_dir)
    )


if __name__ == "__main__":
    raise SystemExit(main())
