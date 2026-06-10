# Instrumented Shop iOS Training App

Instrumented Shop is a small SwiftUI app for the mobile RUM and DXA workshop. It runs in training mode without Splunk credentials and shows captured instrumentation events in the **Telemetry** tab.

The app flow is:

```text
Catalog -> Product Detail -> Cart -> Checkout -> Confirmation or Error
```

Each screen and user action maps to a RUM or DXA concept:

| App action | Training event | Real Splunk RUM equivalent |
| --- | --- | --- |
| App launch | `RUM Bootstrap` | `SplunkRum.install(...)` during startup. |
| Bootstrap configuration | `Automatic Navigation Tracking Enabled` | `navigation.preferences.enableAutomatedTracking = true`. |
| Screen appears | `Catalog`, `Product Detail`, `Cart`, `Checkout` | automatic navigation tracking with readable screen names. |
| Product opens | `Product Viewed` | `customTracking.trackCustomEvent`. |
| Add-to-cart tap | `Add To Cart` | `customTracking.trackCustomEvent`. |
| Checkout starts | `Checkout Started` | custom journey event for DXA funnel start. |
| Submit order | `Order Submitted Started/Finished` | `customTracking.trackWorkflow`. |
| Controlled failure | `Checkout Failed` | custom event plus error attributes. |
| Checkout fields appear | `Sensitive View Marked` | Session Replay sensitivity configuration. |

## Run from Xcode

1. Open `InstrumentedShop.xcodeproj`.
2. Select the `InstrumentedShop` scheme.
3. Select an iPhone simulator.
4. Run the app.

## Run from the command line

From the repository root, use the newest iPhone simulator installed with your Xcode. Example:

```bash
xcodebuild \
  -project workshop/mobile-rum-dxa-ios/InstrumentedShop/InstrumentedShop.xcodeproj \
  -scheme InstrumentedShop \
  -destination 'platform=iOS Simulator,name=iPhone 16 Pro' \
  build
```

If you have multiple runtimes installed, include the OS version shown in Xcode's simulator picker:

```bash
xcodebuild \
  -project workshop/mobile-rum-dxa-ios/InstrumentedShop/InstrumentedShop.xcodeproj \
  -scheme InstrumentedShop \
  -destination 'platform=iOS Simulator,name=iPhone 16 Pro,OS=18.5' \
  build
```

## Learning path

1. Run the app in training mode.
2. Complete the happy path and inspect the **Telemetry** tab.
3. Repeat checkout with **Simulate checkout failure** enabled.
4. Open `WorkshopStore.swift` to see where the app calls the instrumentation layer.
5. Open `TrainingRumInstrumentation.swift` to see the local stand-in for Splunk RUM.
6. Open `SplunkRumExamples.swift` for real Splunk examples:
   - `SplunkRumAutoInstrumentationExample` shows package bootstrap, global attributes, span redaction, anonymous tracking, automatic navigation, and Session Replay startup.
   - `SplunkRumCustomInstrumentationExample` shows screen naming, custom events, checkout workflow spans, and failure attributes.
7. In the workshop labs, add the Splunk RUM iOS package and replace the training implementation with real Splunk RUM calls.
