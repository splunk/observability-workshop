#!/usr/bin/env python3
"""
Galileo console script to disable metric configuration using headless Playwright/Chromium.

For each user in users.csv, drives the following flow concurrently:

  1. Sign in to the Galileo console
  2. Click their assigned project  (project-{participant_number})
  3. Click the "default" log stream
  4. Click "Configure Metrics", disable Correctness + Context Adherence if enabled, click Apply

If the target metrics are already disabled or not present in the list, the script
exits metrics configuration without clicking Apply and marks the run as success.

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
    python loadtest_galileo_remove_metric_configuration.py --users-csv ../workshop-setup/users.csv

    # Preview without opening any browsers
    python loadtest_galileo_remove_metric_configuration.py --users-csv ../workshop-setup/users.csv --dry-run

    # Show the browser for debugging selector issues
    python loadtest_galileo_remove_metric_configuration.py --users-csv ../workshop-setup/users.csv --headed --max-concurrency 1

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
SIGNIN_TIMEOUT_MS = 60_000
NAV_TIMEOUT_MS = 60_000
STEP_RETRIES = 4
STEP_RETRY_DELAY_MS = 1_500

RESULT_FIELDS = [
    "row", "email", "project", "status", "failed_step",
    "total_duration_s", "error", "screenshot",
]

_BROWSER_ARGS = [
    "--disable-dev-shm-usage",
    "--disable-gpu",
]


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
    """Click `locator` and wait for `success_selector` to appear, retrying if it doesn't."""
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
    raise last_exc


async def dismiss_overlays(page: Page, log=None) -> None:
    """Dismiss Mantine popovers, tooltips, and stray dialogs that block clicks."""
    if log:
        log("dismissing overlays")
    for _ in range(2):
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(200)

    for label in ("Close", "Cancel", "OK", "Done"):
        btn = page.get_by_role("button", name=label)
        try:
            if await btn.count() > 0 and await btn.first.is_visible():
                await btn.first.click(force=True, timeout=2_000)
                await page.wait_for_timeout(300)
                break
        except Exception:
            pass


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


# ── Individual UI steps ────────────────────────────────────────────────────────

async def sign_in(page: Page, console_url: str, email: str, password: str, log) -> None:
    log(f"navigating to {console_url}")
    await page.goto(console_url, timeout=SIGNIN_TIMEOUT_MS)

    log("filling sign-in form")
    await page.locator(
        'input[type="email"], input[name="email"], input[placeholder*="email" i]'
    ).first.fill(email)
    await page.locator('input[type="password"]').first.fill(password)

    submit_btn = page.locator(
        'button[type="submit"], button:has-text("Sign in"), button:has-text("Log in")'
    ).first
    projects_indicator = (
        page.locator('[data-testid*="project"], [class*="project"]')
        .or_(page.get_by_text("Projects", exact=True))
        .first
    )

    log("submitting sign-in form")
    last_exc: Exception | None = None
    for attempt in range(STEP_RETRIES):
        if attempt > 0:
            log(f"  retrying sign-in submit (attempt {attempt + 1}/{STEP_RETRIES})...")
        try:
            await submit_btn.click(timeout=NAV_TIMEOUT_MS)
            await projects_indicator.wait_for(state="visible", timeout=SIGNIN_TIMEOUT_MS)
            log("sign-in successful, projects list visible")
            return
        except Exception as exc:
            last_exc = exc
            if attempt < STEP_RETRIES - 1:
                await page.wait_for_timeout(STEP_RETRY_DELAY_MS)
    raise last_exc


def _project_list_row(page: Page, project_name: str):
    """Projects-list row whose first column exactly matches `project_name`."""
    return page.locator("tr[data-with-row-border]").filter(
        has=page.locator("td").first.get_by_text(project_name, exact=True)
    )


async def _wait_for_projects_list(page: Page) -> None:
    await page.get_by_text("Projects", exact=True).first.wait_for(
        state="visible", timeout=NAV_TIMEOUT_MS,
    )


def _project_breadcrumb_name(page: Page, project_name: str):
    """Active project name in the header breadcrumb (see Overview page header)."""
    return (
        page.locator('nav[aria-label="Breadcrumbs"] [aria-current="page"]')
        .locator("p.mantine-Text-root")
        .get_by_text(project_name, exact=True)
    )


async def _verify_project_opened(page: Page, project_name: str) -> None:
    """Confirm the active project via the breadcrumb current-page label."""
    await _project_breadcrumb_name(page, project_name).wait_for(
        state="visible", timeout=NAV_TIMEOUT_MS,
    )


async def open_project(page: Page, project_name: str, log) -> None:
    log(f"opening project '{project_name}'")
    url_before = page.url
    await _wait_for_projects_list(page)

    last_exc: Exception | None = None
    for attempt in range(STEP_RETRIES):
        if attempt > 0:
            log(f"  retrying project open (attempt {attempt + 1}/{STEP_RETRIES})...")
            if page.url != url_before:
                await page.go_back(timeout=NAV_TIMEOUT_MS)
                await _wait_for_projects_list(page)

        try:
            project_row = _project_list_row(page, project_name).first
            await project_row.wait_for(state="visible", timeout=NAV_TIMEOUT_MS)
            await project_row.locator("td").first.click(force=True, timeout=NAV_TIMEOUT_MS)
            await page.wait_for_url(lambda url: url != url_before, timeout=NAV_TIMEOUT_MS)
            await _verify_project_opened(page, project_name)
            log(f"project '{project_name}' opened: {page.url}")
            return
        except Exception as exc:
            last_exc = exc
            if attempt < STEP_RETRIES - 1:
                await page.wait_for_timeout(STEP_RETRY_DELAY_MS)
    raise last_exc


async def _wait_for_log_stream_view(page: Page) -> None:
    await page.wait_for_function(
        """() => {
            const text = document.body.innerText;
            if (/Configure metrics for|Configure evaluators for/i.test(text)) return true;
            return [...document.querySelectorAll('button')].some(
                b => /Configure Metrics|Configure Evaluators/i.test(b.textContent || '')
            );
        }""",
        timeout=NAV_TIMEOUT_MS,
    )


def _log_stream_row(page: Page, stream_name: str):
    """Log-stream row whose first column exactly matches `stream_name`."""
    return page.locator("tr[data-with-row-border]").filter(
        has=page.locator("td").first.get_by_text(stream_name, exact=True)
    )


async def _verify_log_stream_opened(page: Page, stream_name: str) -> None:
    """Confirm the active log stream view is open (not still on project overview)."""
    await page.wait_for_function(
        """({ streamName }) => {
            const text = document.body.innerText;
            if (/Configure metrics for|Configure evaluators for/i.test(text)) return true;
            const hasConfigureBtn = [...document.querySelectorAll('button')].some(
                b => /Configure Metrics|Configure Evaluators/i.test(b.textContent || '')
            );
            if (!hasConfigureBtn) return false;
            if (decodeURIComponent(location.href).includes(streamName)) {
                return true;
            }
            for (const el of document.querySelectorAll('h1, h2, [class*="Title-root"]')) {
                if (el.textContent.trim() === streamName) return true;
            }
            return hasConfigureBtn;
        }""",
        arg={"streamName": stream_name},
        timeout=NAV_TIMEOUT_MS,
    )


async def open_log_stream(page: Page, log, stream_name: str = "default") -> None:
    log(f"opening log stream '{stream_name}'")
    url_before = page.url

    await page.get_by_text("Log stream", exact=False).first.wait_for(
        state="visible", timeout=NAV_TIMEOUT_MS,
    )

    last_exc: Exception | None = None
    for attempt in range(STEP_RETRIES):
        if attempt > 0:
            log(f"  retrying log stream open (attempt {attempt + 1}/{STEP_RETRIES})...")
            if page.url != url_before:
                await page.go_back(timeout=NAV_TIMEOUT_MS)
                await page.get_by_text("Log stream", exact=False).first.wait_for(
                    state="visible", timeout=NAV_TIMEOUT_MS,
                )

        try:
            stream_row = _log_stream_row(page, stream_name).first
            log(f"waiting for '{stream_name}' log stream row to be visible")
            await stream_row.wait_for(state="visible", timeout=NAV_TIMEOUT_MS)
            log(f"clicking '{stream_name}' log stream row")
            await stream_row.locator("td").first.click(force=True, timeout=NAV_TIMEOUT_MS)
            await page.wait_for_url(lambda url: url != url_before, timeout=NAV_TIMEOUT_MS)
            await _verify_log_stream_opened(page, stream_name)
            log(f"log stream '{stream_name}' opened: {page.url}")
            return
        except Exception as exc:
            last_exc = exc
            if attempt < STEP_RETRIES - 1:
                await page.wait_for_timeout(STEP_RETRY_DELAY_MS)
    raise last_exc


def _metrics_config_heading(page: Page):
    return (
        page.get_by_text("Configure metrics for", exact=False)
        .or_(page.get_by_text("Configure evaluators for", exact=False))
    )


async def _is_on_metrics_config_page(page: Page) -> bool:
    try:
        return await _metrics_config_heading(page).first.is_visible()
    except Exception:
        return False


async def _open_metrics_config_page(page: Page, log) -> None:
    if await _is_on_metrics_config_page(page):
        log("already on metrics configuration page")
        return

    configure_btn = (
        page.get_by_role("button", name="Configure Metrics")
        .or_(page.get_by_role("button", name="Configure Evaluators"))
    )
    log("clicking 'Configure Metrics' button")
    await configure_btn.click(timeout=NAV_TIMEOUT_MS)
    await _metrics_config_heading(page).first.wait_for(
        state="visible", timeout=NAV_TIMEOUT_MS,
    )


async def _wait_for_metrics_list(page: Page, log) -> None:
    await _metrics_config_heading(page).first.wait_for(
        state="visible", timeout=NAV_TIMEOUT_MS,
    )
    log("metrics configuration page loaded")

    await page.locator(
        '[role="dialog"] [data-testid="metric-enabled-switch"], '
        '[role="dialog"] input[aria-label*="Enable" i][role="switch"]'
    ).first.wait_for(state="attached", timeout=NAV_TIMEOUT_MS)
    log("metric list loaded")


async def _wait_for_metrics_list_with_retry(page: Page, log) -> None:
    """Retry waiting for metric rows without re-clicking Configure Metrics."""
    last_exc: Exception | None = None
    for attempt in range(STEP_RETRIES):
        if attempt > 0:
            log(f"  retrying wait for metric list (attempt {attempt + 1}/{STEP_RETRIES})...")
        try:
            await _wait_for_metrics_list(page, log)
            return
        except Exception as exc:
            last_exc = exc
            if attempt < STEP_RETRIES - 1:
                await page.wait_for_timeout(STEP_RETRY_DELAY_MS)
    raise last_exc


def _compute_confirmation(page: Page):
    """Post-Apply dialog offering to compute metrics on existing traces."""
    return (
        page.locator('[role="dialog"], [role="alertdialog"]')
        .filter(has=page.get_by_role("button", name="Compute", exact=True))
        .filter(has_text="Last")
        .last
    )


async def _wait_for_log_stream_after_apply(page: Page, log) -> None:
    """Wait for the metrics config modal to close and the log stream view to return."""
    last_exc: Exception | None = None
    for attempt in range(STEP_RETRIES):
        if attempt > 0:
            log(f"  retrying wait for log stream view (attempt {attempt + 1}/{STEP_RETRIES})...")
        try:
            confirmation = _compute_confirmation(page)
            if await confirmation.count() > 0 and await confirmation.first.is_visible():
                log("compute confirmation appeared — clicking Cancel")
                cancel_btn = confirmation.get_by_role("button", name="Cancel")
                if await cancel_btn.count() > 0:
                    await cancel_btn.first.click(force=True, timeout=NAV_TIMEOUT_MS)
                else:
                    await dismiss_overlays(page, log)

            try:
                await _metrics_config_heading(page).first.wait_for(
                    state="hidden", timeout=15_000,
                )
            except Exception:
                pass

            await _wait_for_log_stream_view(page)
            log("metric configuration removed, back on log stream view")
            return
        except Exception as exc:
            last_exc = exc
            if attempt < STEP_RETRIES - 1:
                await page.wait_for_timeout(STEP_RETRY_DELAY_MS)
    raise last_exc


async def _scroll_metrics_modal(page: Page, delta: int) -> None:
    await page.evaluate(
        """([delta]) => {
            const dialog = document.querySelector('[role="dialog"]');
            if (!dialog) return;
            const scroller = dialog.querySelector('.mantine-ScrollArea-viewport')
                || dialog.querySelector('[class*="Modal-body"]')
                || dialog;
            scroller.scrollTop += delta;
        }""",
        [delta],
    )


async def _reset_metrics_modal_scroll(page: Page) -> None:
    await page.evaluate(
        """() => {
            const dialog = document.querySelector('[role="dialog"]');
            if (!dialog) return;
            const scroller = dialog.querySelector('.mantine-ScrollArea-viewport')
                || dialog.querySelector('[class*="Modal-body"]');
            if (scroller) scroller.scrollTop = 0;
        }"""
    )


_METRICS_TO_DISABLE = ["Correctness", "Context Adherence"]

_READ_METRIC_ENABLED_JS = """
({ label }) => {
    const dialog = document.querySelector('[role="dialog"]');
    if (!dialog) return null;

    const ariaSelectors = [
        `input[aria-label="Enable ${label} metric"]`,
        `input[aria-label="Enable ${label} evaluator"]`,
    ];
    for (const sel of ariaSelectors) {
        const input = dialog.querySelector(sel);
        if (input) {
            if (input.getAttribute('role') === 'switch') {
                const ariaChecked = input.getAttribute('aria-checked');
                if (ariaChecked != null) return ariaChecked === 'true';
            }
            return !!input.checked;
        }
    }

    for (const row of dialog.querySelectorAll('tr')) {
        let hasLabel = false;
        for (const cell of row.querySelectorAll('td, th')) {
            if (cell.textContent.trim() === label) {
                hasLabel = true;
                break;
            }
        }
        if (!hasLabel) continue;

        const input = row.querySelector(
            'input[type="checkbox"][role="switch"], input[type="checkbox"]'
        );
        if (input) {
            if (input.getAttribute('role') === 'switch') {
                const ariaChecked = input.getAttribute('aria-checked');
                if (ariaChecked != null) return ariaChecked === 'true';
            }
            return !!input.checked;
        }

        const wrapper = row.querySelector('[data-testid="metric-enabled-switch"]');
        if (wrapper) {
            const inner = wrapper.querySelector('input[type="checkbox"]');
            if (inner) return !!inner.checked;
        }
    }
    return null;
}
"""


def _metrics_dialog(page: Page):
    return page.locator('[role="dialog"]').last


def _metric_toggle_candidates(page: Page, label: str):
    dialog = _metrics_dialog(page)
    row = dialog.locator("tr").filter(has=dialog.get_by_text(label, exact=True))
    yield row.locator('input[type="checkbox"][role="switch"]')
    yield row.locator(f'input[aria-label="Enable {label} metric"]')
    yield dialog.locator(f'input[aria-label="Enable {label} metric"]')
    yield dialog.locator(f'input[aria-label="Enable {label} evaluator"]')
    yield dialog.locator(f'input[aria-label*="Enable {label}" i]')
    yield dialog.get_by_role("switch", name=f"Enable {label} metric")
    yield dialog.get_by_role("switch", name=f"Enable {label} evaluator")
    yield row.locator('[data-testid="metric-enabled-switch"] input[type="checkbox"]')
    yield row.locator('[data-testid="metric-enabled-switch"]')
    yield row.locator('input[type="checkbox"]').first


async def _read_metric_enabled(page: Page, label: str) -> bool | None:
    """Return True/False for metric enabled state, or None if the row cannot be found."""
    return await page.evaluate(_READ_METRIC_ENABLED_JS, {"label": label})


async def _metric_toggle_attached(page: Page, label: str) -> bool:
    return (await _read_metric_enabled(page, label)) is not None


async def _scroll_to_metric(
    page: Page, label: str, log, *, reset_first: bool = True,
) -> None:
    if reset_first:
        await _reset_metrics_modal_scroll(page)

    if not await _metric_toggle_attached(page, label):
        log(f"  scrolling metrics list to find '{label}'")
        for step in range(50):
            await _scroll_metrics_modal(page, 350)
            await page.wait_for_timeout(150)
            if await _metric_toggle_attached(page, label):
                log(f"  '{label}' row found after {step + 1} scroll step(s)")
                break
        else:
            raise TimeoutError(
                f"Could not find '{label}' in metrics list after scrolling"
            )
    else:
        log(f"  '{label}' row in DOM — ensuring visible")

    await page.evaluate(
        """({ label }) => {
            const dialog = document.querySelector('[role="dialog"]');
            if (!dialog) return;
            for (const row of dialog.querySelectorAll('tr')) {
                for (const cell of row.querySelectorAll('td, th')) {
                    if (cell.textContent.trim() === label) {
                        row.scrollIntoView({ block: 'center' });
                        return;
                    }
                }
            }
        }""",
        {"label": label},
    )
    await page.wait_for_timeout(200)


async def _find_metric_toggle(page: Page, label: str, log) -> object:
    await _scroll_to_metric(page, label, log, reset_first=False)

    for candidate in _metric_toggle_candidates(page, label):
        try:
            if await candidate.count() == 0:
                continue
            toggle = candidate.first
            await toggle.wait_for(state="attached", timeout=2_000)
            await toggle.scroll_into_view_if_needed()
            tag = await toggle.evaluate("el => el.tagName")
            if tag and tag.lower() != "input":
                inner = toggle.locator('input[type="checkbox"]')
                if await inner.count() > 0:
                    toggle = inner.first
            return toggle
        except Exception:
            continue

    aria_labels = await page.evaluate(
        "() => [...document.querySelectorAll('[role=\"dialog\"] input[aria-label]')]"
        ".map(el => el.getAttribute('aria-label'))"
    )
    log(f"  toggle not found for '{label}'; dialog aria-labels={aria_labels!r}")
    raise TimeoutError(f"Could not find toggle for metric '{label}'")


_WAIT_FOR_METRIC_ENABLED_JS = """
({ label, wantEnabled }) => {
    const dialog = document.querySelector('[role="dialog"]');
    if (!dialog) return false;

    const ariaSelectors = [
        `input[aria-label="Enable ${label} metric"]`,
        `input[aria-label="Enable ${label} evaluator"]`,
    ];
    let enabled = null;
    for (const sel of ariaSelectors) {
        const input = dialog.querySelector(sel);
        if (input) {
            if (input.getAttribute('role') === 'switch') {
                const ariaChecked = input.getAttribute('aria-checked');
                enabled = ariaChecked != null ? ariaChecked === 'true' : !!input.checked;
            } else {
                enabled = !!input.checked;
            }
            break;
        }
    }
    if (enabled === null) {
        for (const row of dialog.querySelectorAll('tr')) {
            let hasLabel = false;
            for (const cell of row.querySelectorAll('td, th')) {
                if (cell.textContent.trim() === label) {
                    hasLabel = true;
                    break;
                }
            }
            if (!hasLabel) continue;
            const input = row.querySelector(
                'input[type="checkbox"][role="switch"], input[type="checkbox"]'
            );
            if (input) {
                if (input.getAttribute('role') === 'switch') {
                    const ariaChecked = input.getAttribute('aria-checked');
                    enabled = ariaChecked != null ? ariaChecked === 'true' : !!input.checked;
                } else {
                    enabled = !!input.checked;
                }
                break;
            }
            const wrapper = row.querySelector('[data-testid="metric-enabled-switch"]');
            if (wrapper) {
                const inner = wrapper.querySelector('input[type="checkbox"]');
                if (inner) {
                    enabled = !!inner.checked;
                    break;
                }
            }
        }
    }
    if (enabled === null) return false;
    return enabled === wantEnabled;
}
"""


async def _wait_for_toggle_state(
    page: Page, label: str, checked: bool, timeout_ms: int = 5_000,
) -> None:
    """Wait until the metric toggle matches `checked`, re-querying the DOM each poll."""
    await page.wait_for_function(
        _WAIT_FOR_METRIC_ENABLED_JS,
        arg={"label": label, "wantEnabled": checked},
        timeout=timeout_ms,
    )


async def _disable_toggle(page: Page, label: str, log) -> bool:
    """Disable a metric if enabled. Returns True if a toggle click was made."""
    log(f"  checking '{label}'")
    last_exc: Exception | None = None

    for attempt in range(STEP_RETRIES):
        if attempt > 0:
            log(f"  retry disable '{label}' (attempt {attempt + 1}/{STEP_RETRIES})")
            await _reset_metrics_modal_scroll(page)

        enabled = await _read_metric_enabled(page, label)
        if enabled is None:
            try:
                await _scroll_to_metric(
                    page, label, log, reset_first=(attempt == 0),
                )
            except TimeoutError:
                log(f"  '{label}' not in metrics list — nothing to disable")
                return False
            enabled = await _read_metric_enabled(page, label)

        if enabled is False:
            log(f"  '{label}' already disabled")
            return False
        if enabled is None:
            log(f"  '{label}' not in metrics list — nothing to disable")
            return False

        toggle = await _find_metric_toggle(page, label, log)
        log(f"  clicking '{label}' toggle off")
        label_parent = toggle.locator("xpath=ancestor::label[1]")
        if await label_parent.count() > 0:
            await label_parent.click(force=True, timeout=NAV_TIMEOUT_MS)
        else:
            await toggle.click(force=True, timeout=NAV_TIMEOUT_MS)

        await page.wait_for_timeout(400)
        await _scroll_to_metric(page, label, log, reset_first=False)
        try:
            await _wait_for_toggle_state(page, label, checked=False, timeout_ms=10_000)
            log(f"  '{label}' disabled")
            return True
        except Exception as exc:
            last_exc = exc
            await page.wait_for_timeout(STEP_RETRY_DELAY_MS)

    raise last_exc or TimeoutError(f"Failed to disable '{label}'")


async def _ensure_metrics_disabled(page: Page, labels: list[str], log) -> bool:
    """Disable target metrics when enabled. Returns True if any toggle was changed."""
    changed = False
    for label in labels:
        if await _disable_toggle(page, label, log):
            changed = True

    await _reset_metrics_modal_scroll(page)
    last_still_on: list[str] = []

    for attempt in range(STEP_RETRIES):
        still_on: list[str] = []
        for i, label in enumerate(labels):
            enabled = await _read_metric_enabled(page, label)
            if enabled is None:
                try:
                    await _scroll_to_metric(
                        page, label, log, reset_first=(i == 0),
                    )
                    enabled = await _read_metric_enabled(page, label)
                except TimeoutError:
                    enabled = None
            if enabled is True:
                still_on.append(label)

        if not still_on:
            if changed:
                log("verified target metrics are disabled")
            else:
                log("no target metrics were enabled — nothing to change")
            return changed

        last_still_on = still_on
        log(
            f"  still enabled before Apply: {still_on} "
            f"(verify attempt {attempt + 1}/{STEP_RETRIES})"
        )
        for label in still_on:
            if await _disable_toggle(page, label, log):
                changed = True
        await page.wait_for_timeout(STEP_RETRY_DELAY_MS)

    raise TimeoutError(
        f"Metrics still enabled before Apply: {last_still_on}"
    )


async def _leave_metrics_config_without_apply(page: Page, log) -> None:
    """Exit metrics configuration without saving when there were no changes."""
    if not await _is_on_metrics_config_page(page):
        log("already on log stream view")
        await _wait_for_log_stream_view(page)
        return

    for name in ("Cancel", "Back"):
        btn = page.get_by_role("button", name=name)
        try:
            if await btn.count() > 0 and await btn.first.is_visible():
                log(f"clicking '{name}' to leave metrics config")
                await btn.first.click(timeout=NAV_TIMEOUT_MS)
                await _wait_for_log_stream_view(page)
                log("returned to log stream view without Apply")
                return
        except Exception:
            continue

    log("no Cancel/Back button — using browser back")
    await page.go_back(timeout=NAV_TIMEOUT_MS)
    await _wait_for_log_stream_view(page)
    log("returned to log stream view without Apply")


async def remove_metric_configuration(page: Page, log) -> None:
    await _open_metrics_config_page(page, log)
    await _wait_for_metrics_list_with_retry(page, log)

    needs_apply = await _ensure_metrics_disabled(page, _METRICS_TO_DISABLE, log)

    if not needs_apply:
        await _leave_metrics_config_without_apply(page, log)
        return

    log("clicking 'Apply'")
    await page.get_by_role("button", name="Apply").click(timeout=NAV_TIMEOUT_MS)
    log("Apply clicked — waiting to return to log stream view")
    await _wait_for_log_stream_after_apply(page, log)


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
    start_delay_s: float,
    screenshot_dir: str | None,
    results_lock: asyncio.Lock,
    output_csv: str,
) -> dict:
    result: dict = {
        "row": row_num,
        "email": email,
        "project": project_name,
        "status": "failed",
        "failed_step": "",
        "total_duration_s": 0.0,
        "error": "",
        "screenshot": "",
    }
    wall_start = time.monotonic()
    failed_step = ""

    if start_delay_s > 0:
        await asyncio.sleep(start_delay_s)

    async with sem:
        context: BrowserContext = await browser.new_context()
        page: Page = await context.new_page()

        log = make_logger(row_num, email)

        if headed:
            page.on(
                "console",
                lambda msg: print(f"  [browser] {msg.type}: {msg.text}")
                if msg.type == "error" else None,
            )

        try:
            failed_step = "sign_in"
            await sign_in(page, console_url, email, password, log)

            failed_step = "open_project"
            await open_project(page, project_name, log)

            failed_step = "open_log_stream"
            await open_log_stream(page, log)

            failed_step = "remove_metric_configuration"
            await remove_metric_configuration(page, log)
            result["status"] = "success"

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

    result["total_duration_s"] = round(time.monotonic() - wall_start, 1)

    async with results_lock:
        write_header = not os.path.exists(output_csv)
        with open(output_csv, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=RESULT_FIELDS)
            if write_header:
                writer.writeheader()
            writer.writerow(result)

    label = "OK  " if result["status"] == "success" else "FAIL"
    step_info = f"  step={result['failed_step']}" if result["failed_step"] else ""
    print(
        f"[{label}] row {row_num:>3}  {email}  {project_name}{step_info}"
        + (f"\n       {result['error'][:200]}" if result["error"] else "")
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
    start_delay_s: float,
    screenshot_dir: str | None,
) -> int:
    sem = asyncio.Semaphore(max_concurrency)
    results_lock = asyncio.Lock()

    if os.path.exists(output_csv):
        os.remove(output_csv)

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=not headed,
            args=_BROWSER_ARGS,
        )
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
                start_delay_s=i * start_delay_s,
                screenshot_dir=screenshot_dir,
                results_lock=results_lock,
                output_csv=output_csv,
            )
            for i, row in enumerate(rows)
        ]
        results = await asyncio.gather(*tasks)
        await browser.close()

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
        "--users-csv",
        default="../workshop-setup/users.csv",
        metavar="FILE",
        help="CSV with email and participant_number columns (default: ../workshop-setup/users.csv)",
    )
    parser.add_argument(
        "--output-csv",
        default="galileo_remove_metric_configuration_results.csv",
        help="Where to write per-user results (default: galileo_remove_metric_configuration_results.csv)",
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
        "--start-delay",
        type=float,
        default=3.0,
        metavar="SECONDS",
        help=(
            "Seconds to wait between starting each user's session (default: 3). "
            "Staggering prevents all users from hitting the server simultaneously."
        ),
    )
    parser.add_argument(
        "--screenshot-dir",
        default="galileo_failure_screenshots",
        metavar="DIR",
        help=(
            "Directory for PNG screenshots on failure (default: galileo_failure_screenshots). "
            "Pass an empty string to disable."
        ),
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

    screenshot_dir = args.screenshot_dir.strip() or None

    if args.dry_run:
        print(f"[dry run] Would disable metrics for {len(rows)} user(s) against {console_url}:")
        for i, row in enumerate(rows, 1):
            print(f"  {i:>3}. {row['email']}  →  project-{row['participant_number']}")
        return 0

    print(
        f"Removing Galileo metric configuration: {len(rows)} user(s), "
        f"max_concurrency={args.max_concurrency}, "
        f"start_delay={args.start_delay}s, console={console_url}"
    )
    return asyncio.run(
        main_async(
            rows, console_url, password,
            args.max_concurrency, args.output_csv,
            args.headed, args.start_delay,
            screenshot_dir,
        )
    )


if __name__ == "__main__":
    raise SystemExit(main())
