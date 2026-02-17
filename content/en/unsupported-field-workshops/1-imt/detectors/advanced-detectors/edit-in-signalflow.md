---
title: Edit in SignalFlow
linkTitle: 4.2.2 SignalFlow Refactor
weight: 3
---

## Edit in SignalFlow

Navigate to:

**Alerts & Detectors → Detectors**

Locate your detector and open your detector.

From the detector action menu in the upper right hand corner (⋯), select:

**Edit in SignalFlow**

---

## Generated SignalFlow

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
).publish('CMA_NotAdvancedDetector')
```
## What This Is

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

Documentation:  
https://github.com/signalfx/signalflow-library/tree/master/library/signalfx/detectors/against_periods

This approach is convenient, but it bundles threshold generation and alert logic together.  
To build multi-condition logic, we must separate threshold generation from detection logic.

---

## Step 1 – Replace the Import

Remove:

```python
from signalfx.detectors.against_periods import against_periods
```

Replace with:

```python
from signalfx.detectors.against_periods import streams
from signalfx.detectors.against_periods import conditions
```

- `streams` provides functions that generate threshold streams.
- `conditions` provides building blocks for composing alert logic.

Documentation:  
https://github.com/signalfx/signalflow-library/tree/master/library/signalfx/detectors/against_periods

---
## Step 2 – Rename the Signal Stream

Rename the signal from `A` to `CPU` (this improves readability and becomes the stream input to thresholds):

Replace:

```python
A = data('system.cpu.utilization', filter=filter('deployment.environment', 'astronomy-shop')).publish(label='A')
```

With:

```python
CPU = data('system.cpu.utilization', filter=filter('deployment.environment', 'astronomy-shop')).publish(label='CPU')
```

## Step 3 – Replace the Helper Function

Refactor the Wizard-Generated Helper Call (Preserve the Tuned Parameters)

The wizard generated a helper call that already contains the anomaly tuning we want to keep:

- `window_to_compare='10m'`
- `space_between_windows='1d'`
- `num_windows=4`
- `fire_num_stddev=2.5`
- `clear_num_stddev=2`
- `discard_historical_outliers=True`

Documentation:  
https://github.com/signalfx/signalflow-library/tree/master/library/signalfx/detectors/against_periods

The goal is **not** to retype these values. The goal is to keep them and convert the helper call into explicit threshold streams.

---

## Convert the Helper Call into Threshold Streams

In the existing code, locate this line:

```python
against_periods.detector_mean_std(
```

Replace **only that function name** with:

```python
fire_bot, clear_bot, clear_top, fire_top = streams.mean_std_thresholds(
```

Then update the stream argument to use the renamed stream:

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

`streams.mean_std_thresholds()` generates threshold streams.  
It does **not** implement detector behaviors such as orientation or auto-resolve.

Remove these lines from the parameter list:

```python
orientation='above',
auto_resolve_after='1h'
```

---

## Remove the Helper Publish

The helper call publishes a detector directly:

```python
).publish('CMA_NotAdvancedDetector')
```

`streams.mean_std_thresholds()` does not publish a detector, so remove the publish entirely.


---

## Step 4 – Add Multi-Condition Detect Logic

Now that you have a reusable anomaly threshold stream (`fire_top`), define your detector logic explicitly:

```python
detect(CPU > fire_top and when(CPU > threshold(90), lasting='15m')).publish('custom_CPU_detector')
```

This expresses two conditions:

- **Historical baseline anomaly:** `CPU > fire_top`
- **Static guardrail:** `CPU > 90` sustained for **15 minutes**

---

## Step 5 – (Optional) Publish the Threshold Stream

To visualize and/or reference the computed anomaly threshold:

```python
fire_top.publish('CPU_top_threshold')
```

## Result

You have replaced a bundled helper-based detector with:

- Explicit threshold generation
- Composable alert logic
- Static guardrails
- Sustained evaluation
- Reusable threshold streams