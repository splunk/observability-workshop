## Before We Start - SignalFx Org Access
_An organisation needs to be pre-provisioned as a µAPM entitlement is required for the purposes of this module. Please contact someone from SignalFx to get a trial instance with µAPM enabled if you don’t have one already._

_To check if you have an organisation with µAPM enabled, just login to SignalFx and check that you have the µAPM tab on the top navbar next to Dashboards._

---

## Step 1: Create an instance running Kubernetes
1. This is already documented in [1.4 Running the SmartAgent in Kubernetes using K3s](https://github.com/signalfx/app-dev-workshop/wiki/1.4-Running-the-SmartAgent-in-Kubernetes-using-K3s). 

---

## Step 2: Deploy the Hotrod application into K3s
1. To deploy the Hotrod application into K3s apply the deployment
   
   **Input**
   ```
   kubectl apply -f workshop/apm/hotrod/k8s/deployment.yaml 
   ```

   **Output**
   ```
   deployment.apps/hotrod created
   service/hotrod created
   ```

2. Make sure the application is now running

   **Input**
   ```
   kubectl get pods
   ```

   **Output**
   ```
   NAME                      READY   STATUS    RESTARTS   AGE
   signalfx-agent-mmzxk      1/1     Running   0          110s
   hotrod-7cc9fc85b7-n765r   1/1     Running   0          41s
   ```

3. To find the IP address assigned to the Hotrod service

   **Input**
   ```
   kubectl get svc
   ```

   **Output**
   ```
   NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
   kubernetes   ClusterIP   10.43.0.1       <none>        443/TCP    25m
   hotrod       ClusterIP   10.43.124.159   <none>        8080/TCP   94s
   ```

   Make note of the ClusterIP address associated with Hotrod

4. Generate some traffic to the application using Apache Benchmark

   ```
   ab -n10 -c10 "http://[CLUSTERIP]:8080/dispatch?customer=392&nonse=0.17041229755366172"
   ```

   Create some errors with an invalid customer number

   ```
   ab -n10 -c10 "http://[CLUSTERIP]:8080/dispatch?customer=391&nonse=0.17041229755366172"
   ```
---


