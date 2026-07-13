---
title: API Test
linkTitle:  2. API Test
weight: 2
hidden: false
---

The **API Test** provides a flexible way to check the functionality and performance of API endpoints. The shift toward API-first development has magnified the necessity to monitor the back-end services that provide your core front-end functionality — by the time a regression surfaces in a Real Browser Test, the underlying API has often already been broken for a while.

Whether you're interested in testing multi-step API interactions or you want to gain visibility into the performance of individual endpoints, the API Test can help you accomplish your goals.

![API test result](../img/api-test-result.png)

## How an API Test differs from a Real Browser Test

API Tests are **headless** — there's no browser, no JavaScript engine, no DOM. The test runner makes raw HTTP requests, parses the responses, and runs your validation rules against them. That has three practical consequences:

- **Cheaper and faster per run.** A typical API run completes in tens or hundreds of milliseconds rather than the 10–30 seconds an RBT takes. This makes higher-frequency monitoring feasible — many teams run critical API tests every minute.
- **No rendering signal.** You can't measure paint times or layout shifts because nothing's being rendered. If you need to know how a real user *experiences* the result, you still want an RBT covering that journey.
- **Easier to chain steps.** Variables extracted from one response can be referenced by name in the next request, which makes it natural to model real business transactions like "log in, fetch user profile, perform an action, verify the result."

## When to reach for an API Test

- **Backend SLOs.** Endpoint availability and latency for the APIs your services depend on.
- **Authentication flows.** OAuth token issuance, SAML assertion exchange, session creation — all multi-step, all critical, all easier to validate explicitly than by inference from a browser test.
- **JSON contract validation.** Asserting that a response includes a specific field, that an array has the expected number of elements, or that a value matches a regex — catches breaking schema changes before they hit clients.
- **Synthetic business transactions.** Sequences of API calls that represent a real user action, end to end, even when no human is currently performing one.

In this chapter you'll build a two-step API Test against the public Spotify Web API. The first step performs an **OAuth 2 Client Credentials** authentication and extracts the bearer token from the response. The second step uses that token to call the Spotify search endpoint and extracts the ID of the first matching track. The same pattern — auth followed by an authenticated action — covers a huge slice of real backend monitoring use cases.
