---
title: 2. Example of RUM enablement in your Website
linkTitle:  2. Using RUM on your Website
menuPost: " <i class='fa fa-user-ninja'></i>"
weight: 2
---

* Check the original HEAD section of your Online-boutique webpage (or use the examples here) in your browser
* Find the Web address of your workshop hosts Online Boutique
* Compare the changes made to the hosts Online-Boutique and compare with the base one.

---

## 1. Browse to the Online Boutique

If you have access to an EC2 instance and have previously installed the Online Boutique as part of the APM session, you can view it on port 81 of the EC2 instance's IP address.

If you have not got access to an EC2 instance with the Online Boutique installed then your workshop instructor will provide you with the Online Boutique URL that does not have RUM installed so that you can complete the next steps.

## 2.  Inspecting the HTML source

The changes needed for RUM are placed in the `<head>` section of the hosts Web page. Below is the updated `<head>` section with the changes required to enable RUM:

![Online Boutique](../images/ViewRUM-HEAD-html.png)

The first three lines (marked in red) have been added to the `<head>` section of the host Web page to enable RUM Tracing, the last three (marked in blue) are optional and used to enable Custom RUM events.

* The first part is to indicate where to download the Splunk Open Telemetry Javascript file from: `https://cdn.signalfx.com/o11y-gdi-rum/latest/splunk-otel-web.js` (this can also be hosted locally if so required).
* The second line defines the location where to send the traces to in the beacon url: `{beaconUrl: "https://rum-ingest.eu0.signalfx.com/v1/rum"`
* The RUM Access Token:  `rumAuth: "<redacted>"`.
* Identification tags `app` and `environment` to indentify in the SPLUNK RUM UI e.g.  `app: "ksnq-store", environment: "ksnq-workshop"}`

{{% notice title="Info" style="info" %}}
In this example the app name is **ksnq-store**, this will be different in the Workshop. Check with your host what the app name and environment to use in the RUM session will be and make a note of it!
{{% /notice %}}

The above two lines are all that is required to enable RUM on your website!

The (blue) optional section that uses `var tracer=Provider.getTracer('appModuleLoader');` will add a custom event for every page change allowing you to better track your website conversions and usage.  
