---
title: 4. Configure RUM for DXA
linkTitle: 4. Configure RUM
weight: 4
---

DXA depends on consistent RUM identity, environment, version, screen, and user-session context. In this lab you make that data explicit.

## What the configuration does

The bootstrap code answers three questions for every mobile signal:

| Question | Configuration | Example |
| --- | --- | --- |
| Where should telemetry be sent? | `realm` and `rumAccessToken` | `us1` and the mobile RUM token. |
| Which app and release produced it? | `appName`, environment, and app version | `ios-dxa-workshop`, `workshop`, `1.0.0`. |
| How should users and screens be grouped? | anonymous tracking and navigation naming | anonymous user/session IDs, `Cart`, `Checkout`. |

Without this configuration, RUM might still collect technical telemetry, but DXA will be harder to use because sessions, events, environments, and releases will not line up cleanly.

## Required configuration

Confirm the agent configuration sets:

| Setting | Why it matters |
| --- | --- |
| `realm` | Routes telemetry to the correct Splunk Observability Cloud realm. |
| `rumAccessToken` | Authorizes RUM telemetry intake. |
| `appName` | Groups telemetry into the RUM mobile application that DXA will use. |
| `deploymentEnvironment` | Separates workshop, staging, and production data. |
| app version | Lets teams compare releases and troubleshoot regressions. |
| anonymous user tracking | Lets DXA correlate events by anonymous user and session. |

Use anonymous tracking for the workshop:

```swift
SplunkRum.shared.user.preferences.trackingMode = .anonymousTracking
```

Disable it only when your privacy policy or consent model requires no user-level correlation:

```swift
SplunkRum.shared.user.preferences.trackingMode = .noTracking
```

{{% notice title="DXA correlation" style="warning" %}}
If user tracking is disabled, RUM can still collect technical telemetry, but DXA user and journey analysis will be limited because events cannot be correlated across an anonymous user session in the same way.
{{% /notice %}}

## Normalize screen names

Automatic navigation tracking is useful, but raw controller names are often too technical for DXA users. Add a navigation event processor when internal class names need to become business-friendly screen names.

For the workshop app, map implementation names to product language:

| Raw app name | DXA-friendly name |
| --- | --- |
| `CatalogViewController` or `CatalogView` | `Catalog` |
| `ProductDetailViewController` or `ProductDetailView` | `Product Detail` |
| `CartViewController` or `CartView` | `Cart` |
| `CheckoutViewController` or `CheckoutView` | `Checkout` |
| `ConfirmationViewController` or `ConfirmationView` | `Order Confirmation` |

Example mapping:

```swift
class WorkshopNavigationProcessor: NavigationEventProcessor {
    func onViewController(
        typeName: String,
        controllerIdentity: String
    ) -> NavigationEvent? {
        let mapped = [
            "ProductDetailViewController": "Product Detail",
            "CartViewController": "Cart",
            "CheckoutViewController": "Checkout"
        ][typeName] ?? typeName.replacingOccurrences(of: "ViewController", with: "")

        return NavigationEvent(
            name: mapped,
            attributes: ["app.feature": "checkout"]
        )
    }
}
```

Pass the processor during install:

```swift
let navigationConfig = NavigationConfiguration(
    isEnabled: true,
    enableAutomatedTracking: true,
    navigationEventProcessor: WorkshopNavigationProcessor()
)

try SplunkRum.install(
    with: agentConfiguration,
    moduleConfigurations: [navigationConfig]
)
```

## Add stable global attributes

Use global attributes for low-cardinality tags that every span should carry:

| Attribute | Example | Use |
| --- | --- | --- |
| `app.team` | `checkout` | Route investigation to the owning team. |
| `app.feature` | `shopping-cart` | Group mobile telemetry by feature area. |
| `release.channel` | `testflight` | Separate production, TestFlight, and internal builds. |
| `tenant.type` | `consumer` | Compare broad user populations without personal data. |

Avoid adding names, emails, account IDs, session secrets, device identifiers, or raw payloads as attributes. If a value identifies a person or a very small population, treat it as sensitive.
