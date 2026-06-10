---
title: 3. Add Flutter Context and Custom Events
weight: 3
---

Automatic instrumentation gives you the baseline. Useful mobile troubleshooting also needs app-specific context: release identifiers, feature flags, anonymous user segments, tenant IDs, checkout steps, and privacy controls.

In the sample app, this is the difference between seeing "a mobile request was slow" and seeing "checkout slowed down for the `1.0.0` workshop build while a gold-tier test user moved from cart review to payment authorization."

The complete sample app keeps these calls in two places:

| File | Purpose |
| ---- | ------- |
| `flutter-shop/lib/src/rum_service.dart` | Defines the Splunk RUM calls. |
| `flutter-shop/lib/src/shop_store.dart` | Calls the RUM service when cart and checkout business events happen. |

## Add Global Attributes

Global attributes apply to telemetry emitted after they are set. Use them for low-cardinality context that helps operators filter and compare sessions.

{{% notice title="Exercise" style="green" icon="running" %}}

Add a small helper around global attributes:

```dart
import 'package:splunk_otel_flutter/splunk_otel_flutter.dart';

Future<void> configureRumContext({
  required String buildFlavor,
  required String tenantTier,
}) async {
  await SplunkRum.instance.globalAttributes.setAll(
    attributes: MutableAttributes(
      attributes: {
        'app.platform': MutableAttributeString(value: 'flutter'),
        'app.build_flavor': MutableAttributeString(value: buildFlavor),
        'tenant.tier': MutableAttributeString(value: tenantTier),
      },
    ),
  );
}
```

Call it after install and before the user starts the primary workflow.

{{% /notice %}}

## Track Privacy-Safe Users

By default, use anonymous tracking unless your product, legal, and privacy teams have approved a stronger identifier.

{{% notice title="Exercise" style="green" icon="running" %}}

Set the user tracking mode and avoid direct PII:

```dart
await SplunkRum.instance.user.preferences.setTrackingMode(
  trackingMode: UserTrackingMode.anonymousTracking,
);
```

If you need to connect a session to an internal support case, use an opaque ID that cannot be reversed into an email address or account number by itself.

{{% /notice %}}

## Add Custom Events and Workflows

Custom events are useful for domain milestones. Workflows are useful when duration matters, such as checkout, onboarding, search, or login.

For this app:

- `cart_item_added` tells you a user crossed a meaningful product milestone.
- `checkout` measures the full checkout duration.
- `checkout_failed` records a safe failure type without logging payment details, request bodies, names, or email addresses.
- `workshop_custom_event` shows the smallest possible custom event.
- `manual_instrumentation_training` shows a custom workflow that is not tied to checkout.

The last two examples are exposed in the app through **Telemetry status** -> **Open instrumentation examples**.

{{% notice title="Exercise" style="green" icon="running" %}}

Add a domain event for a cart milestone:

```dart
await SplunkRum.instance.customTracking.trackCustomEvent(
  name: 'cart_item_added',
  attributes: MutableAttributes(
    attributes: {
      'cart.item_count': MutableAttributeInt(value: itemCount),
      'catalog.category': MutableAttributeString(value: category),
    },
  ),
);
```

Wrap checkout in a workflow:

```dart
final checkoutWorkflow = await SplunkRum.instance.customTracking.startWorkflow(
  name: 'checkout',
);

try {
  await submitOrder();
  await checkoutWorkflow.end();
} catch (error) {
  await SplunkRum.instance.customTracking.trackCustomEvent(
    name: 'checkout_failed',
    attributes: MutableAttributes(
      attributes: {
        'error.type': MutableAttributeString(value: error.runtimeType.toString()),
      },
    ),
  );
  await checkoutWorkflow.end();
  rethrow;
}
```

{{% /notice %}}

{{< tabs >}}
{{% tab title="Question" %}}
**Which attributes should you avoid adding to every mobile span or event?**
{{% /tab %}}
{{% tab title="Answer" %}}
**Avoid high-cardinality or sensitive values such as raw user names, emails, access tokens, full request bodies, and unrestricted IDs.**
{{% /tab %}}
{{< /tabs >}}

## Manual Screen Tracking

If your navigation stack is custom, verify whether the automatic navigation module captures the route names you expect. If it does not, track important screens manually:

```dart
await SplunkRum.instance.navigation.track(screenName: 'CheckoutReviewScreen');
```

Use names that product, support, and engineering teams already understand.

## Custom Instrumentation Examples in the App

Use the examples screen when you want to demonstrate explicit instrumentation without walking through the full checkout:

| Button | Code path | Telemetry |
| ------ | --------- | --------- |
| **Send custom event** | `RumService.trackWorkshopMilestone()` | Emits `workshop_custom_event` with `workshop.scenario` and `instrumentation.type`. |
| **Run custom workflow** | `RumService.runTrainingWorkflow()` | Starts `manual_instrumentation_training`, emits a step event, and ends the workflow. |

These examples are intentionally small. They show the difference between telemetry the agent can infer automatically and telemetry the application must describe because only the application knows the business meaning.
