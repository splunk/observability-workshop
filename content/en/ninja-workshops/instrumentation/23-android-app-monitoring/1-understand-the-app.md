---
title: 1. Understand the App and Instrumentation Plan
weight: 1
time: 10 minutes
description: Understand the reference Android app, its user journey, and where monitoring code will be added.
---

This workshop uses a fictional Android shopping app called **Buttercup** as the
reference app. Buttercup is intentionally ordinary: it has screens, buttons, API
calls, successful journeys, and failure paths. That makes it a useful model for most
mobile apps.

You can use your own Android app instead. When you see a Buttercup screen or workflow,
replace it with the equivalent screen or workflow in your app.

## What Buttercup Does

Buttercup lets a user browse products and place an order.

```text
Open app
  -> Browse products
  -> View product details
  -> Add item to cart
  -> Enter shipping information
  -> Submit payment
  -> View order confirmation
```

The app has three kinds of behavior that matter for monitoring:

| Behavior | Example | What the user feels |
| --- | --- | --- |
| Screen flow | Product list to cart to checkout | "Is the app responsive and easy to use?" |
| Backend calls | Catalog, cart, shipping, payment, order APIs | "Why is this screen slow or stuck?" |
| Failure paths | Payment validation error, API timeout, crash | "Why did checkout fail?" |

Splunk RUM helps connect those behaviors into one mobile session.

## App Areas Used in the Workshop

Use this model to map Buttercup to your own app.

| Buttercup area | Typical Android code location | What happens there |
| --- | --- | --- |
| App startup | `Application`, main `Activity` | The process starts and the first screen loads. |
| Product list | Activity, fragment, or Compose route | The user sees catalog data from a backend API. |
| Product detail | Activity, fragment, or Compose route | The user opens one item and might add it to the cart. |
| Cart | View model, repository, API client | The app updates cart state and calls cart APIs. |
| Checkout shipping | View model and validation logic | The app validates user input and records checkout progress. |
| Checkout payment | Payment view model, repository, API client | The app submits payment and waits on backend services. |
| Confirmation | Activity, fragment, or Compose route | The app reports that checkout completed successfully. |

The workshop does not require these exact class names. The important part is knowing
which code owns startup, navigation, API calls, checkout, and error handling.

## What We Add

We add monitoring in five layers. Each layer answers a different question.

| Layer | Code change | Question answered |
| --- | --- | --- |
| SDK dependency | Add Splunk RUM Android to Gradle | Can this app send mobile telemetry? |
| Agent startup | Call `SplunkRum.install()` in `Application.onCreate()` | Which app, version, environment, and realm produced this session? |
| Automatic modules | Enable lifecycle, rendering, crash, ANR, interaction, and HTTP modules | What happened without custom app code? |
| Manual app context | Track screen names, custom events, workflows, and handled exceptions | What business journey was the user trying to complete? |
| Release metadata | Upload R8/ProGuard mapping files in CI | Can production crash stack traces be understood? |

## What the SDK Captures Automatically

After the SDK starts, automatic modules can capture baseline signals:

- App startup and lifecycle transitions.
- User interactions such as taps.
- Slow and frozen rendering.
- Crashes and ANRs.
- Supported HTTP client requests.
- Device, OS, app version, and environment metadata.

Automatic data is useful, but it usually does not know product intent. A tap on a
button is not the same as "the user submitted checkout." That context comes from
manual instrumentation.

## What We Instrument Manually

Manual instrumentation is small and targeted. In this workshop, it focuses on checkout.

| User action | Manual signal | Why it matters |
| --- | --- | --- |
| User reaches shipping | Screen name `checkout_shipping` | Groups sessions by user-facing workflow, not internal class names. |
| User views a checkout step | Custom event `checkout_step_viewed` | Shows funnel progress through checkout. |
| User submits checkout | Workflow span `checkout_submit` | Times the full user action across multiple app and API operations. |
| App catches payment error | Handled exception | Surfaces failed experiences that do not crash the app. |
| App calls payment API | HTTP span and APM correlation | Connects mobile latency to backend trace latency. |

## Before and After

Before instrumentation, a user might report: "Checkout is slow and sometimes fails."
You might only have backend logs, crash reports, or support tickets.

After instrumentation, Splunk RUM can show:

- Which app version and environment the user ran.
- Which screen the user was on.
- Whether rendering, network, or backend latency dominated the experience.
- Whether the app crashed, froze, or caught an exception.
- Whether the payment API call links to a backend APM trace.
- Whether other users saw the same issue.

## Exercise

Choose the journey you will instrument.

| Buttercup example | Your app equivalent |
| --- | --- |
| Product list |  |
| Product detail |  |
| Cart |  |
| Checkout shipping |  |
| Checkout payment |  |
| Confirmation |  |
| Primary API client |  |
| Most important handled error |  |

Keep this mapping open while you complete the rest of the workshop.
