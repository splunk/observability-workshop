# Deploying Hot R.O.D. in K3s - Lab Summary

* Deploy application into K3s
* Verify the application is running
* Generate some artificial traffic
* Validate traces in the UI

!!! note "Ensure you have a running instance"
    The setup part is already documented in the [Preparation](../../smartagent/prep/) and [Deploy the Smart Agent in K3s](../../smartagent/k3s/) steps. If you are using an AWS/EC2 instance, make sure it is available and skip to [Step 1](../../apm/hotrod/#1-deploy-the-hot-rod-application-into-k3s), otherwise ensure your Multipass instance is available and running before continuing.

    === "Input"

        ```
        multipass list
        ```

    === "Output"

        ```
        Name                     State             IPv4             Image
        d823-k3s                 Running           192.168.64.17    Ubuntu 18.04 LTS
        ```

---

## 1. Deploy the Hot R.O.D. application into K3s

To deploy the Hot R.O.D. application into K3s apply the deployment.
  
=== "Input"

    ```bash
    cd ~/workshop
    kubectl apply -f apm/hotrod/k8s/deployment.yaml 
    ```

=== "Output"

    ```text
    deployment.apps/hotrod created
    service/hotrod created
    ```

To ensure the Hot R.O.D. application is running:

=== "Input"

    ```bash
    kubectl get pods
    ```

=== "Output"

    ```text
    NAME                      READY   STATUS    RESTARTS   AGE
    signalfx-agent-mmzxk      1/1     Running   0          110s
    hotrod-7cc9fc85b7-n765r   1/1     Running   0          41s
    ```

---

## 2. Viewing the Hot R.O.D. application in your browser

!!! note "AWC/EC2 Users"
    If you are using an AWS/EC2 instance and have access to an SSH client on your local machine, we have prepared a little helper to allow you to view the application in your browser. Run

    ```bash
    tunnelme
    ```

    and follow the instructions. This will guide you to set up a SSH tunnel from your local machine port 9123 and forward the requests to the k3s ingress load balancer on AWS.

    Then continue with the next section on how to [Generate Traffic](../../apm/hotrod/#3-generate-some-traffic-to-the-application-using-siege-benchmark).

In order to view the application in your web browser we need to find the `LoadBalancer` IP address and the port the application is listening on.

=== "Input"

    ```bash
    kubectl get svc
    ```

=== "Output"

    ```text
    NAME         TYPE           CLUSTER-IP     EXTERNAL-IP     PORT(S)          AGE
    kubernetes   ClusterIP      10.43.0.1      <none>          443/TCP          43m
    hotrod       LoadBalancer   10.43.32.97   {==192.168.64.35==}   8080:31521/TCP   40m
    ```

Make note of the `EXTERNAL-IP` (in the example above this is `192.168.64.35`). Open your web browser and type in `http://{==EXTERNAL-IP==}:8080`, you will then be able to see the application running. Click on customer name to order a car:

![Hot R.O.D. Application](../images/apm/hotrod-app.png)

---

## 3. Generate some traffic to the application using Siege Benchmark

Return to your shell and create an environment variable for the IP address and port that the Hot R.O.D. application is exposed on:

=== "Input"

    ```
    HOTROD_ENDPOINT=$(kubectl get svc hotrod -n default -o jsonpath='{.spec.clusterIP}:{.spec.ports[0].port}')
    ```

Confirm the environment variable is set

=== "Input"

    ```
    curl $HOTROD_ENDPOINT
    ```

Then run the following command(s) to create load on the service:

=== "Input"

    ```bash
    siege -r1 -c10 "http://$HOTROD_ENDPOINT/dispatch?customer=392&nonse=0.17041229755366172"
    ```

Create some errors with an invalid customer number

=== "Input"

    ```bash
    siege -r1 -c10 "http://$HOTROD_ENDPOINT/dispatch?customer=391&nonse=0.17041229755366172"
    ```

---

## 4. Verify that µAPM traces are reaching SignalFx

Open SignalFx in your browser and select the **µAPM** tab.

![select APM](../images/apm/select-apm.png){: .zoom}

Select the **Troubleshooting** tab, and select your environment and set the time to 15 minutes. This will show you the Dependency Map for the Hot R.O.D. application.

![Hot R.O.D. in APM](../images/apm/hotrod-troubleshooting.png)

If you did create some errors, they will show up as the big red dot in the Redis service.
