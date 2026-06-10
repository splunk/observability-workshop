---
title: 6. Capture Mobile Journeys
weight: 6
time: 15 minutes
description: Add network, navigation, custom event, workflow, error, and backend correlation signals.
---

The default agent modules collect a useful baseline. Add manual signals where your app
has business-specific journeys or UI frameworks that automatic detection cannot name
well.

## What We Are Instrumenting

In the Buttercup reference flow, the important journey is checkout:

```text
Product list -> Product detail -> Cart -> Shipping -> Payment -> Confirmation
```

Automatic instrumentation can tell you that the app launched, a user tapped controls,
screens changed, network calls happened, or the app crashed. Manual instrumentation
adds product context:

| User journey point | Why automatic data is not enough | Manual instrumentation |
| --- | --- | --- |
| `checkout_shipping` screen | Class names or Compose routes might not match user-facing workflow names. | Track a screen name. |
| Shipping step viewed | A tap alone does not say the user reached a checkout funnel step. | Track a custom event. |
| Checkout submit | Several API calls can belong to one user action. | Wrap the operation in a workflow span. |
| Payment validation error | The app catches the error, so it might not crash. | Track a handled exception. |
| Payment API request | Mobile latency needs to connect to backend latency. | Capture network timing and correlate to APM. |

In the included sample app, the manual instrumentation is in:

```text
workshop/android-app-monitoring/app/src/main/java/com/splunk/workshop/androidrum/MainActivity.java
```

## Track Screen Navigation

For XML and Activity/Fragment apps, automatic lifecycle events may be enough for a
first pass. For Jetpack Compose, custom navigators, or meaningful screen names, track
navigation manually.

```kotlin
import com.splunk.rum.integration.navigation.extension.navigation

SplunkRum.instance.navigation.track("checkout_shipping")
```

For Jetpack Compose Navigation, call it when the active route changes:

```kotlin
import com.splunk.rum.integration.navigation.extension.navigation

val navController = rememberNavController()
val currentBackEntry by navController.currentBackStackEntryAsState()
val currentRoute = currentBackEntry?.destination?.route

LaunchedEffect(currentRoute) {
    currentRoute?.let { route ->
        SplunkRum.instance.navigation.track(route)
    }
}
```

Use names that describe product screens, not implementation classes.

## Capture Custom Events

Use custom events for important user actions that are not obvious from taps alone.

```kotlin
import com.splunk.rum.integration.agent.common.attributes.MutableAttributes
import com.splunk.rum.integration.customtracking.extension.customTracking

val attributes = MutableAttributes().also {
    it["cart.item_count"] = 3
    it["checkout.step"] = "shipping"
}

SplunkRum.instance.customTracking.trackCustomEvent(
    "checkout_step_viewed",
    attributes
)
```

Keep event attributes low-cardinality. Avoid raw product IDs, emails, search strings,
and free-form text.

## Track a Workflow Duration

Use workflow spans when a user journey has a start and end point.
In Buttercup, `checkout_submit` starts when the user taps **Place order** and ends
when the app either shows confirmation or reports failure.

```kotlin
import com.splunk.rum.integration.customtracking.extension.customTracking

val checkoutSpan = SplunkRum.instance.customTracking.trackWorkflow("checkout_submit")
try {
    submitCheckout()
} finally {
    checkoutSpan?.end()
}
```

This gives RUM a timing signal that aligns better with the user's task than a single
tap or screen event.

## Report Handled Exceptions

Crashes are captured automatically by the application lifecycle module. Report handled
exceptions when the app catches an error but the user still experiences a failed
workflow.

```kotlin
import com.splunk.rum.integration.agent.common.attributes.MutableAttributes
import com.splunk.rum.integration.customtracking.extension.customTracking

val attributes = MutableAttributes().also {
    it["feature.name"] = "checkout"
    it["error.recoverable"] = true
}

SplunkRum.instance.customTracking.trackException(
    IllegalStateException("Payment method missing"),
    attributes
)
```

## Capture Network Requests

The SDK supports HTTP instrumentation modules for common Android HTTP clients. If the
app uses OkHttp, start by confirming whether it uses manual instrumentation or the
automatic Gradle plugin path. The automatic path requires the matching Gradle plugin
from the previous module. Use the runtime module settings to enable instrumentation and
control safe header capture.

```kotlin
import com.splunk.rum.integration.httpurlconnection.auto.HttpURLModuleConfiguration
import com.splunk.rum.integration.okhttp3.auto.OkHttp3AutoModuleConfiguration

SplunkRum.install(
    application = this,
    agentConfiguration = agentConfiguration,
    moduleConfigurations = arrayOf(
        HttpURLModuleConfiguration(
            isEnabled = true,
            capturedRequestHeaders = listOf("Accept"),
            capturedResponseHeaders = listOf("Content-Type")
        ),
        OkHttp3AutoModuleConfiguration(
            isEnabled = true,
            capturedRequestHeaders = listOf("Accept"),
            capturedResponseHeaders = listOf("Content-Type")
        )
    )
)
```

Header capture is opt-in. Only capture headers that are useful and safe.

## Correlate with Backend Traces

When backend services are instrumented with Splunk APM, RUM can connect mobile network
requests to server-side trace data. The backend must expose compatible trace context,
commonly through the `Server-Timing` response header.

Example response header:

```http
Server-Timing: traceparent;desc="00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01"
```

In the RUM UI, open a network request or session waterfall and look for the link to
the backend trace. If the link is missing, confirm that the backend service is
instrumented and that the response header is not stripped by gateways or mobile API
clients.

## Exercise

Generate data:

1. Open the app.
2. Navigate through at least three screens.
3. Trigger the custom event.
4. Complete or fail the custom workflow.
5. Make at least one backend API call.
6. Trigger one handled exception in a controlled path.
