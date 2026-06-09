---
title: 2. Prerequisites and Architecture
weight: 2
time: 10 minutes
description: Confirm the Android, Splunk, and application prerequisites for mobile monitoring.
---

Before changing code, confirm what you are instrumenting and where the data will go.
RUM telemetry is produced on end-user devices, sent directly to Splunk RUM ingest, and
shown in Splunk Observability Cloud. A local OpenTelemetry Collector is not required
for the Android RUM path.

## Reference App Flow

The examples use **Buttercup**, a simple shopping app, as the reference app. The app is
not special. It is a stand-in for any Android app that has screens, user actions, API
calls, and failure paths.

| Buttercup area | What the user does | Why we monitor it |
| --- | --- | --- |
| Product list | Opens the app and browses products | Measures startup, first screen, and basic interaction health. |
| Product detail | Opens an item and reviews details | Tracks navigation and screen-level latency. |
| Cart | Adds or removes items | Tracks important taps and cart API calls. |
| Checkout shipping | Enters delivery information | Tracks a key funnel step and handled validation errors. |
| Checkout payment | Submits payment | Tracks the highest-risk workflow and backend payment latency. |
| Confirmation | Sees order completion | Confirms the journey succeeded end to end. |

If you bring your own app, choose one journey with equivalent steps. The workshop code
uses names like `checkout_shipping` and `checkout_submit`; replace them with names
that describe your own app's user journey.

## Lab Requirements

- Access to a Splunk Observability Cloud organization with RUM enabled.
- Permission to create or read a RUM access token.
- An Android Studio project for a native Android app.
- Android Gradle Plugin compatible with the app and Splunk RUM Android 2.x.
- Android compile/build API level 21 or higher.
- A test device or emulator with internet access to Splunk ingest endpoints.
- A backend endpoint that the app calls, ideally instrumented with Splunk APM for
  trace correlation.

{{% notice title="Version Compatibility" style="info" %}}
The Splunk RUM Android 2.x agent builds for Android API level 21 and higher. By
default, the agent runs on devices with Android API level 24 and higher. If you need
full runtime support for API levels 21-23, configure `forceEnableOnLowerApi` after
testing that behavior in your app.
{{% /notice %}}

## Collect the Values

Create a worksheet with the values you will use in the code examples.

| Value | Example | Notes |
| --- | --- | --- |
| Splunk realm | `us1` | Use the realm for your Observability Cloud organization. |
| RUM access token | `***` | Use a RUM token, not an API token. |
| Application name | `buttercup-android` | Use a stable app name. |
| Deployment environment | `workshop` | Use values like `dev`, `qa`, `prod`, or `workshop`. |
| App version | `1.0.0-workshop` | Prefer the real release version. |
| Build variant | `debug` | Start with debug before production builds. |

## Decide the Monitoring Scope

For this workshop, the first pass should capture:

- Startup, foreground/background, and lifecycle transitions.
- User taps and screen transitions.
- Network calls made through OkHttp or `HttpURLConnection`.
- Crashes, handled exceptions, ANRs, and slow rendering.
- A custom event for one important user action.
- A custom workflow span around one important user journey.
- Optional session replay after privacy controls are reviewed.

## Instrumentation Plan

Use this map before writing code. It separates what the app already does from what you
will add for observability.

| App behavior | Code location | Instrumentation added |
| --- | --- | --- |
| App process starts | `Application.onCreate()` | `SplunkRum.install()` initializes the SDK once. |
| App moves between foreground and background | Android lifecycle callbacks | Lifecycle module records app state changes automatically. |
| User taps buttons and moves through screens | Activities, fragments, or Compose navigation | Automatic interaction capture plus manual screen names. |
| App calls backend APIs | OkHttp or `HttpURLConnection` client | Automatic HTTP module records request timing and response data. |
| Checkout submit starts and completes | Checkout repository, use case, or view model | Manual workflow span around the checkout operation. |
| App catches a recoverable error | Error handler or view model | Manual handled exception event with safe context. |
| Production crash stack traces are obfuscated | CI release build | Mapping file upload de-obfuscates crashes in RUM. |

## Data Flow

```text
Buttercup Android app
  |-- product, cart, and checkout screens
  |-- catalog, cart, payment, and order API calls
  |-- startup, lifecycle, interaction, render, crash, and ANR spans
  |-- network spans for supported HTTP clients
  |-- custom navigation, checkout workflow, events, and handled exceptions
  v
Splunk RUM ingest endpoint for your realm
  v
Splunk Observability Cloud RUM mobile views
  |-- sessions
  |-- errors and crashes
  |-- network requests
  |-- screen and workflow analysis
  v
Splunk APM correlation when backend traces expose trace context
```

## Exercise

Write down:

1. The app package ID and module name.
2. The HTTP client used by the app.
3. The primary screen or journey you will track manually.
4. Whether the app uses XML views, Jetpack Compose, WebView, or a mix.
5. Whether the production build uses R8 or ProGuard minification.

You will use those answers in the following modules.
