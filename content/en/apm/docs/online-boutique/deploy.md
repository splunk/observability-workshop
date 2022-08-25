---
title: Deploying the Online Boutique in K3s
weight: 2
---

* Deploy the Online Boutique application into Kubernetes (K3s)
* Verify the application is running
* Generate some artificial traffic using Locust
* See APM metrics in the UI

---

## 1. Check your EC2 server

This assumes you are running this after you have run the IMT workshop, and still have access to your ec2 instance.
If this is the case, continue with paragraph 3. *Deploy Online Boutique*,
otherwise if you have received a fresh instance,  please run the first two (2) sections of [Deploying the OpenTelemetry Collector in Kubernetes](../../../imt/docs/gdi/k3s.md) to get the system ready for the APM workshop, then continue with the next section.

## 2. Deploy Online Boutique

To deploy the Online Boutique application into K3s, run the apm-config script, then apply the deployment:

{{< tabpane >}}
{{< tab header="Deploy Online Boutique" lang="bash" >}}
cd ~/workshop/apm
./apm-config.sh
kubectl apply -f deployment.yaml
{{< /tab >}}
{{< tab header="Deployment Output" lang= "bash" >}}
APM Only Deployment
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

{{% alert title="In case of a message about a VARIABLE being unset" color="warning" %}}
Please undeploy the APM environment first by running **kubectl delete -f deployment.yaml**</br>
Then export the variable as described in the guide/message, followed by rerunning the deployment script above.
{{% /alert %}}

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

## 4. Validate in the UI

In the Splunk UI click on Infrastructure ![infrastructure button](../../../images/infrastructure.png) this will bring you to the Infrastructure Overview dashboard, then click on **Kubernetes**.

Use the **Cluster** dropdown so select your cluster, you should see the new pods started and containers deployed.

When you click on your cluster in the Splunk UI you should have a view that looks like below:

![back to Cluster](../../../images/online-boutique-k8s.png)

If you select the **WORKLOADS** tab again you should now see that there are a number of Deployments and ReplicaSets:

![HOTROD loaded](../../../images/online-boutique-workload.png)

---

## 5. View Online Boutique

The Online Boutique is viewable on port 81 of the EC2 instance's IP address. The IP address is the one you used to SSH into the instance at the beginning of the workshop.

Open your web browser and go to `http://{==EC2-IP==}:81/` where you will then be able to see the Online Boutique running.

![Online Boutique](../../../images/online-boutique.png)
