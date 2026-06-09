---
title: 5. Capture Mobile Journeys
linkTitle: 5. Capture Journeys
weight: 5
---

RUM automatically captures useful mobile telemetry, but DXA works best when the app reports product-level journey events. In this lab you add explicit events and timed workflows around the steps that matter to the business.

## What automatic RUM cannot know

Automatic RUM can see that a screen appeared, a tap happened, a network request ran, or an error occurred. It cannot reliably know that a tap means "add to cart", that a screen means "checkout started", or that a successful API response means "order submitted".

Custom events and workflows add that product meaning:

| App code location | Instrumentation | Meaning added |
| --- | --- | --- |
| Product detail screen appears | `trackCustomEvent(name: "Product Viewed", ...)` | User entered the product journey. |
| Add-to-cart button handler | `trackCustomEvent(name: "Add To Cart", ...)` | User showed purchase intent. |
| Checkout screen appears | `trackCustomEvent(name: "Checkout Started", ...)` | User entered the conversion funnel. |
| Checkout submission method | `trackWorkflow("Order Submitted")` | App timed the operation that completes conversion. |
| Checkout error handler | `trackCustomEvent(name: "Checkout Failed", ...)` | App marked a business-impacting failure. |

In the included app, those hook points are concentrated in:

```text
workshop/mobile-rum-dxa-ios/InstrumentedShop/InstrumentedShop/WorkshopStore.swift
```

That keeps the teaching flow clear: views call the store, and the store records the RUM/DXA event at the exact point where app state changes.

## Choose workshop events

Create a small event catalog before writing code:

| Event | Trigger | Recommended attributes |
| --- | --- | --- |
| `Product Viewed` | Product or content detail screen appears | `product.category`, `app.feature` |
| `Add To Cart` | User taps add-to-cart or save | `product.category`, `cart.size` |
| `Checkout Started` | User enters checkout | `cart.size`, `checkout.method` |
| `Order Submitted` | User submits order | `checkout.method`, `payment.type` |
| `Checkout Failed` | Checkout returns a handled failure | `error.type`, `checkout.step` |

Keep attributes intentionally low-cardinality. Category, feature, route, and result values are useful. Raw product IDs, order IDs, emails, and addresses usually are not appropriate for RUM analytics attributes.

## Report zero-duration events

Use a zero-duration event for a discrete action, such as tapping `Add To Cart`:

```swift
let attributes: NSDictionary = [
    "app.feature": "cart",
    "product.category": "workshop"
]

SplunkRum.shared.customTracking.trackCustomEvent(
    name: "Add To Cart",
    attributes: attributes
)
```

The supporting example is:

```text
workshop/mobile-rum-dxa-ios/Sources/MobileJourneyInstrumentation.swift
```

Call that helper from the app's button handler.

SwiftUI example:

```swift
Button("Add to cart") {
    cart.add(product)
    MobileJourneyInstrumentation.reportAddToCart(
        category: product.category,
        cartSize: cart.items.count
    )
}
```

UIKit example:

```swift
@IBAction func addToCartTapped(_ sender: UIButton) {
    cart.add(product)
    MobileJourneyInstrumentation.reportAddToCart(
        category: product.category,
        cartSize: cart.items.count
    )
}
```

## Time a workflow

Use a workflow when the operation has meaningful duration:

```swift
let span = SplunkRum.shared.customTracking.trackWorkflow("Checkout Submitted")
span.setAttribute(key: "app.feature", value: "checkout")

defer {
    span.end()
}

// Run checkout submission work here.
```

Workflow spans show up as workflow events in RUM. Those workflow events can then be used as DXA source events or supporting context for funnel analysis.

Wrap the real checkout method so the workflow includes the time spent waiting for validation, API calls, or local persistence:

```swift
try MobileJourneyInstrumentation.runCheckoutSubmission(
    method: "card"
) {
    try checkoutService.submit(cart: cart)
}
```

For async checkout code, keep the same idea: start the workflow before the operation begins, add the result attributes, and end the span after success or failure.

## Validate event design

After implementing events, run a short manual journey:

1. Launch the app.
2. Open a product or content detail screen.
3. Add or save the item.
4. Begin checkout, signup, quote, or booking.
5. Complete the flow once.
6. Trigger one controlled failure, if your demo app supports it.

Use the same event names in code, documentation, and DXA event definitions. Renaming events mid-workshop makes the data harder to explain.
