---
title: 1. Plan Your Instrumentation Path
weight: 1
---

Before adding code, decide which runtime owns each user interaction. A Flutter screen, a native Android or iOS screen, and a WebView page can all run inside the same mobile app, but they do not all need the same RUM agent.

## App Scenario

In this workshop, the app behaves like a mobile commerce application:

```text
Mobile app launch
  -> Flutter home screen
  -> Flutter product list
  -> Flutter cart screen
  -> WebView checkout or promo step
  -> Flutter confirmation screen
```

The Flutter shell owns most of the app experience. It starts the app, manages navigation, renders product and cart screens, and makes native mobile HTTP calls to backend APIs. The embedded WebView owns one web-delivered step, such as checkout, sign-in, promo redemption, help, or terms and conditions.

That split is the reason this workshop uses two front-end instrumentation paths:

- **Flutter RUM** for the mobile shell and Flutter screens.
- **Browser RUM** for JavaScript running inside the WebView.
- **APM/OpenTelemetry** for backend APIs called by either layer.

The goal is one understandable user journey in Splunk RUM, not two competing versions of the same session.

## Baseline App Behavior

Before instrumentation, the app already has working product behavior:

| User action | App behavior | What is hard to see before instrumentation |
| ----------- | ------------ | ------------------------------------------ |
| Open app | Flutter starts and renders the home screen. | Startup delay, app lifecycle, device context, and first screen timing. |
| Browse products | Flutter calls `/products` and renders the catalog. | Which users saw slow catalog responses or rendering delays. |
| Add item to cart | Flutter updates cart state and calls `/cart`. | Whether cart failures cluster by version, device, tenant, or release channel. |
| Start checkout | Flutter opens a checkout workflow. | How long checkout takes from the user's perspective. |
| Complete WebView step | Embedded JavaScript loads web assets and calls checkout APIs. | WebView route changes, JavaScript errors, web resource timing, and web-owned API calls. |
| Confirm order | Flutter renders the confirmation screen. | Whether a backend trace explains a slow or failed confirmation. |

Instrumentation does not create these app behaviors. It makes them observable.

## Instrumented Flow

After the workshop changes, the same user journey emits telemetry from the right layer:

```text
Flutter app launch
  -> Flutter RUM session starts
  -> global attributes identify app version, environment, shell, and build flavor
  -> product and cart screens produce navigation, interaction, rendering, and network timing
  -> checkout workflow starts
  -> WebView page loads browser RUM and emits embedded web telemetry
  -> backend APM receives server-side spans
  -> checkout workflow ends with success or privacy-safe failure context
```

The result is not just "more data." The result is a path an engineer can follow during an incident.

## What You Need

- A Splunk Observability Cloud organization.
- A RUM access token.
- Your Splunk realm, such as `us1`, `eu0`, or `au0`.
- A Flutter, hybrid, or WebView-based mobile app that you can build locally.
- Android Studio or Xcode for the target platform.
- Access to backend APM traces if you want to validate front-end to back-end correlation.

{{% notice title="Exercise" style="green" icon="running" %}}

Create a local environment file for your lab values:

```bash
cd workshop/flutter-hybrid-rum
cp .env.example .env
```

Edit `.env` and set:

```bash
SPLUNK_RUM_REALM=us1
SPLUNK_RUM_ACCESS_TOKEN=replace-with-your-rum-token
SPLUNK_RUM_APPLICATION_NAME=mobile-checkout
SPLUNK_RUM_ENVIRONMENT=workshop
SPLUNK_RUM_APP_VERSION=1.0.0
```

Load the values into your current shell before running the Flutter commands later in the workshop:

```bash
set -a
source .env
set +a
```

Keep this file local. Do not commit real tokens.

{{% /notice %}}

## Choose the Agent Path

Use this decision table during the workshop:

| App surface | Recommended path | Notes |
| ----------- | ---------------- | ----- |
| Flutter Android/iOS screens | Splunk RUM Flutter agent | Captures mobile app lifecycle, navigation, interactions, network activity, performance, and crash signals supported by the agent. |
| Native Android/iOS shell around Flutter | Native mobile RUM if shell behavior matters | Use only when native-only screens or shell startup need their own instrumentation plan. Avoid duplicate app identity across agents. |
| WebView, Ionic, Cordova, Capacitor, embedded web checkout | Browser RUM agent in the web bundle | Treat the WebView as browser RUM and tag it so you can distinguish embedded sessions from desktop browser sessions. |
| React Native | Splunk RUM React Native agent | Do not instrument React Native as a generic WebView unless the surface is actually a WebView. |
| Backend APIs | Splunk APM/OpenTelemetry server instrumentation | Required for end-to-end trace correlation beyond the mobile client. |

## Instrumentation Map

Use this map before you edit code:

| App behavior | Where it happens | Instrumentation we add |
| ------------ | ---------------- | ---------------------- |
| App starts and renders the first screen | Flutter `main.dart` and app root | Install `splunk_otel_flutter` before `runApp()`. |
| User browses products and cart | Flutter widgets and navigation stack | Let automatic Flutter RUM capture navigation, interactions, rendering, and mobile network requests. |
| User taps **Add to cart** | Flutter business logic | Add a custom event such as `cart_item_added` with safe attributes. |
| User begins checkout | Flutter workflow boundary | Start a custom workflow named `checkout`. |
| Checkout page is loaded from web content | WebView JavaScript bundle | Initialize browser RUM with `applicationName=mobile-checkout-webview` and `app.platform=hybrid-webview`. |
| API request reaches backend services | Server-side API handlers | Use Splunk APM/OpenTelemetry and preserve trace context. |
| User completes or fails checkout | Flutter or WebView, depending on owner | End the workflow and add a privacy-safe success or failure event. |

## Code Change Plan

You will make four kinds of changes:

1. **Install the Flutter RUM dependency** in the mobile app.
2. **Initialize Flutter RUM** in `main.dart` before the app renders.
3. **Add app-specific context** near the cart and checkout code paths.
4. **Initialize browser RUM** in the WebView's web bundle when the app contains embedded web content.

If you also own the backend, you validate that backend services are instrumented with APM and preserve trace context. If another team owns the backend, you use this workshop to define the contract they need to provide.

{{< tabs >}}
{{% tab title="Question" %}}
**Why not install every available agent in every layer?**
{{% /tab %}}
{{% tab title="Answer" %}}
**Duplicate instrumentation creates noisy sessions, confusing application names, and hard-to-debug trace boundaries. Instrument each runtime once and add shared tags for correlation.**
{{% /tab %}}
{{< /tabs >}}

## Define Consistent Naming

Pick stable names before you add code:

| Field | Example | Why it matters |
| ----- | ------- | -------------- |
| Application name | `mobile-checkout` | Groups mobile sessions in RUM. |
| Environment | `workshop`, `staging`, `production` | Keeps test data away from production views. |
| App version | `1.0.0` or build SHA | Lets teams compare releases. |
| Platform | `flutter`, `capacitor`, `webview` | Separates implementation paths. |
| Build flavor | `debug`, `qa`, `release` | Helps filter non-production sessions. |

{{% notice title="Privacy checkpoint" style="info" %}}
Do not add raw email addresses, names, account numbers, session cookies, authorization headers, or full URLs containing sensitive query strings as RUM attributes. Use stable anonymous IDs, coarse segments, and redacted URLs.
{{% /notice %}}
