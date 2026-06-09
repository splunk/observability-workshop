---
title: 9. Operationalize Mobile RUM and DXA
linkTitle: 9. Operationalize
weight: 9
---

Use this checklist before rolling out iOS RUM and DXA beyond the lab.

## Release controls

- Test new RUM agent versions in pre-production before pinning them for production.
- Keep `appName`, `deploymentEnvironment`, and app version stable and reviewable.
- Upload dSYMs for every released build before distribution.
- Keep RUM token rotation documented for mobile release cycles.
- Confirm RUM telemetry volume and sampling expectations before broad rollout.

## Privacy controls

- Keep anonymous tracking aligned with consent and privacy policy.
- Do not add personal data to global attributes or custom workflow attributes.
- Use `spanInterceptor` to redact URLs and metadata before export.
- Keep sensitive UIKit, SwiftUI, and WebView content hidden in Session Replay.
- Review Session Replay retention, access, and enablement with the right owners.

## Event design controls

- Treat event names as a contract between mobile engineering, product, and operations.
- Keep a small controlled vocabulary for event names.
- Prefer durable attributes such as `app.feature`, `checkout.step`, and `result`.
- Avoid high-cardinality attributes such as order IDs, email addresses, precise location, and raw search text.
- Version major event schema changes when analyses or alerts depend on them.

## Troubleshooting matrix

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| No mobile sessions in RUM | Wrong realm, wrong token, agent not installed, or network blocked | Check startup logs, token type, realm, and device connectivity. |
| Sessions exist but DXA has weak user analysis | Anonymous user tracking disabled | Use `.anonymousTracking` when policy permits. |
| Screen names are technical | Raw controller names are used | Add a navigation event processor with business-friendly names. |
| Workflow events do not appear | Workflow not tracked or span not ended | Use `trackWorkflow(...)` and always call `span.end()`. |
| Replay hides too much | Sensitive class or view policy is too broad | Use targeted sensitivity overrides after privacy review. |
| Replay exposes too much | Sensitive views are not marked | Mark sensitive UIKit/SwiftUI views and keep WebViews sensitive by default. |
| Crashes are not readable | dSYMs missing or do not match the released build | Upload the exact dSYMs for the archived binary. |
| DXA events are noisy | Event definitions are too broad | Filter by event name, screen, feature, environment, or result. |

## Production handoff

Leave the mobile team with:

- the exact RUM agent package version,
- the initialization code location,
- the app name and environment naming convention,
- the event catalog,
- the privacy review outcome,
- the dSYM upload job,
- the DXA project and event-definition owners,
- a rollback plan for disabling Session Replay or custom events if needed.
