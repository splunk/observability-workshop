---
title: 2. Showcase of RUM with the Online Boutique
linkTitle: 2. Showcase
weight: 2
---

* Find the Web address of your workshop hosts Online Boutique
* Generate traffic by shopping for bargains on your workshop hosted Online Boutique web shop.

---

## 1. URL of RUM enabled Online Boutique

As discussed in the previous section we are going to use an Online Boutique running on a RUM host.
If you're participating in a RUM only workshop, after you have received the RUM instance URL, you can continue to Section 4: [Using the Online Boutique to generate load on your system](./#4-using-the-online-boutique-to-generate-load-on-your-system) as the system your going to use is already prepared.

## 2. Obtain RUM Access Token

As part of the overall workshop you have installed services for the APM Workshop. We are now going to add the RUM capability to the deployment as well.

The first thing we need to do is obtain a RUM_ACCESS_TOKEN with a RUM Authorization scope.  You can find the workshop RUM Access Token by clicking on the **Settings Cog** menu button and then selecting **Access Tokens**.

Expand the RUM workshop token that your host has instructed you to use e.g. **O11y-Workshop-RUM-TOKEN**, then click on **Show Token** to expose your token. Click the {{% button style="grey" %}}Copy{{% /button %}} button to copy to clipboard. Please do not use the **Default** token! Make sure the token has RUM as its Authorization Scope.

![Access Token](../images/RUM-Access-Token.png)

{{% notice title="Please do not attempt to create your own token" style="warning" %}}
We have created a RUM Token specifically for this workshop with the appropriate settings for the exercises you will be performing
{{% /notice %}}

Create the `RUM_TOKEN` environment variable to use in the proceeding shell script to personalize your deployment.

{{< tabs >}}
{{% tab name="Export Variables" %}}

``` bash
export RUM_TOKEN=<replace_with_O11y-Workshop-RUM-TOKEN>
```

{{% /tab %}}
{{< /tabs >}}

## 3. Deploy RUM based Online Boutique

To deploy the Online Boutique application into your EC2 instance  kubernetes (K3s) installation delete the  original deployment, then run the apm config script for RUM, then apply the RUM deployment:

{{< tabs >}}
{{% tab name="Deploy Online Boutique with RUM" %}}

``` bash
cd ~/workshop/apm
kubectl delete -f deployment.yaml
./apm-config.sh -r
kubectl apply -f deployment.yaml
```

{{% /tab %}}
{{% tab name="Partial Deployment Output" %}}

``` text
......
Adding RUM_TOKEN to deployment
deployment.apps/recommendationservice created
service/recommendationservice created
deployment.apps/productcatalogservice created
service/productcatalogservice created
deployment.apps/cartservice created
service/cartservice created
deployment.apps/adservice created
service/adservice created
deployment.apps/paymentservice created
service/paymentservice created
deployment.apps/loadgenerator created
service/loadgenerator created
deployment.apps/shippingservice created
service/shippingservice created
deployment.apps/currencyservice created
service/currencyservice created
deployment.apps/redis-cart created
service/redis-cart created
deployment.apps/checkoutservice created
service/checkoutservice created
deployment.apps/frontend created
service/frontend created
service/frontend-external created
deployment.apps/emailservice created
service/emailservice created
deployment.apps/rum-loadgen-deployment created
```

{{% /tab %}}
{{< /tabs >}}

{{% notice title="In case of a message about a VARIABLE being unset" color="warning" %}}
Please undeploy the APM environment by running **kubectl delete -f deployment.yaml**

Before exporting the variable as described in the guide and rerunning the deployment script above.
{{% /notice %}}

## 4. Using the Online Boutique to generate load on your system

We are all connected to an Online Boutique, together with some synthetic users who are also shopping for this session. This will create more traffic from multiple locations, making the data more realistic.

You should have received the correct URL from your workshop host at this point.
Open a new web browser and go to `http://{==RUM-HOST-EC2-IP==}:81/` where you will then be able to see the RUM enabled Online Boutique running.

![Online Boutique](../images/online-boutique.png)

## 5. Generate traffic

The goal of this exercise is for you to browse the RUM enabled Online Boutique and buy different products and different quantities.
For extra credit, you may even use the url from different browsers or from your smartphone.

This will create  multiple sessions to investigate. Take your time to examine and buy the various products and put them in your cart:

![Cart Online Boutique](../images/cart.png)

Doesn't that HOME BARISTA KIT look tempting?...   Your time to start shopping now!
