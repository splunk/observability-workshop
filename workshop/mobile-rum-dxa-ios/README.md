# Mobile RUM and DXA for iOS Workshop Assets

This directory contains reference snippets for the iOS mobile RUM and Digital Experience Analytics workshop.

The workshop content is in:

```text
content/en/ninja-workshops/instrumentation/21-mobile-rum-dxa-ios/
```

## App used by the workshop

The workshop assumes a simple iOS shopping flow:

```text
Catalog -> Product Detail -> Cart -> Checkout -> Confirmation or Error
```

You can use any app with the same shape. The goal is to show how automatic RUM captures technical behavior while custom events and workflows explain the product journey for DXA.

## Files

- `.env.example`: placeholder values for instructor and learner setup.
- `InstrumentedShop/`: runnable SwiftUI iOS training app with a local telemetry tab.
- `Sources/RUMBootstrap.swift`: example Splunk RUM iOS agent bootstrap.
- `Sources/MobileJourneyInstrumentation.swift`: examples for custom events and workflow spans.
- `Sources/PrivacySpanInterceptor.swift`: example metadata redaction with `spanInterceptor`.
- `scripts/upload-dsyms.sh`: wrapper for `splunk-rum ios upload` and `splunk-rum ios list`.

The `InstrumentedShop` app is a complete Xcode project. The files under `Sources/` are focused snippets to copy into another Xcode application target.

## Quick checklist

1. Open `InstrumentedShop/InstrumentedShop.xcodeproj`.
2. Run the app in an iPhone simulator.
3. Complete the catalog-to-checkout flow and inspect the Telemetry tab.
4. Add `https://github.com/signalfx/splunk-otel-ios` through Swift Package Manager.
5. Add the `SplunkAgent` package to the app target.
6. Replace the training instrumentation with real Splunk RUM calls.
7. Validate the app in Splunk RUM.
8. Create DXA event definitions from the mobile RUM events.
9. Upload dSYMs from release archives with the CLI script.
