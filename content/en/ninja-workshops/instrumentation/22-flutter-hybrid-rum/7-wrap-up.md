---
title: 7. Wrap Up
weight: 7
---

You have instrumented the main paths for a Flutter or hybrid mobile application and validated the resulting sessions in Splunk Observability Cloud.

## What You Completed

- Planned the right agent path for Flutter, hybrid WebView, React Native, and backend surfaces.
- Added Flutter RUM initialization with realm, token, app name, environment, and version.
- Added privacy-safe global attributes, user tracking mode, custom events, workflows, and screen tracking.
- Added browser RUM to a WebView/hybrid layer with explicit embedded-app context.
- Reviewed how RUM sessions connect to backend APM traces.
- Validated data in Splunk RUM and walked through common troubleshooting checks.

## Production Next Steps

- Move token and realm values into your normal mobile configuration pipeline.
- Add CI checks that prevent committing real RUM tokens or PII-bearing configuration.
- Add release dashboards that compare crash rate, app startup, network latency, workflow duration, and failed requests by `app.version`.
- Review session replay and header capture with privacy and legal stakeholders before enabling broad rollout.
- Create alerts only after you understand baseline behavior for each mobile platform and release channel.

{{% notice title="Congratulations" style="blue" icon="wine-bottle" %}}
You now have a practical instrumentation pattern for Flutter screens, embedded WebView experiences, and backend trace correlation.
{{% /notice %}}
