---
title: 2. RUM instrumentation in a browser app
linkTitle:  2. RUM instrumentation
weight: 2
---

* Check the HEAD section of the Online-boutique webpage in your browser
* Find the code that instruments RUM

---

## 1. Browse to the Online Boutique

Your workshop instructor will provide you with the Online Boutique URL that has RUM installed so that you can complete the next steps.

## 2.  Inspecting the HTML source

The changes needed for RUM are placed in the `<head>` section of the hosts Web page. Below is the updated `<head>` section with the changes required to enable RUM:

![Online Boutique](../images/rum-inst.png)

This code enables RUM Tracing, [Session Replay](https://docs.splunk.com/observability/en/rum/rum-session-replay.html), and [Custom Events](https://docs.splunk.com/observability/en/rum/RUM-custom-events.html) to better understand performance in the context of user workflows:

* The first part is to indicate where to download the Splunk Open Telemetry Javascript file from: `https://cdn.signalfx.com/o11y-gdi-rum/latest/splunk-otel-web.js` (this can also be hosted locally if so required).
* The next section defines the location where to send the traces to in the beacon url: `{beaconUrl: "https://rum-ingest.eu0.signalfx.com/v1/rum"`
* The RUM Access Token:  `rumAuth: "<redacted>"`.
* Identification tags `app` and `environment` to indentify in the SPLUNK RUM UI e.g.  `app: "frontend-demo-us-store", environment: "frontend-demo-us"}` (these values will be different in your workshop)

The above lines 21 and 23-30 are all that is required to enable RUM on your website!

Lines 22 and 31-34 are optional if you want Session Replay instrumented.

Line 36-39 `var tracer=Provider.getTracer('appModuleLoader');` will add a Custom Event for every page change, allowing you to better track your website conversions and usage.  
