---
title: 6. Validate and Troubleshoot
weight: 6
---

After instrumentation is added, validate the data path before judging the shape of the data. Mobile RUM may take a few minutes to appear, and local debug builds can behave differently from release builds.

## Generate Test Sessions

{{% notice title="Exercise" style="green" icon="running" %}}

Run a repeatable script manually in the app:

1. Launch the app fresh.
2. Navigate to the home screen.
3. Open a product or detail screen.
4. Trigger one successful network call.
5. Trigger one failed or slow network call if your test environment supports it.
6. Complete or abandon one workflow, such as checkout or sign-in.
7. Background and foreground the app.
8. Close and relaunch the app.

Record the exact time and app version so you can find the session quickly.

{{% /notice %}}

## Check Splunk RUM

In Splunk Observability Cloud:

1. Open **RUM**.
2. Select the instrumented application.
3. Filter to your `deployment.environment`.
4. Set the time picker to the last 15 minutes.
5. Confirm the app version, platform, user/session count, screen or route names, errors, and network requests.

{{% notice title="Expected result" style="info" %}}
You should see a small number of sessions from your test device. The first validation goal is presence and basic shape: correct app name, environment, version, device/platform, and a timeline that matches your test actions.
{{% /notice %}}

## Common Failures

| Symptom | Check |
| ------- | ----- |
| No sessions appear | Confirm realm, token, network access, app name, environment filter, and time range. |
| Flutter build fails on Android | Check `minSdkVersion`, desugaring, Gradle sync, and current package requirements. |
| Flutter build fails on iOS | Check iOS deployment target, Swift Package Manager, pods/package resolution, and clean build state. |
| Sessions appear under the wrong app | Confirm `appName` and hybrid WebView `applicationName` values. |
| WebView sessions look like desktop browser sessions | Add explicit `app.platform=hybrid-webview` and shell attributes. |
| Missing route or screen names | Add or adjust manual navigation tracking for custom navigation stacks. |
| Missing backend trace link | Check backend APM instrumentation, trace header handling, `Server-Timing`, and CORS-exposed headers. |
| Sensitive values appear | Redact URLs, query strings, headers, and custom attributes before wider rollout. |

{{< tabs >}}
{{% tab title="Question" %}}
**When should you troubleshoot from device logs instead of the Splunk UI?**
{{% /tab %}}
{{% tab title="Answer" %}}
**Use device logs when no telemetry appears at all, the SDK fails to initialize, or network export requests are blocked before reaching Splunk.**
{{% /tab %}}
{{< /tabs >}}

## Rollout Checklist

- Run in a non-production environment first.
- Use a dedicated RUM application name for the workshop or test app.
- Confirm privacy review for user IDs, custom attributes, captured headers, and session replay.
- Compare debug and release builds.
- Validate Android and iOS separately.
- Document the app owner, token owner, release process, and expected dashboards.
