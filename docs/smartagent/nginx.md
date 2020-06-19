# Deploying NGINX in K3s - Lab Summary

* Deploy a NGINX ReplicaSet into your K3s cluster and confirm the auto discovery of your NGINX deployment.
* Run a benchmark test to create metrics and confirm them streaming into SignalFX!

---

## 1. Start your NGINX

This deployment of NGINX has been configured to use Kubernetes pod annotations to tell the Smart Agent how to monitor the service.

This is achieved by defining the `port` and `monitor type` to use for monitoring the NGINX service e.g.

=== "Example Annotation"

    ```
    agent.signalfx.com/monitorType.80: "collectd/nginx"
    ```

Verify the number of pods running in the SignalFx UI by selecting the **WORKLOADS** tab. This should give you an overview of the workloads on your cluster.

![Workload Agent](../images/smartagent/k8s-workloads.png){: .zoom}

Note the single agent container running per node among the default Kubernetes pods. This single container will monitor all the pods and services being deployed on this node!

Now switch back to the default cluster node view by selecting the **MAP** tab and select your cluster again.

In the Multipass or AWS/EC2 shell session and change into the `nginx` directory:

=== "Shell Command"

    ```bash
    cd ~/workshop/k3s/nginx
    ```
  
---

## 2. Create NGINX deployment

Create the NGINX `configmap`[^1] using the `nginx.conf` file:

=== "Shell Command"

    ```text
    kubectl create configmap nginxconfig --from-file=nginx.conf
    ```

=== "Output"

    ```
    configmap/nginxconfig created
    ```

Then create the deployment:

=== "Shell Command"

    ```
    kubectl create -f nginx-deployment.yaml
    ```

=== "Output"

    ```
    deployment.apps/nginx created
    service/nginx created
    ```

Validate the deployment has been successful and that the NGINX pods are running.

If you have the SignalFx UI open you should see new Pods being started and containers being deployed.

It should only take around 20 seconds for the pods to transition into a Running state. In the SignalFx UI you will have a cluster that looks like below:

![back to Cluster](../images/smartagent/cluster.png){: .zoom}

If you select the **WORKLOADS** tab again you will now see that there is a new ReplicaSet and a deployment added for NGINX:

![NGINX loaded](../images/smartagent/k8s-workloads-nginx.png){: .zoom}

---

Let's validate this in your shell as well:

=== "Shell Command"

    ```text
    kubectl get pods
    ```

=== "Output"

    ```text
    NAME                     READY   STATUS    RESTARTS   AGE
    signalfx-agent-7mljv     1/1     Running   0          87m
    nginx-7554f6c668-pdjkp   1/1     Running   0          65s
    nginx-7554f6c668-pddfj   1/1     Running   0          65s
    nginx-7554f6c668-ggblg   1/1     Running   0          65s
    nginx-7554f6c668-mjtsh   1/1     Running   0          65s
    ```

Run `kubectl get svc` and make note of the `CLUSTER-IP` address that is allocated to the NGINX service.

=== "Shell Command"

    ```text
    kubectl get svc
    ```

=== "Output"

    ```text
    NAME         TYPE         CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
    kubernetes   ClusterIP    10.96.0.1      <none>        443/TCP        9m3s
    nginx        NodePort    {==10.110.36.62==}    <none>        80:30995/TCP   8s
    ```

---

## 3. Run Siege Benchmark

Using the NGINX `{==CLUSTER-IP==}` address reported from above, use the Siege[^2] Load Testing command to generate some traffic to light up your SignalFx NGINX dashboards. Run this a couple of times!

=== "Shell Command"

    ```text
    siege -b -r 50 -c 20 --no-parser http://{==CLUSTER-IP==}/ 1>/dev/null
    ```

=== "Output"

    ```text
    ** SIEGE 4.0.5
    ** Preparing 20 concurrent users for battle.
    The server is now under siege...

    Transactions:               1000 hits
    Availability:               100.00 %
    Elapsed time:               1.17 secs
    Data transferred:           20.05 MB
    Response time:              0.02 secs
    Transaction rate:           854.70 trans/sec
    Throughput:                 17.14 MB/sec
    Concurrency:                19.77
    Successful transactions:    1000
    Failed transactions:        0
    Longest transaction:        0.16
    Shortest transaction:       0.01
    ```

Validate you are seeing metrics in the UI by going to **Dashboards → NGINX → NGINX Servers**

![NGINX Dashboard](../images/smartagent/nginx-dashboard.png){: .zoom}

[^1]: A ConfigMap is an API object used to store non-confidential data in key-value pairs. Pods can consume ConfigMaps as environment variables, command-line arguments, or as configuration files in a volume. A ConfigMap allows you to decouple environment-specific configuration from your container images, so that your applications are easily portable.

[^2]: [What is Siege?](https://github.com/JoeDog/siege){: target=_blank}
