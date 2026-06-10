#!/usr/bin/env python3
"""Playwright smoke test that reads the MkDocs site like a student."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from urllib.parse import urljoin

try:
    from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
    from playwright.sync_api import sync_playwright
except ImportError:  # pragma: no cover - exercised before Playwright is installed.
    print(
        "Playwright is not installed. Run:\n"
        "  python -m pip install -r requirements-qa.txt\n"
        "  python -m playwright install chromium",
        file=sys.stderr,
    )
    sys.exit(2)


@dataclass(frozen=True)
class PageCheck:
    path: str
    label: str
    required_text: tuple[str, ...]


PAGE_CHECKS = (
    PageCheck(
        "/",
        "Overview",
        (
            "AI PODs In One Minute",
            "the GPUs are the center",
            "Your Workshop Path",
        ),
    ),
    PageCheck(
        "/prerequisites/",
        "Prerequisites",
        (
            "Set Your Lab Variables",
            "student-kubeconfig.yaml",
            "Configure Kubernetes Access",
            "COLLECTOR_CHART",
            "Prompt Capture Safety",
        ),
    ),
    PageCheck(
        "/module-0-orientation/",
        "Orientation",
        (
            "AI PODs In Plain English",
            "GPU-centered monitoring workflow",
            "ShopMate request -> AI agents -> NVIDIA NIM -> GPUs -> Splunk drilldown",
        ),
    ),
    PageCheck(
        "/data-journey/",
        "Data Journey",
        (
            "Follow one request",
            "Configuration Sessions",
            "otlp_http",
            "prometheus/gpu_nim",
        ),
    ),
    PageCheck(
        "/module-1-collector/",
        "Student Collector",
        (
            "Create The Core Collector Config",
            "student-collector-values.yaml",
            "resource/environment",
            "otlp_http",
            "deployment.environment",
        ),
    ),
    PageCheck(
        "/module-2-app-instrumentation/",
        "App Instrumentation",
        (
            "Point The App At Your Collector",
            "OTEL_RESOURCE_ATTRIBUTES",
            "opentelemetry-instrument",
            "NIM_BASE_URL",
            "shopmate.workflow",
        ),
    ),
    PageCheck(
        "/module-3-gpu-nim-scraping/",
        "GPU And NIM Scraping",
        (
            "Add Prometheus Receiver Jobs",
            "DCGM_SCRAPE_TARGET",
            "NIM_SCRAPE_TARGET",
            "filter/gpu_nim_allowlist",
            "metrics/gpu_nim",
        ),
    ),
    PageCheck(
        "/module-4-correlation/",
        "Correlation",
        (
            "Start From The Trace",
            "Correlate To GPU Metrics",
            "AI Pod overview",
        ),
    ),
    PageCheck(
        "/module-5-tokenomics/",
        "Tokenomics",
        (
            "Tokenomics And Environment Cost Signals",
            "deployment.environment",
            "Highest-Token Environment View",
        ),
    ),
    PageCheck(
        "/final-review/",
        "Final Review",
        (
            "Final Evidence Checklist",
            "Final Answer Template",
            "Exit Criteria",
        ),
    ),
    PageCheck(
        "/appendix-ai-pod-hardware/",
        "AI POD Hardware Appendix",
        (
            "Lab To Production",
            "UCS hardware",
            "Nexus fabric",
        ),
    ),
    PageCheck(
        "/appendix-troubleshooting/",
        "Troubleshooting",
        (
            "Fast Triage Checklist",
            "Collector Issues",
            "Important Environment Variables",
        ),
    ),
    PageCheck(
        "/reference-github-splunk/",
        "GitHub And Splunk References",
        (
            "Collector References",
            "AI Agent Monitoring References",
            "Lab To Production",
        ),
    ),
    PageCheck(
        "/lab-files/",
        "Lab Files",
        (
            "student-kubeconfig.yaml",
            "shopmate-ai.yaml",
            "collector-observability-snippet.yaml",
        ),
    ),
    PageCheck(
        "/lab-files/collector-observability-snippet.yaml",
        "Collector Observability Snippet",
        (
            "prometheus/gpu_nim",
            "resource/environment",
            "filter/gpu_nim_allowlist",
            "send_otlp_histograms",
        ),
    ),
)


FORBIDDEN_TEXT = (
    "Use this framing during the lab",
    "Do not tell students",
    "Then connect it to production",
    "This distinction helps students",
    "full physical Cisco AI POD",
)


def normalize_base_url(base_url: str) -> str:
    return base_url.rstrip("/") + "/"


def run(base_url: str, headed: bool, slow_mo: int, timeout_ms: int) -> list[str]:
    failures: list[str] = []
    base_url = normalize_base_url(base_url)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=not headed, slow_mo=slow_mo)
        page = browser.new_page(viewport={"width": 1440, "height": 1000})
        page.set_default_timeout(timeout_ms)
        request_context = playwright.request.new_context(base_url=base_url)

        for check in PAGE_CHECKS:
            url = urljoin(base_url, check.path.lstrip("/"))
            if check.path.startswith("/lab-files/"):
                response = request_context.get(check.path)
                body_text = response.text()
            else:
                try:
                    response = page.goto(url, wait_until="domcontentloaded")
                    page.locator("body").wait_for(state="visible")
                    body_text = page.locator("body").inner_text()
                except PlaywrightTimeoutError as exc:
                    failures.append(f"{check.label}: timed out loading {url}: {exc}")
                    continue

            if response is None:
                failures.append(f"{check.label}: no HTTP response for {url}")
                continue

            if response.status >= 400:
                failures.append(f"{check.label}: HTTP {response.status} for {url}")
                continue

            for required in check.required_text:
                if required not in body_text:
                    failures.append(
                        f"{check.label}: missing expected text {required!r} on {url}"
                    )

            for forbidden in FORBIDDEN_TEXT:
                if forbidden in body_text:
                    failures.append(
                        f"{check.label}: found instructor-facing text {forbidden!r} on {url}"
                    )

        request_context.dispose()
        browser.close()

    return failures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a student-style Playwright walkthrough against the MkDocs site."
    )
    parser.add_argument(
        "--base-url",
        default="http://127.0.0.1:8001/",
        help="Base URL for the running MkDocs site.",
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Show Chromium while the walkthrough runs.",
    )
    parser.add_argument(
        "--slow-mo",
        type=int,
        default=0,
        help="Delay Playwright actions by this many milliseconds.",
    )
    parser.add_argument(
        "--timeout-ms",
        type=int,
        default=10_000,
        help="Per-action Playwright timeout in milliseconds.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    failures = run(args.base_url, args.headed, args.slow_mo, args.timeout_ms)

    if failures:
        print("Student MkDocs walkthrough failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"Student MkDocs walkthrough passed for {normalize_base_url(args.base_url)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
