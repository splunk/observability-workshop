---
title: Deploying the Online Boutique in K3s
weight: 2
---

* Deploy the Online Boutique application into Kubernetes (K3s)
* Verify the application is running
* Generate some artificial traffic using Locust
* See APM metrics in the UI

---

## 1. Obtain Access Token

As this Deployment we are about to do is also used as part of the RUM workshop section, you will need to obtain your RUM Access Token from the Splunk UI. You can find the workshop Access Token by clicking **>>** bottom left and then selecting **Settings → Access Tokens**.

Expand the RUM workshop token that your host has instructed you to use e.g. **O11y-Workshop-RUM-TOKEN**, then click on **Show Token** to expose your token. Click the {{% labelbutton color="ui-button-grey" %}}Copy{{% /labelbutton %}} button to copy to clipboard. Please do not use the **Default** token!

![Access Token](../../../../imt/images/access-token.png)

{{% alert title="Please do not attempt to create your own token" color="warning" %}}
We have created a RUM Token specifically for this workshop with the appropriate settings for the exercises you will be performing
{{% /alert %}}

## 2. Deploy Online Boutique

Create the `RUM_TOKEN` environment variable to use in the proceeding shell script to personalize your deployment.

{{< tabpane >}}
{{< tab header="Export Variables" lang="bash" >}}
export RUM_TOKEN=<replace_with_O11y-Workshop-RUM-TOKEN>
{{< /tab >}}
{{< /tabpane >}}

To deploy the Online Boutique application into K3s, run the apm config script, then apply the deployment:

{{< tabpane >}}
{{< tab header="Deploy Online Boutique" lang="bash" >}}
cd ~/workshop/apm
./apm-config
kubectl apply -f deploymentRUM.yaml
{{< /tab >}}
{{< tab header="Deployment Output" lang= "bash" >}}
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
{{< /tab >}}
{{< /tabpane >}}

To ensure the Online Boutique application is running:

{{< tabpane >}}
{{< tab header="Get Pods" lang="bash" >}}
kubectl get pods
{{< /tab >}}
{{< tab header="Get Pods Output" lang= "bash" >}}
NAME                                                          READY   STATUS    RESTARTS   AGE
splunk-otel-collector-k8s-cluster-receiver-56585564cc-xclzj   1/1     Running   0          84s
splunk-otel-collector-agent-hkshj                             1/1     Running   0          84s
svclb-frontend-external-c74n6                                 1/1     Running   0          53s
currencyservice-747b74467f-xxrl9                              1/1     Running   0          52s
redis-cart-74594bd569-2jb6c                                   1/1     Running   0          54s
adservice-6fb948b8c6-2xlrc                                    0/1     Running   0          53s
recommendationservice-b5df8776c-sbt4h                         1/1     Running   0          53s
shippingservice-6d6f7b8d87-5lg9g                              1/1     Running   0          53s
svclb-loadgenerator-jxwct                                     1/1     Running   0          53s
emailservice-9dd74d87c-wjdqr                                  1/1     Running   0          53s
checkoutservice-8bcd56b46-bfj7d                               1/1     Running   0          54s
productcatalogservice-796cdcc5f5-vhspz                        1/1     Running   0          53s
paymentservice-6c875bf647-dklzb                               1/1     Running   0          53s
frontend-b8f747b87-4tkxn                                      1/1     Running   0          53s
cartservice-59d5979db7-bqf64                                  1/1     Running   1          53s
loadgenerator-57c8b84966-7nr4f                                1/1     Running   3          53s
{{< /tab >}}
{{< /tabpane >}}

{{% alert title="Info" color="info" %}}
Usually it should only take around 1min 30secs for the pods to transition into a Running state.
{{% /alert %}}

---

## 3. Validate in the UI

In the Splunk UI click on Infrastructure ![infrastructure button](../../../images/infrastructure.png) this will bring you to the Infrastructure Overview dashboard, then click on **Kubernetes**.

Use the **Cluster** dropdown so select your cluster, you should see the new pods started and containers deployed.

When you click on your cluster in the Splunk UI you should have a view that looks like below:

![back to Cluster](../../../images/online-boutique-k8s.png)

If you select the **WORKLOADS** tab again you should now see that there are a number of Deployments and ReplicaSets:

![HOTROD loaded](../../../images/online-boutique-workload.png)

---

## 4. View Online Boutique

The Online Boutique is viewable on port 81 of the EC2 instance's IP address. The IP address is the one you used to SSH into the instance at the beginning of the workshop.

Open your web browser and go to `http://{==EC2-IP==}:81/` where you will then be able to see the Online Boutique running.

![Online Boutique](../../../images/online-boutique.png)
