---
title: 7. Operationalize DXA and RUM
linkTitle: 7. Operationalize
weight: 7
---

Use this checklist before rolling out DXA-backed RUM instrumentation beyond the lab.

## RUM to APM integration

Splunk RUM can link browser spans to backend APM spans when backend services emit the `Server-Timing` response header with trace context. When using Splunk APM instrumentation, enable response headers in the backend service:

```bash
SPLUNK_TRACE_RESPONSE_HEADER_ENABLED=true
```

After rollout, open a RUM waterfall and look for the **APM** link on backend resource spans. That link moves the investigation from the user interaction to the server-side trace.

## Source maps

For production browser applications, upload source maps during CI/CD with the `splunk-rum` CLI or an approved build integration. Source maps make JavaScript stack traces readable in RUM, which makes DXA error-driven segments easier to investigate.

## Privacy and data minimization

- Keep RUM click-text and Session Replay masking restrictive by default.
- Unmask only selectors reviewed and approved for analytics and troubleshooting.
- Exclude DOM regions that can contain secrets, personal data, payment data, or support transcripts.
- Redact sensitive query parameters before export.
- Avoid global attributes that contain personal data unless there is a clear debugging need and an approved policy.

## Injection and deployment strategy

- Prefer app-native instrumentation when the frontend team owns the application build.
- Use nginx injection for legacy, static, or multi-page apps where proxy-level rollout is the lowest-risk path.
- Inject near `<head>`, not near `</body>`, so RUM starts before application JavaScript.
- Keep the injected snippet identical across replicas by templating it from environment variables or deployment configuration.
- Test the exact nginx config in staging before production.

## Common rollout failures

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Marker is missing from HTML | `sub_filter` did not match the page | Verify the page contains lowercase `<head>` or inject at a stable HTML marker. |
| Works on static files but not proxied app | Upstream response is compressed | Add `proxy_set_header Accept-Encoding "";` to the proxied location. |
| Scripts are present but blocked | CSP blocks CDN or ingest | Add `cdn.observability.splunkcloud.com` to `script-src` and `rum-ingest.<realm>.observability.splunkcloud.com` to `connect-src`. |
| nginx logs `status=missing` | Initialization ran before the CDN scripts created the browser globals, or scripts were blocked | Confirm both script tags appear before initialization and check Chrome Network and Console. |
| nginx logs `status=error` | Initialization code threw an exception | Check Chrome Console for the exception and verify realm, token, and snippet syntax. |
| RUM appears but DXA has no useful users | Anonymous user tracking disabled or old agent version | Use RUM browser agent 2.0.0 or later and set `user.trackingMode` to `anonymousTracking`. |
| Event definitions are noisy | Selector or event pattern is too broad | Narrow the event definition by URL, target text, element selector, or environment. |
| APM links are missing | Backend response trace header disabled | Enable `SPLUNK_TRACE_RESPONSE_HEADER_ENABLED=true` and confirm backend services are instrumented. |

## Clean up the local lab

Stop the demo when you are finished:

```bash
cd workshop/rum-nginx-session-replay
docker compose down
```

You now have the core operating model for DXA with RUM: collect browser telemetry, preserve anonymous user/session context, define meaningful events, analyze journeys in DXA, and return to RUM/APM when the analysis points to a technical problem.
