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
  7. Click into the first trace in the list  (optional — use --skip-trace-click)

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

    # Metrics-only load test (skip trace click — common under high concurrency)
    python loadtest_galileo.py --users-csv ../workshop-setup/users.csv --skip-trace-click

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
SIGNIN_TIMEOUT_MS = 60_000
NAV_TIMEOUT_MS = 60_000
METRICS_COMPUTE_TIMEOUT_MS = 300_000
COMPUTE_BUTTON_TIMEOUT_MS = 30_000  # Apply → Compute confirmation can take several seconds
STEP_RETRIES = 4
STEP_RETRY_DELAY_MS = 1_500

RESULT_FIELDS = [
    "row", "email", "project", "status", "failed_step",
    "compute_time_s", "total_duration_s", "error", "screenshot",
]

# JS helpers: detect Queued / Computing status labels (not the Compute button).
_METRICS_IN_PROGRESS_JS = """
() => {
    const isVisible = (el) => {
        if (!el) return false;
        const s = window.getComputedStyle(el);
        if (s.visibility === 'hidden' || s.display === 'none' || s.opacity === '0') return false;
        const rect = el.getBoundingClientRect();
        return rect.width > 0 && rect.height > 0;
    };
    const isInProgress = (t) => {
        if (t === 'compute') return false;
        return t === 'computing' || t === 'computing...'
            || t === 'queued' || t === 'queued...'
            || t.startsWith('computing') || t.startsWith('queued');
    };
    for (const el of document.querySelectorAll('*')) {
        if (!isVisible(el)) continue;
        if (el.tagName === 'BUTTON' || el.closest('button')) continue;
        const t = (el.textContent || '').trim().toLowerCase();
        if (isInProgress(t) && (el.textContent || '').trim().length < 40) return true;
    }
    return false;
}
"""

_METRICS_IN_PROGRESS_LABEL_JS = """
() => {
    const isVisible = (el) => {
        if (!el) return false;
        const s = window.getComputedStyle(el);
        if (s.visibility === 'hidden' || s.display === 'none' || s.opacity === '0') return false;
        const rect = el.getBoundingClientRect();
        return rect.width > 0 && rect.height > 0;
    };
    const isInProgress = (t) => {
        if (t === 'compute') return false;
        return t === 'computing' || t === 'computing...'
            || t === 'queued' || t === 'queued...'
            || t.startsWith('computing') || t.startsWith('queued');
    };
    for (const el of document.querySelectorAll('*')) {
        if (!isVisible(el)) continue;
        if (el.tagName === 'BUTTON' || el.closest('button')) continue;
        const raw = (el.textContent || '').trim();
        const t = raw.toLowerCase();
        if (isInProgress(t) && raw.length < 40) return raw;
    }
    return '';
}
"""

_BROWSER_ARGS = [
    "--disable-dev-shm-usage",  # avoid /dev/shm exhaustion under many contexts
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


# ── Retry / overlay helpers ───────────────────────────────────────────────────

async def retry_click(
    locator,
    page: Page,
    success_selector: str,
    *,
    log=None,
    retries: int = STEP_RETRIES,
    retry_delay_ms: int = STEP_RETRY_DELAY_MS,
    success_timeout_ms: int = 8_000,
    force: bool = False,
) -> None:
    """Click `locator` and wait for `success_selector` to appear, retrying if it doesn't."""
    last_exc: Exception | None = None
    for attempt in range(retries):
        if attempt > 0 and log:
            log(f"  retrying click (attempt {attempt + 1}/{retries})...")
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


async def wait_for_dialogs_closed(page: Page, timeout_ms: int = 10_000) -> None:
    """Wait until no modal dialog is attached to the DOM."""
    await page.wait_for_function(
        "() => !document.querySelector('[role=\"dialog\"], [role=\"alertdialog\"]')",
        timeout=timeout_ms,
    )


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
    """Navigate to metrics config if needed; skip the button click when already there."""
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
    """Wait for the metrics/evaluators config page and its metric rows to finish loading."""
    await _metrics_config_heading(page).first.wait_for(
        state="visible", timeout=NAV_TIMEOUT_MS,
    )
    log("metrics configuration page loaded")

    # Wait for the table to begin rendering (first row may be above the fold only).
    await page.locator(
        '[role="dialog"] [data-testid="metric-enabled-switch"], '
        '[role="dialog"] input[aria-label*="Enable" i][role="switch"]'
    ).first.wait_for(state="attached", timeout=NAV_TIMEOUT_MS)
    log("metric list loaded")


async def _scroll_metrics_modal(page: Page, delta: int) -> None:
    """Scroll the metrics modal body down by `delta` pixels."""
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


_METRICS_TO_ENABLE = ["Correctness", "Context Adherence"]

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
        log(f"  '{label}' row in DOM — scrolling into view")

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


def _metric_toggle_candidates(page: Page, label: str):
    """Yield locator candidates for a metric toggle, most specific first."""
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


async def _find_metric_toggle(page: Page, label: str, log) -> object:
    """Scroll the metrics list if needed, then locate the toggle for `label`."""
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


async def _enable_toggle(page: Page, label: str, log) -> None:
    """Enable a metric toggle by its display name, with retries."""
    log(f"  checking '{label}'")
    last_exc: Exception | None = None

    for attempt in range(STEP_RETRIES):
        if attempt > 0:
            log(f"  retry enable '{label}' (attempt {attempt + 1}/{STEP_RETRIES})")
            await _reset_metrics_modal_scroll(page)

        enabled = await _read_metric_enabled(page, label)
        if enabled is None:
            await _scroll_to_metric(page, label, log, reset_first=(attempt == 0))
            enabled = await _read_metric_enabled(page, label)

        if enabled is True:
            log(f"  '{label}' already enabled")
            return
        if enabled is None:
            raise TimeoutError(f"Could not locate '{label}' in metrics list")

        toggle = await _find_metric_toggle(page, label, log)
        log(f"  clicking '{label}' toggle on")
        label_parent = toggle.locator("xpath=ancestor::label[1]")
        if await label_parent.count() > 0:
            await label_parent.click(force=True, timeout=NAV_TIMEOUT_MS)
        else:
            await toggle.click(force=True, timeout=NAV_TIMEOUT_MS)

        await page.wait_for_timeout(400)
        await _scroll_to_metric(page, label, log, reset_first=False)
        try:
            await _wait_for_toggle_state(page, label, checked=True, timeout_ms=10_000)
            log(f"  '{label}' enabled")
            return
        except Exception as exc:
            last_exc = exc
            await page.wait_for_timeout(STEP_RETRY_DELAY_MS)

    raise last_exc or TimeoutError(f"Failed to enable '{label}'")


async def _ensure_metrics_enabled(page: Page, labels: list[str], log) -> None:
    """Enable each target metric and verify all are on before clicking Apply."""
    for label in labels:
        await _enable_toggle(page, label, log)

    await _reset_metrics_modal_scroll(page)
    last_still_off: list[str] = []

    for attempt in range(STEP_RETRIES):
        still_off: list[str] = []
        for i, label in enumerate(labels):
            enabled = await _read_metric_enabled(page, label)
            if enabled is None:
                await _scroll_to_metric(page, label, log, reset_first=(i == 0))
                enabled = await _read_metric_enabled(page, label)
            if enabled is not True:
                still_off.append(label)

        if not still_off:
            log(f"verified all metrics enabled: {', '.join(labels)}")
            return

        last_still_off = still_off
        log(
            f"  still disabled before Apply: {still_off} "
            f"(verify attempt {attempt + 1}/{STEP_RETRIES})"
        )
        for label in still_off:
            await _enable_toggle(page, label, log)
        await page.wait_for_timeout(STEP_RETRY_DELAY_MS)

    raise TimeoutError(f"Metrics still disabled before Apply: {last_still_off}")


async def configure_metrics(page: Page, log) -> None:
    await _open_metrics_config_page(page, log)
    await _wait_for_metrics_list_with_retry(page, log)

    await _ensure_metrics_enabled(page, _METRICS_TO_ENABLE, log)

    log("clicking 'Apply'")
    for attempt in range(STEP_RETRIES):
        if attempt > 0:
            log(f"  retrying Apply (attempt {attempt + 1}/{STEP_RETRIES})...")
        await page.get_by_role("button", name="Apply").click(timeout=NAV_TIMEOUT_MS)
        break
    log("Apply clicked — waiting for Compute confirmation in next step")


async def _wait_for_computing_to_finish(page: Page, log, t0: float) -> float:
    """Wait until Queued/Computing status clears before continuing."""
    try:
        await page.wait_for_function(_METRICS_IN_PROGRESS_JS, timeout=30_000)
        label = await page.evaluate(_METRICS_IN_PROGRESS_LABEL_JS) or "Queued/Computing"
        log(f"'{label}' status visible, waiting for metrics to finish...")
    except Exception:
        log("No Queued/Computing status appeared — metrics may have finished quickly")

    await page.wait_for_function(
        f"() => !({_METRICS_IN_PROGRESS_JS})()",
        timeout=METRICS_COMPUTE_TIMEOUT_MS,
    )

    elapsed = time.monotonic() - t0
    log(f"metrics resolved in {elapsed:.1f}s")
    return elapsed


def _compute_confirmation(page: Page):
    """The post-Apply dialog that offers to compute metrics on existing traces."""
    return (
        page.locator('[role="dialog"], [role="alertdialog"]')
        .filter(has=page.get_by_role("button", name="Compute", exact=True))
        .filter(has_text="Last")
        .last
    )


async def _locate_compute_button(page: Page):
    """Find Compute inside the confirmation dialog only (not other UI)."""
    confirmation = _compute_confirmation(page)
    if await confirmation.count() == 0:
        return None
    btn = confirmation.get_by_role("button", name="Compute", exact=True)
    try:
        await btn.wait_for(state="visible", timeout=1_000)
        return btn
    except Exception:
        return None


async def _click_compute_button(page: Page, log) -> None:
    """Click Compute in the confirmation dialog and verify that dialog closes."""
    last_exc: Exception | None = None
    for attempt in range(STEP_RETRIES):
        confirmation = _compute_confirmation(page)
        compute_btn = confirmation.get_by_role("button", name="Compute", exact=True)

        if attempt > 0:
            log(f"  retrying Compute click (attempt {attempt + 1}/{STEP_RETRIES})...")
        else:
            log("clicking 'Compute'")

        try:
            await confirmation.wait_for(state="visible", timeout=NAV_TIMEOUT_MS)
            await compute_btn.wait_for(state="visible", timeout=NAV_TIMEOUT_MS)
            await compute_btn.scroll_into_view_if_needed()

            try:
                await compute_btn.click(force=True, timeout=5_000)
            except Exception:
                log("  Playwright click failed — trying JS click")
                await compute_btn.evaluate("el => el.click()")

            await confirmation.wait_for(state="hidden", timeout=15_000)
            log("compute confirmation dismissed")
            return
        except Exception as exc:
            last_exc = exc
            if attempt < STEP_RETRIES - 1:
                await page.wait_for_timeout(STEP_RETRY_DELAY_MS)
    raise last_exc


async def _wait_for_compute_button(page: Page, log) -> None:
    """Wait for the Compute confirmation button to appear after Apply."""
    log("waiting for 'Compute' confirmation button")
    deadline = time.monotonic() + COMPUTE_BUTTON_TIMEOUT_MS / 1000
    while time.monotonic() < deadline:
        btn = await _locate_compute_button(page)
        if btn is not None:
            log("'Compute' button visible")
            return
        await page.wait_for_timeout(500)

    if await page.evaluate(_METRICS_IN_PROGRESS_JS):
        log("'Compute' button never appeared — metric calculation already in progress")
        return

    raise TimeoutError(
        f"'Compute' button did not appear within {COMPUTE_BUTTON_TIMEOUT_MS / 1000}s after Apply"
    )


async def compute_and_measure(page: Page, log) -> float:
    """Click Compute in the confirmation dialog and measure how long metrics take to resolve."""
    t0 = time.monotonic()
    await _wait_for_compute_button(page, log)

    if await _locate_compute_button(page) is None:
        if await page.evaluate(_METRICS_IN_PROGRESS_JS):
            return await _wait_for_computing_to_finish(page, log, t0)
        raise TimeoutError("Compute confirmation expected but button not found")

    await _click_compute_button(page, log)
    return await _wait_for_computing_to_finish(page, log, t0)


async def click_first_trace(page: Page, log) -> None:
    """Open the first trace row, dismissing Mantine overlays that block pointer events."""
    log("clicking first trace")
    url_before = page.url
    first_row = page.locator(
        'table tbody tr[class*="table_row"], '
        '[data-testid*="trace-row"], '
        'table tbody tr'
    ).first

    last_exc: Exception | None = None
    for attempt in range(STEP_RETRIES):
        if attempt > 0:
            log(f"  retrying trace click (attempt {attempt + 1}/{STEP_RETRIES})...")
        await dismiss_overlays(page, log if attempt == 0 else None)
        try:
            await wait_for_dialogs_closed(page, timeout_ms=5_000)
        except Exception:
            pass
        await first_row.wait_for(state="visible", timeout=NAV_TIMEOUT_MS)

        try:
            await first_row.click(force=True, timeout=NAV_TIMEOUT_MS)
            await page.wait_for_url(lambda url: url != url_before, timeout=NAV_TIMEOUT_MS)
            log(f"trace detail view loaded: {page.url}")
            return
        except Exception as exc:
            last_exc = exc
            if attempt < STEP_RETRIES - 1:
                await page.wait_for_timeout(STEP_RETRY_DELAY_MS)
    raise last_exc


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
    skip_trace_click: bool,
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
        "compute_time_s": "",
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

            failed_step = "configure_metrics"
            await configure_metrics(page, log)

            failed_step = "compute_and_measure"
            compute_s = await compute_and_measure(page, log)
            result["compute_time_s"] = round(compute_s, 1)

            if skip_trace_click:
                result["status"] = "success"
            else:
                failed_step = "click_first_trace"
                await click_first_trace(page, log)
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
    compute_info = (
        f"  compute={result['compute_time_s']}s" if result["compute_time_s"] != "" else ""
    )
    step_info = f"  step={result['failed_step']}" if result["failed_step"] else ""
    print(
        f"[{label}] row {row_num:>3}  {email}  {project_name}{compute_info}{step_info}"
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
    skip_trace_click: bool,
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
                skip_trace_click=skip_trace_click,
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

    compute_times = [
        r["compute_time_s"] for r in results
        if isinstance(r["compute_time_s"], (int, float))
    ]
    if compute_times:
        avg_s = round(sum(compute_times) / len(compute_times), 1)
        max_s = round(max(compute_times), 1)
        min_s = round(min(compute_times), 1)
        print(f"\nMetric compute time — min: {min_s}s  avg: {avg_s}s  max: {max_s}s")

    if failed:
        by_step: dict[str, int] = {}
        for r in results:
            if r["status"] == "failed" and r["failed_step"]:
                by_step[r["failed_step"]] = by_step.get(r["failed_step"], 0) + 1
        if by_step:
            print("Failures by step:", ", ".join(f"{k}={v}" for k, v in sorted(by_step.items())))

    print(f"Done: {passed}/{len(results)} passed, {failed} failed.")
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
        "--skip-trace-click",
        action="store_true",
        help="Stop after metrics compute completes (skip clicking the first trace)",
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
        print(f"[dry run] Would test {len(rows)} user(s) against {console_url}:")
        for i, row in enumerate(rows, 1):
            print(f"  {i:>3}. {row['email']}  →  project-{row['participant_number']}")
        if args.skip_trace_click:
            print("  (--skip-trace-click: would stop after metrics compute)")
        return 0

    print(
        f"Running Galileo load test: {len(rows)} user(s), "
        f"max_concurrency={args.max_concurrency}, "
        f"start_delay={args.start_delay}s, "
        f"skip_trace_click={args.skip_trace_click}, "
        f"console={console_url}"
    )
    return asyncio.run(
        main_async(
            rows, console_url, password,
            args.max_concurrency, args.output_csv,
            args.headed, args.start_delay,
            args.skip_trace_click, screenshot_dir,
        )
    )


if __name__ == "__main__":
    raise SystemExit(main())
