---
title: 2. Run the Training App
linkTitle: 2. Run App
weight: 2
---

Before adding Splunk RUM, run the included app in training mode. This gives students a concrete mobile journey and a visible telemetry feed.

## Open the project

The Xcode project is here:

```text
workshop/mobile-rum-dxa-ios/InstrumentedShop/InstrumentedShop.xcodeproj
```

Open it in Xcode, select the `InstrumentedShop` scheme, choose the newest available iPhone simulator, and run the app.

The app opens to a catalog. The second tab, **Telemetry**, shows the events that the app records through its training instrumentation layer.

## Command-line build

From the repository root:

```bash
xcodebuild \
  -project workshop/mobile-rum-dxa-ios/InstrumentedShop/InstrumentedShop.xcodeproj \
  -scheme InstrumentedShop \
  -destination 'platform=iOS Simulator,name=iPhone 16 Pro' \
  build
```

If your Xcode installation has multiple simulator runtimes, add the OS version:

```bash
xcodebuild \
  -project workshop/mobile-rum-dxa-ios/InstrumentedShop/InstrumentedShop.xcodeproj \
  -scheme InstrumentedShop \
  -destination 'platform=iOS Simulator,name=iPhone 16 Pro,OS=18.5' \
  build
```

Use the newest installed runtime on your machine. In Xcode, the simulator picker is the easiest way to confirm the exact device and OS names.

{{% notice title="Simulator platform note" style="tip" %}}
If `xcodebuild` says the current iOS platform is not installed, open **Xcode > Settings > Components** and install the matching iOS simulator runtime for that Xcode. The app itself targets iOS 17.0 and newer, but Xcode still needs a compatible simulator platform installed to build and run from the command line.
{{% /notice %}}

## Generate the project after edits

The project is generated from `project.yml`. If you change project structure or build settings and have XcodeGen installed, regenerate it:

```bash
cd workshop/mobile-rum-dxa-ios/InstrumentedShop
xcodegen generate
```

You do not need XcodeGen to run the checked-in project. It is only needed when changing the project definition.

## Walk the app flow

Run this happy path:

1. Open **Shop**.
2. Select a product.
3. Tap **Add to cart**.
4. Open **Review cart**.
5. Tap **Begin checkout**.
6. Tap **Submit order**.
7. Open **Telemetry**.

You should see events such as:

| Event | Why it exists |
| --- | --- |
| `RUM Bootstrap` | The app started the instrumentation layer. |
| `Automatic Navigation Tracking Enabled` | The app enabled automatic RUM screen instrumentation. |
| `Catalog` and `Product Detail` | Screen tracking fired as views appeared. |
| `Product Viewed` | The app reported a product journey event. |
| `Add To Cart` | The add-to-cart button handler reported user intent. |
| `Checkout Started` | The checkout screen became the funnel start. |
| `Sensitive View Marked` | Checkout fields were marked as Session Replay-sensitive. |
| `Order Submitted Started` and `Order Submitted Finished` | The checkout operation was timed as a workflow. |

Now repeat checkout with **Simulate checkout failure** enabled. The app records `Checkout Failed`, which becomes the failure event used later in DXA.

## Where to read the code

Start with:

```text
workshop/mobile-rum-dxa-ios/InstrumentedShop/InstrumentedShop/WorkshopStore.swift
```

That file is intentionally the teaching surface. It contains the app state and every instrumentation call:

- `bootstrapIfNeeded()` starts instrumentation.
- `screenViewed(...)` records readable screen names.
- `productViewed(...)` records product-detail entry.
- `addToCart(...)` records conversion intent.
- `checkoutStarted()` records funnel entry and marks sensitive checkout fields.
- `submitCheckout(...)` records the timed checkout workflow, network request, success, and failure.

The training implementation is:

```text
workshop/mobile-rum-dxa-ios/InstrumentedShop/InstrumentedShop/Instrumentation/TrainingRumInstrumentation.swift
```

Real Splunk RUM examples for the same hook points are in:

```text
workshop/mobile-rum-dxa-ios/InstrumentedShop/InstrumentedShop/Instrumentation/SplunkRumExamples.swift
```

In later labs, students keep the app flow and replace the training implementation with real Splunk RUM calls.
