## Enabling µAPM
_An organisation needs to be pre-provisioned as a µAPM entitlement is required for the purposes of this module. Please contact someone from SignalFx to get a trial instance with µAPM enabled if you don’t have one already._

_To check if you have an organisation with µAPM enabled, just login to SignalFx and check that you have the µAPM tab on the top navbar next to Dashboards._

---

### 1. Create an instance running Kubernetes
This is already documented in [Deploying the Smart Agent in Kubernetes (K3s)](https://signalfx.github.io/app-dev-workshop/module1/k3s/). 

---

### 2. Deploy the Hotrod application into K3s
To deploy the Hotrod application into K3s apply the deployment
  
```bash tab="Input"
kubectl apply -f workshop/apm/hotrod/k8s/deployment.yaml 
```


```text tab="Output"
deployment.apps/hotrod created
service/hotrod created
```

To ensure the Hotrod application is running:

```bash tab="Input"
kubectl get pods
```

```text tab="Output"
NAME                      READY   STATUS    RESTARTS   AGE
signalfx-agent-mmzxk      1/1     Running   0          110s
hotrod-7cc9fc85b7-n765r   1/1     Running   0          41s
```

You then need find the IP address assigned to the Hotrod service:

```bash tab="Input"
kubectl get svc
```

```text tab="Output"
NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
kubernetes   ClusterIP   10.43.0.1       <none>        443/TCP    25m
hotrod       ClusterIP   10.43.124.159   <none>        8080/TCP   94s
```

Make note of the `CLUSTER-IP` address associated with Hotrod

---

### 3. Generate some traffic to the application using Apache Benchmark
```bash
ab -n10 -c10 "http://{CLUSTER-IP}:8080/dispatch?customer=392&nonse=0.17041229755366172"
```

Create some errors with an invalid customer number

```bash
ab -n10 -c10 "http://{CLUSTER-IP}:8080/dispatch?customer=391&nonse=0.17041229755366172"
```
