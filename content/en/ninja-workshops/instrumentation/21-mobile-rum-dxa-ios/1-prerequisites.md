---
title: 1. Prerequisites
linkTitle: 1. Prerequisites
weight: 1
---

Before you instrument iOS for RUM and DXA, make sure the app, Splunk organization, and build environment are ready.

## Required Splunk values

- **Realm**: your Splunk Observability Cloud realm, such as `us0`, `us1`, `eu0`, or `au0`.
- **RUM access token**: the token used by the mobile app to send RUM telemetry.
- **Application name**: the RUM application name that will be added to a DXA project.
- **Deployment environment**: for example `workshop`, `staging`, or `production`.
- **Application version**: the version or build identifier shipped to users.
- **DXA access**: Digital Experience Analytics must be available in your Splunk Observability Cloud organization.
- **API access token**: required later for the `splunk-rum` CLI dSYM upload workflow. This is not the RUM token.

{{% notice title="DXA data source" style="info" %}}
DXA does not require a separate iOS SDK. It uses data collected by Splunk RUM. For mobile applications, use Splunk RUM iOS agent version 2.0.0 or later for DXA capability, and keep anonymous user tracking enabled unless your privacy policy requires otherwise.
{{% /notice %}}

## Required tools

For the hands-on lab you need:

- macOS with Xcode.
- An iOS app that can run in the Simulator or on a test device.
- Swift Package Manager access from Xcode.
- Node.js 18 or later for the `splunk-rum` CLI used in dSYM upload.
- Access to Splunk Observability Cloud.

## Prepare workshop values

Copy the example environment file and fill it in for your organization:

```bash
cd workshop/mobile-rum-dxa-ios
cp .env.example .env
```

Example values:

```bash
SPLUNK_REALM=us1
SPLUNK_RUM_ACCESS_TOKEN=replace-with-your-rum-token
SPLUNK_RUM_APPLICATION_NAME=ios-dxa-workshop
SPLUNK_RUM_ENVIRONMENT=workshop
SPLUNK_RUM_APP_VERSION=1.0.0
SPLUNK_ACCESS_TOKEN=replace-with-your-org-api-token
```

The RUM token belongs in app configuration. The API access token belongs only in build or CI systems that upload source maps, mapping files, or dSYMs.

## Decide the workshop app

Use one of these options:

| Option | Best for | Notes |
| --- | --- | --- |
| Included `InstrumentedShop` app | Workshop delivery | Use this first so everyone sees the same screens and events. |
| Existing internal app | Real rollout practice | Use a non-production target and a test RUM app name. |
| New SwiftUI app | Fastest local lab | Create a small Xcode app with a few screens and buttons. |
| Existing demo app | Instructor-led delivery | Keep the app stable so screenshots and navigation names match. |

Create or identify at least four user actions for the DXA portion:

- open product or content detail,
- add or save an item,
- begin checkout, booking, quote, or signup,
- complete or fail the flow.

These actions become the mobile journey events in later labs.

## Define the app behavior

For the rest of the workshop, map your app to this simple journey:

| Workshop screen | User action | App behavior | RUM/DXA signal |
| --- | --- | --- | --- |
| Catalog | User opens the app and browses products or content | The first screen loads and may fetch data from an API | App start, screen view, resource spans. |
| Product Detail | User opens an item | The app displays item details and a primary action | Screen view plus `Product Viewed`. |
| Cart | User taps add-to-cart or save | The cart count changes locally or through an API call | Tap interaction plus `Add To Cart`. |
| Checkout | User starts checkout | The app displays shipping, account, or payment controls | Screen view plus `Checkout Started`. |
| Confirmation | User submits successfully | The app shows a confirmation state | Timed workflow `Order Submitted`. |
| Error State | User hits a controlled failure | The app shows a handled error message | Custom event `Checkout Failed` and any related error telemetry. |

If your app is not commerce, rename the screens while keeping the same shape:

- catalog can be home, search results, or account overview,
- product detail can be article, quote, policy, trip, or item detail,
- cart can be saved item, booking draft, or form review,
- checkout can be signup, quote submission, appointment booking, or payment.

The important part is the instrumentation pattern: automatic RUM captures technical activity, and custom events describe the product journey in language that DXA users understand.
