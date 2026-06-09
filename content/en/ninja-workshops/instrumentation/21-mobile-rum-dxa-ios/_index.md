---
title: Mobile Instrumentation for RUM and DXA on iOS
linkTitle: Mobile RUM and DXA for iOS
weight: 21
archetype: chapter
time: 90 minutes
authors: ["Splunk"]
description: Instrument a native iOS application with Splunk RUM, capture mobile journey events for Digital Experience Analytics, enable privacy-safe Session Replay, and operationalize dSYM uploads.
draft: false
hidden: false
---

Digital Experience Analytics (DXA) uses Splunk Real User Monitoring (RUM) data to analyze mobile user journeys, adoption, conversion friction, and frustration signals. In this workshop you will instrument a native iOS application with the Splunk RUM iOS agent, add journey-level events, enable privacy-safe Session Replay, upload dSYMs for crash symbolication, and build DXA analyses from the resulting RUM data.

Some teams refer to this capability as DEA in conversation. Splunk product documentation uses **DXA** for Digital Experience Analytics, so this workshop uses DXA throughout.

## Workshop goals

- Add the Splunk RUM iOS agent through Swift Package Manager.
- Configure RUM with realm, RUM token, application name, environment, version, and anonymous user tracking.
- Capture mobile screens, taps, network activity, crashes, slow rendering signals, and custom journey events.
- Protect sensitive data with span interception and Session Replay sensitivity settings.
- Upload iOS dSYMs through the `splunk-rum` CLI so RUM crashes are symbolicated.
- Create DXA event definitions, user segments, funnels, and time series views from mobile RUM data.

## Lab files

The runnable iOS training app and supporting snippets for this workshop are in:

```text
workshop/mobile-rum-dxa-ios/
```

Start with the included `InstrumentedShop` SwiftUI app. It runs in training mode without Splunk credentials and shows each instrumentation event in a local telemetry tab. After students understand the flow, the same hook points can be wired to Splunk RUM in their own app.

## Workshop app story

Use the workshop as if you are instrumenting a small shopping app:

```text
Launch app
  -> browse catalog
  -> view product detail
  -> add item to cart
  -> open cart
  -> start checkout
  -> submit order
  -> see confirmation or checkout error
```

The app does not need a real payment processor or production backend. It only needs a few screens, buttons, and one path that can succeed or fail. That gives RUM enough activity to capture app launches, screen changes, taps, network calls, handled errors, and replay frames. It gives DXA enough business events to build a funnel from product discovery to order submission.

## How instrumentation is added

The workshop adds instrumentation in layers:

| Layer | Where it goes | What it creates |
| --- | --- | --- |
| RUM package | Xcode Swift Package Manager | Makes the Splunk RUM iOS agent available to the app target. |
| Bootstrap | SwiftUI `App.init()` or UIKit app delegate startup | Starts RUM once, sets realm/token/app/environment, and enables automatic navigation tracking. |
| Navigation naming | RUM install configuration | Converts technical controller names into readable screen names such as `Product Detail` and `Checkout`. |
| Custom journey events | Button handlers and checkout methods | Creates DXA-friendly events such as `Add To Cart`, `Checkout Started`, and `Order Submitted`. |
| Session Replay privacy | View setup and reusable sensitive components | Records the session while hiding fields, payment containers, account details, and WebView content. |
| Span interception | RUM agent configuration | Redacts sensitive exported metadata such as full URLs before telemetry leaves the device. |
| dSYM upload | Release or CI pipeline | Makes mobile crash stacks readable in RUM. |

## App code

The runnable app lives here:

```text
workshop/mobile-rum-dxa-ios/InstrumentedShop/
```

Key files:

| File | Purpose |
| --- | --- |
| `InstrumentedShop/WorkshopStore.swift` | Owns cart and checkout state, and calls the instrumentation layer at each business event. |
| `InstrumentedShop/Instrumentation/TrainingRumInstrumentation.swift` | Local stand-in for Splunk RUM that records events to the app's Telemetry tab. |
| `InstrumentedShop/Views/*.swift` | SwiftUI screens for catalog, product detail, cart, checkout, confirmation, and telemetry. |
| `project.yml` | XcodeGen source for the Xcode project. |
| `InstrumentedShop.xcodeproj` | Generated Xcode project that students can open directly. |

## References

- [Set up Digital Experience Analytics in Splunk RUM](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/digital-experience-analytics/set-up-digital-experience-analytics)
- [Instrument mobile and web applications for Splunk RUM](https://help.splunk.com/en/splunk-observability-cloud/manage-data/instrument-front-end-applications/instrument-mobile-and-web-applications-for-splunk-real-user-monitoring-rum)
- [Splunk RUM iOS agent version 2.0.0 and above](https://help.splunk.com/en/splunk-observability-cloud/manage-data/instrument-front-end-applications/instrument-mobile-and-web-applications-for-splunk-real-user-monitoring-rum/instrument-ios-applications-for-splunk-rum/splunk-rum-ios-agent-version-2.0.0-and-above)
- [Install the Splunk RUM iOS agent](https://help.splunk.com/en/splunk-observability-cloud/manage-data/instrument-front-end-applications/instrument-mobile-and-web-applications-for-splunk-real-user-monitoring-rum/instrument-ios-applications-for-splunk-rum/splunk-rum-ios-agent-version-2.0.0-and-above/install-the-splunk-rum-ios-agent)
- [Configure the Splunk RUM iOS agent](https://help.splunk.com/en/splunk-observability-cloud/manage-data/instrument-front-end-applications/instrument-mobile-and-web-applications-for-splunk-real-user-monitoring-rum/instrument-ios-applications-for-splunk-rum/splunk-rum-ios-agent-version-2.0.0-and-above/configure-the-splunk-rum-ios-agent)
- [Manually instrument iOS applications](https://help.splunk.com/en/splunk-observability-cloud/manage-data/instrument-front-end-applications/instrument-mobile-and-web-applications-for-splunk-real-user-monitoring-rum/instrument-ios-applications-for-splunk-rum/splunk-rum-ios-agent-version-2.0.0-and-above/manually-instrument-ios-applications)
- [Record iOS sessions](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/real-user-monitoring/replay-user-sessions/record-ios-sessions)
- [Add dSYMs](https://help.splunk.com/en/splunk-observability-cloud/manage-data/instrument-front-end-applications/instrument-mobile-and-web-applications-for-splunk-real-user-monitoring-rum/instrument-ios-applications-for-splunk-rum/splunk-rum-ios-agent-version-2.0.0-and-above/add-dsyms)
