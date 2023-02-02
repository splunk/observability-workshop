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

This assumes you are running this after you have run the IM workshop, and still have access to your ec2 instance.
If this is the case, continue with paragraph 3. *Deploy Online Boutique*,
otherwise if you have received a fresh instance, please run the first two (2) sections of [Deploying the OpenTelemetry Collector in Kubernetes](../../../../imt/docs/gdi/k3s) to get the system ready for the APM workshop, then continue with the next section.

## 2. Deploy Online Boutique

To deploy the Online Boutique application into K3s, run the apm-config script, then apply the deployment:

{{< tabpane >}}
{{< tab header="Deploy Online Boutique" lang="sh" >}}
cd ~/workshop/apm
./apm-config.sh
kubectl apply -f deployment.yaml
{{< /tab >}}
{{< tab header="Deployment Output" lang= "text" >}}
APM Only Deployment
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
{{< /tab >}}
{{< /tabpane >}}

{{% alert title="In case of a message about a VARIABLE being unset" color="warning" %}}
Please undeploy the APM environment first by running **kubectl delete -f deployment.yaml**</br>
Then export the variable as described in the guide/message, followed by rerunning the deployment script above.
{{% /alert %}}

To ensure the Online Boutique application is running:

{{< tabpane >}}
{{< tab header="Get Pods" lang="sh" >}}
kubectl get pods
{{< /tab >}}
{{< tab header="Get Pods Output" lang= "text" >}}
NAME                                                       READY  STATUS  RESTARTS      AGE
splunk-otel-collector-k8s-cluster-receiver-849cf595bf-l7mnq 1/1   Running   0           31m
splunk-otel-collector-agent-pxrgp                           2/2   Running   0           31m
productcatalogservice-8464cd56d-n8f89                       1/1   Running   0            1m
redis-cart-bcf44df97-djv6z                                  1/1   Running   0            1m
checkoutservice-8558fd7b95-b9pn8                            1/1   Running   0            1m
shippingservice-7cc4bdd6f4-xsvnx                            1/1   Running   0            1m
recommendationservice-647d57fd44-l7tkq                      1/1   Running   0            1m
frontend-66c5d589d-55vzb                                    1/1   Running   0            1m
emailservice-6ff5bbd67d-pdcm2                               1/1   Running   0            1m
paymentservice-6866558995-8xmf2                             1/1   Running   0            1m
currencyservice-8668d75d6f-mr68h                            1/1   Running   0            1m
rum-loadgen-deployment-58ccf7bd8f-cr4pr                     1/1   Running   0            1m
rum-loadgen-deployment-58ccf7bd8f-qjr4b                     1/1   Running   0            1m
rum-loadgen-deployment-58ccf7bd8f-fvb4x                     1/1   Running   0            1m
cartservice-7b58c88c45-xvxhq                                1/1   Running   0            1m
loadgenerator-6bdc7b4857-9kxjd                              1/1   Running   2 (49s ago)  1m
adservice-7b68d5b969-89ft2                                  1/1   Running   0            1m
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
