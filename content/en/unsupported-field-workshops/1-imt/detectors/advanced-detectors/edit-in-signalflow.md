---
title: SignalFlow Refactor with Multiple Conditions
linkTitle: 4.2.2 Edit in SignalFlow
weight: 3
---

## Objective

Refactor the wizard-generated detector to:

- Separate threshold calculation from alert logic
- Compose multiple conditions in a single `detect()` statement
- Introduce a static operational guardrail
- Surface dynamic anomaly thresholds for reuse in alert messages

---

## Edit in SignalFlow

From the detector action menu in the upper right hand corner **(⋯)**, select **Edit in SignalFlow**

You should still be in the Detector UI for the detector you just saved, if not: 

Navigate to:

**Alerts & Detectors → Detectors**

Locate your detector and open it, then **Edit in SignalFlow.**

---

## Generated SignalFlow
Choose the **SignalFlow** tab and review the generated SignalFlow for the historical anomaly detector. 

{{% notice title="Notice on Format" style="info" %}}
Note that the format of ```against_periods.detector_mean_std``` function is on a single line. You an either add line returns after each parameter or copy and paste the same formatted SignalFlow below for readability.
{{% /notice %}}

```python
from signalfx.detectors.against_periods import against_periods

A = data(
  'system.cpu.utilization',
  filter=filter('deployment.environment', 'astronomy-shop')
).publish(label='A')

against_periods.detector_mean_std(
  stream=A,
  window_to_compare='10m',
  space_between_windows='1d',
  num_windows=4,
  fire_num_stddev=2.5,
  clear_num_stddev=2,
  discard_historical_outliers=True,
  orientation='above',
  auto_resolve_after='1h'
).publish('XYZ_AdvancedDetector')
```

---

## Why We Are Refactoring

The wizard generated the detector using:

```
against_periods.detector_mean_std()
```

This helper function:

- Calculates historical baseline thresholds  
- Applies fire and clear logic  
- Applies orientation (`above` / `below`)  
- Handles auto-resolve timing  
- Publishes the detector in a single call  

While convenient, this structure bundles threshold generation and alert behavior together.  
To build multi-condition logic, we must separate threshold calculation from detection logic.

{{% notice title="SignalFlow Detector Library" style="info" %}}
Explore the underlying helper functions and threshold stream implementations used in this lab.

[View SignalFlow Detector Library Documentation](https://github.com/signalfx/signalflow-library/blob/master/library/signalfx/detectors/against_periods/README.md)
{{% /notice %}}

---

## Step 1 – Replace the Import

Remove:

```python
from signalfx.detectors.against_periods import against_periods
```

Replace with:

```python
#import from SignalFx Library
from signalfx.detectors.against_periods import streams
from signalfx.detectors.against_periods import conditions
```

- `streams` generates reusable threshold streams.
- `conditions` enables logical composition in `detect()`.

---

## Step 2 – Rename the Signal Stream

Rename the signal from `A` to `CPU` for clarity.

Replace:

```python
A = data('system.cpu.utilization', filter=filter('deployment.environment', 'astronomy-shop')).publish(label='A')
```

With:

```python
#Calculate/filter CPU
CPU = data('system.cpu.utilization', filter=filter('deployment.environment', 'astronomy-shop')).publish(label='CPU')
```

---

## Step 3 – Convert the Helper Call into Threshold Streams

The wizard-generated helper already contains the anomaly tuning we want to preserve:

- `window_to_compare='10m'`
- `space_between_windows='1d'`
- `num_windows=4`
- `fire_num_stddev=2.5`
- `clear_num_stddev=2`
- `discard_historical_outliers=True`

We will keep these values.

Locate:

```python
against_periods.detector_mean_std(
```

Replace only the function name with:

```python
#Use the streams.mean_std_thresholds function to establish the built in min/max fire and clear threshold conditions
fire_bot, clear_bot, clear_top, fire_top = streams.mean_std_thresholds(
```

Update the stream argument:

Replace:

```python
stream=A,
```

With:

```python
CPU,
```

---

## Remove Helper-Only Alert Parameters

`streams.mean_std_thresholds()` generates threshold streams only.  
It does not implement detector behaviors such as orientation or auto-resolve.

Remove:

```python
orientation='above',
auto_resolve_after='1h'
```

---

## Remove the Helper Publish

The helper call publishes a detector directly:

```python
).publish('XYZ_AdvancedDetector')
```

`streams.mean_std_thresholds()` does not publish a detector.  

**Remove** ```.publish('XYZ_AdvancedDetector')```

---

## Step 4 – Add Multi-Condition Detect Logic

Now that threshold generation and alert logic are separated, you must explicitly define the detection criteria.

First, define the static guardrail as its own stream by appending:

```python
#Define static threshold for CPU as a variable 
static_threshold = threshold(.90)
```

This creates a constant threshold stream at 90%.  
By defining it as a stream (instead of embedding `threshold(.90)` directly inside `detect()`), it can be published, visualized, and referenced in alert messages.

Next, define the multi-condition detection logic:

```python
#detect when CPU has exceeded the fire_top thresholds established AND CPU exceeds static threshold (90%) for 15 minutes; publish detector
detect(
  CPU > fire_top and when(CPU > static_threshold, lasting='15m')
).publish('custom_CPU_detector')
```

This detect statement evaluates two independent conditions:

1. **Historical baseline anomaly**  
   `CPU > fire_top`  
   The 10-minute moving average exceeds the dynamically calculated anomaly threshold.

2. **Static operational guardrail with duration**  
   `when(CPU > static_threshold, lasting='15m')`  
   CPU must remain above 90% for 15 consecutive minutes.

Both conditions must evaluate to true before the detector fires.

You now control exactly how anomaly behavior and operational thresholds interact.
This introduces:

- **Historical baseline anomaly:** `CPU > fire_top`
- **Static operational guardrail:** `CPU > static_threshold`
- **Sustained violation requirement:** 15 minutes
- Explicit detector publication

---

## Step 5 – Publish Threshold Streams for Preview and Messaging

To surface both thresholds for detector preview and alert messaging:

```python
#publish the fire_top threshold and static_threshold for data visualization
fire_top.publish('CPU_top_threshold')
static_threshold.publish('CPU_static_threshold')
```

---

## Result
{{< tabs >}}
{{% tab title="Results" %}}

You have transformed a wizard convenience helper into:

- Explicit threshold generation  
- Composable multi-condition alert logic  
- Static guardrail enforcement  
- Sustained evaluation logic  
- Reusable anomaly and static threshold streams  

This structure provides greater precision, flexibility, and clarity in detector behavior.
{{% /tab %}}
{{% tab title="Final SignalFlow" %}}
```python
#import from SignalFx Library
from signalfx.detectors.against_periods import streams
from signalfx.detectors.against_periods import conditions

#Calculate/filter CPU
CPU = data('system.cpu.utilization', filter=filter('deployment.environment', 'astronomy-shop')).publish(label='CPU')

#Use the streams.mean_std_thresholds function to establish the built in min/max fire and clear threshold conditions
fire_bot, clear_bot, clear_top, fire_top = streams.mean_std_thresholds(
  CPU,
  window_to_compare='10m',
  space_between_windows='1d',
  num_windows=4,
  fire_num_stddev=2.5,
  clear_num_stddev=2,
  discard_historical_outliers=True,
)

#Define static threshold for CPU as a variable
static_threshold = threshold(.90)

#detect when CPU has exceeded the fire_top thresholds established AND CPU exceeds static threshold (90%) for 15 minutes; publish detector
detect(
  CPU > fire_top and when(CPU > static_threshold, lasting='15m')
).publish('custom_CPU_detector')

#publish the fire_top threshold and static_threshold for data visualization
fire_top.publish('CPU_top_threshold')
static_threshold.publish('CPU_static_threshold')
```
{{% /tab %}}
{{< /tabs >}}

{{% notice title="Static Threshold in Alert Messages" style="info" %}}
Because the static guardrail is defined and published:

```python
static_threshold.publish('CPU_static_threshold')
```

it is now available in the custom alert message as:

```
{{inputs.CPU_static_threshold.value}}
```

Any published stream in SignalFlow becomes accessible as `inputs.<stream_name>.value` in alert messaging.
{{% /notice %}}
