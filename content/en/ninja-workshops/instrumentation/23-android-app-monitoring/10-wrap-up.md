---
title: 10. Wrap Up
weight: 10
time: 5 minutes
description: Review what was configured and identify next production steps.
---

You now have the core Android monitoring path in place: the Splunk RUM Android agent
is installed, initialized, and sending mobile telemetry to Splunk Observability Cloud.
You also added manual signals that make sessions easier to understand from a product
and support perspective.

## What You Completed

- Created or identified a Splunk RUM token and realm.
- Added Maven Central, desugaring, and the Splunk Android RUM dependency.
- Initialized the agent in `Application.onCreate()`.
- Added app name, version, and deployment environment metadata.
- Generated startup, lifecycle, interaction, network, navigation, custom event,
  workflow, and handled-exception telemetry.
- Reviewed optional session replay and masking controls.
- Prepared the production checklist for R8/ProGuard mapping uploads.
- Verified telemetry in Splunk RUM and reviewed troubleshooting steps.

## Production Next Steps

- Move RUM configuration values into your standard build and secret management flow.
- Decide whether session replay is enabled, where consent is collected, and how
  sensitive data is masked.
- Add mapping file upload to CI before each minified production release.
- Create RUM detectors for crash rate, error rate, slow startup, and key workflow
  latency.
- Review captured attributes and headers with privacy and security owners.
- Connect backend services to Splunk APM and verify trace links from mobile network
  requests.

## Discussion Prompts

1. Which mobile journey should have an SLO or detector first?
2. Which user-facing errors are currently invisible because the app catches them?
3. Which custom attributes help support without creating privacy or cardinality risk?
4. What release gate should fail if RUM telemetry or mapping upload breaks?

## References

- [Splunk RUM for Android installation](https://help.splunk.com/en/splunk-observability-cloud/manage-data/instrument-front-end-applications/instrument-mobile-and-web-applications-for-splunk-real-user-monitoring-rum/instrument-android-applications-for-splunk-rum/splunk-rum-android-agent-version-2.0.0-and-above/install-the-splunk-rum-android-agent)
- [Splunk RUM Android configuration](https://help.splunk.com/en/splunk-observability-cloud/manage-data/instrument-front-end-applications/instrument-mobile-and-web-applications-for-splunk-real-user-monitoring-rum/instrument-android-applications-for-splunk-rum/splunk-rum-android-agent-version-2.0.0-and-above/configure-the-splunk-rum-android-agent)
- [Splunk RUM Android manual instrumentation](https://help.splunk.com/en/splunk-observability-cloud/manage-data/instrument-front-end-applications/instrument-mobile-and-web-applications-for-splunk-real-user-monitoring-rum/instrument-android-applications-for-splunk-rum/splunk-rum-android-agent-version-2.0.0-and-above/manually-instrument-android-applications)
- [Splunk RUM Android troubleshooting](https://help.splunk.com/en/splunk-observability-cloud/manage-data/instrument-front-end-applications/instrument-mobile-and-web-applications-for-splunk-real-user-monitoring-rum/instrument-android-applications-for-splunk-rum/splunk-rum-android-agent-version-2.0.0-and-above/troubleshoot-android-instrumentation)
