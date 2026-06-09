---
title: 9. Verify and Troubleshoot
weight: 9
time: 10 minutes
description: Confirm Android telemetry in Splunk RUM and troubleshoot common setup issues.
---

After the app runs on a device or emulator, use both Android logs and Splunk RUM to
confirm that telemetry is flowing.

## Generate a Test Session

On a device or emulator:

1. Start the app.
2. Navigate through the tracked screens.
3. Trigger one network request.
4. Trigger the custom event.
5. Trigger the handled exception path.
6. Background and foreground the app.
7. Close and reopen the app.

Wait a few minutes for data to appear.

## Verify in Splunk RUM

In Splunk Observability Cloud:

1. Open **RUM**.
2. Select the mobile application name.
3. Filter to the deployment environment from the workshop.
4. Open recent sessions.
5. Confirm the session contains screens, interactions, network requests, errors, and
   lifecycle events.
6. Open a backend request and check whether APM trace correlation is available.

## Use Logcat

For a debug build, filter Logcat for Splunk and OpenTelemetry output:

```bash
adb logcat | grep -i -E "splunk|opentelemetry|otel|rum"
```

If logs are too noisy, use Android Studio's Logcat search and filter by package name.

## Common Problems

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| No app appears in RUM | Wrong realm, wrong token, no internet, or app never initialized RUM | Confirm `SplunkRum.install()` runs once and Logcat has no auth or network errors. |
| Data appears under the wrong app | App name differs by variant or placeholder value | Print the configured app name at startup and align build config. |
| Runtime errors on older Android versions | Desugaring missing or lower API support not tested | Enable `coreLibraryDesugaring` and test the target API level. |
| No network spans | Unsupported HTTP client or auto instrumentation not enabled | Confirm the HTTP client and configure the matching module or manual instrumentation. |
| No backend trace link | Backend not instrumented or response lacks trace context | Confirm Splunk APM traces exist and `Server-Timing` trace context reaches the app. |
| Obfuscated crash stack traces | Mapping files not uploaded for the release build | Add the mapping upload step to CI and verify app ID/version code alignment. |
| Sensitive replay data visible | Missing sensitivity or mask settings | Stop session replay and fix masking before production use. |

## Temporarily Enable Debug Logging

If data is missing, set `enableDebugLogging = true` in `AgentConfiguration` for a
debug build, reproduce the issue, and inspect Logcat. Remove debug logging afterward.

## Exercise

Complete this validation table:

| Signal | Seen in RUM? | Notes |
| --- | --- | --- |
| App startup/lifecycle |  |  |
| Navigation/screen names |  |  |
| User interactions |  |  |
| Network requests |  |  |
| Custom event |  |  |
| Custom workflow |  |  |
| Handled exception |  |  |
| Crash or ANR test |  |  |
| Backend trace link |  |  |
| Session replay |  |  |
