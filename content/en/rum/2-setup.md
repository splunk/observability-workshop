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

Open your web browser and go to the Online Boutique.  (The one you previously used, or the one provided by the Workshop instructor). You will see the non RUM Online Boutique running.

![Online Boutique](../images/online-boutique.png)

In Chrome & Firefox or Microsoft Edge you can right click on the Online-Boutique site, you will have an option to **"View Page Source"**

![Chrome-see-source](../images/Chrome-1.png)

Selecting it will show you the HTML page source code in a separate Tab. The changes for RUM will be placed in the HEAD section of your Web page, Below are the original lines as you should have it in your local Base version. There is no reference to the Splunk or OpenTelemetry Beacon (the function that is used to send RUM Metrics and Traces).

![Chrome-see-html](../images/Chrome-html.png)

## 2. Obtain RUM Access Token

As this Deployment we are about to do is also used as part of the RUM workshop section, you will need to obtain your RUM Access Token from the Splunk UI. You can find the workshop Access Token by clicking **>>** bottom left or the ![settings](../images/setting.png?classes=inline&height=25px) menu option and then selecting **Settings → Access Tokens**.

Expand the RUM workshop token that your host has instructed you to use e.g. **O11y-Workshop-RUM-TOKEN**, then click on **Show Token** to expose your token. Click the {{% button style="grey" %}}Copy{{% /button %}} button to copy to clipboard. Please do not use the **Default** token! Make sure the token has RUM as its Authorization Scope.

![Access Token](../images/RUM-Access-Token.png)

{{% notice title="Please do not attempt to create your own token" style="note" %}}
We have created a RUM Token specifically for this workshop with the appropriate settings for the exercises you will be performing
{{% /notice %}}

Create the `RUM_TOKEN` environment variable to use in the proceeding shell script to personalize your deployment.

{{% tab title="Export Variables" %}}

```bash
export RUM_TOKEN=<replace_with_O11y-Workshop-RUM-TOKEN>
```

{{% /tab %}}

## 3. Removing existing deployment

If you have deployed the Online Boutique as part of the APM session, you will need to remove the existing deployment before you can deploy the RUM enabled version.

{{% tab title="Remove existing deployment" %}}

```bash
cd ~/workshop/apm
kubectl delete -f deployment.yaml
```

{{% /tab %}}

## 4. Deploy RUM enabled Online Boutique

To deploy the Online Boutique application into K3s, run the apm config script, then apply the deployment:

{{< tabs >}}
{{% tab title="Deploy RUM enabled Online Boutique" %}}

```bash
cd ~/workshop/apm
./apm-config.sh -r
kubectl apply -f deployment.yaml
```

{{% /tab %}}
{{% tab title="Deployment Output" %}}

``` text
deployment.apps/checkoutservice created
service/checkoutservice created
deployment.apps/redis-cart created
service/redis-cart created
deployment.apps/productcatalogservice created
service/productcatalogservice created
deployment.apps/loadgenerator created
service/loadgenerator created
deployment.apps/frontend created
service/frontend created
service/frontend-external created
deployment.apps/paymentservice created
service/paymentservice created
deployment.apps/emailservice created
service/emailservice created
deployment.apps/adservice created
service/adservice created
deployment.apps/cartservice created
service/cartservice created
deployment.apps/recommendationservice created
service/recommendationservice created
deployment.apps/shippingservice created
service/shippingservice created
deployment.apps/currencyservice created
service/currencyservice created
```

{{% /tab %}}
{{< /tabs >}}

## 6.  Review the changes to Online Boutique

The changes needed for RUM are placed in the `<head>` section of the hosts Web page. Below is the updated `<head>` section with the changes required to enable RUM:

![Online Boutique](../images/ViewRUM-HEAD-html.png)

The first three lines (marked in red) have been added to the `<head>` section of the host Web page to enable RUM Tracing, the last three (marked in blue) are optional and used to enable Custom RUM events.

``` html
<script src="https://cdn.signalfx.com/o11y-gdi-rum/latest/splunk-otel-web.js" type="text/javascript"></script>
<script>window.SplunkRum && window.SplunkRum.init({beaconUrl: "https://rum-ingest.eu0.signalfx.com/v1/rum",
        rumAuth: "<redacted>", app: "ksnq-rum-app", environment: "ksnq-rum-env"});</script>
    <script>
    const Provider = SplunkRum.provider; 
    var tracer=Provider.getTracer('appModuleLoader');
</script>
```

* The first part is to indicate where to download the Splunk Open Telemetry Javascript file from: `https://cdn.signalfx.com/o11y-gdi-rum/latest/splunk-otel-web.js` (this can also be hosted locally if so required).
* The second line defines the location where to send the traces to in the beacon url: `{beaconUrl: "https://rum-ingest.eu0.signalfx.com/v1/rum"`
* The Access Token:  `rumAuth: "<redacted>"`.
* Identification tags `app` and `environment` to indentify in the SPLUNK RUM UI:  `app: "ksnq-rum-app", environment: "ksnq-rum-env"}`

{{% notice title="Info" style="info" %}}
In this example the app name is **ksnq-rum-app**, this will be different in the Workshop. Check with your host what the app name and environment to use in the RUM session will be and make a note of it!
{{% /notice %}}

The above two lines are all that is required to enable RUM on your website!

The (blue) optional section that uses `var tracer=Provider.getTracer('appModuleLoader');` will add a custom event for every page change allowing you to better track your website conversions and usage.  
