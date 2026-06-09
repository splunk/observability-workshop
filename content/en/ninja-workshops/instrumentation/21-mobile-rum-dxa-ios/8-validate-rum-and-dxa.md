---
title: 8. Validate RUM and DXA
linkTitle: 8. Validate
weight: 8
---

In this lab you confirm that iOS RUM data is usable, then create DXA project artifacts from the mobile events.

## Validate in RUM

In Splunk Observability Cloud:

1. Open **RUM**.
2. Select **Mobile**.
3. Find the app name from your configuration.
4. Filter to `deployment.environment = workshop`.
5. Confirm that new sessions appear after you run the app.

Open a session and check for:

- app start and navigation events,
- screen names that make sense to a product or support user,
- tap or interaction activity,
- network spans,
- custom workflow events,
- errors or crashes, if you generated them,
- Session Replay availability, if enabled.

If no sessions appear, check the app logs and confirm the realm, token, app target, and network connectivity.

## Create a DXA project

In Splunk Observability Cloud:

1. Open **Digital Experience Analytics**.
2. Select **Create project**.
3. Name the project `iOS DXA Workshop`.
4. Add the RUM mobile application from this workshop.
5. Add a description such as `Mobile checkout journey analysis`.
6. Create the project.

## Create event definitions

Create event definitions from the mobile RUM events:

| Event definition | Source event pattern | Why it matters |
| --- | --- | --- |
| `Product viewed` | screen or workflow event for product detail | Entry point for the mobile journey. |
| `Add to cart` | `Add To Cart` custom event | First conversion signal. |
| `Begin checkout` | checkout screen or `Checkout Started` event | Funnel start. |
| `Order submitted` | `Order Submitted` workflow event | Conversion completion. |
| `Checkout failed` | handled error or `Checkout Failed` event | Technical friction. |

Use the event names and attributes you implemented in the app. If event definitions are too broad, add filters such as `app.feature = checkout` or `deployment.environment = workshop`.

## Build segments and analyses

Create these user segments:

| Segment | Criteria | Use |
| --- | --- | --- |
| `Workshop users` | `deployment.environment = workshop` | Keep lab data isolated. |
| `Checkout visitors` | users with `Begin checkout` | Measure checkout behavior. |
| `Abandoned checkout` | users with `Begin checkout` and without `Order submitted` | Investigate drop-off. |
| `Error affected users` | users with `Checkout failed` | Compare failures to conversion. |

Create a conversion funnel:

1. `Product viewed`
2. `Add to cart`
3. `Begin checkout`
4. `Order submitted`

Create a time series analysis for:

- `Add to cart`,
- `Begin checkout`,
- `Order submitted`,
- `Checkout failed`.

When an analysis highlights a drop-off or spike, open affected RUM sessions and use waterfalls, errors, crashes, and Session Replay to understand what happened.

{{< tabs >}}
{{% tab title="Question" %}}
Why create DXA event definitions when RUM already has sessions?
{{% /tab %}}
{{% tab title="Answer" %}}
RUM sessions are best for technical troubleshooting of individual experiences. DXA event definitions turn those sessions into reusable behavioral concepts such as checkout start, conversion, abandonment, and error-affected users.
{{% /tab %}}
{{< /tabs >}}
