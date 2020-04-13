## Enabling µAPM on EKS
_An organisation needs to be pre-provisioned as a µAPM entitlement is required for the purposes of this module. Please contact someone from SignalFx to get a trial instance with µAPM enabled if you don’t have one already._

_To check if you have an organisation with µAPM enabled, just login to SignalFx and check that you have the µAPM tab on the top navbar next to Dashboards._

---

### 1. Set environment variables

Create the following variables to use in the proceeding helm install command:

```
export ACCESS_TOKEN=<token from Step 2>
export EKS_CLUSTER_NAME=<e.g. EKS-APP-DEV>
export REALM=<realm from Step 2>
export INITIALS=<your initials e.g. RWC>
export VERSION=<Smart Agent version e.g. 5.1.1>
export AWS_REGION=<e.g. us-east-1>
```

Check SignalFx Smart Agent release version on [Github](https://github.com/signalfx/signalfx-agent/releases) i.e. 5.1.1

### 2. Configure AWS CLI for your account

`aws configure`

And enter the variables from your AWS account as shown below with sample values:

```
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: us-west-2
Default output format [None]: json
```
    
---

### 3. Create a cluster running Amazon Elastic Kubernetes (EKS) Service
```
eksctl create cluster \
--name $EKS_CLUSTER_NAME \
--region $AWS_REGION \
--node-type t3.medium \
--nodes-min 3 \
--nodes-max 7 \
--version=1.15
```

This may take some time (10-15 minutes). Once complete update `kubeconfig` to allow `kubectl` access to the cluster:

```
sudo eksctl utils write-kubeconfig -n $EKS_CLUSTER_NAME
```

Ensure you see your cluster active in AWS EKS console before proceeding.

---

### 4. Deploy SignalFx SmartAgent to your EKS Cluster

```bash
helm repo add signalfx https://dl.signalfx.com/helm-repo
```

```text
helm repo update
```

```
sed -i -e 's/\[INITIALS\]/'"$INITIALS"'/' workshop/k3s/values.yaml
helm install \
--set signalFxAccessToken=$ACCESS_TOKEN \
--set clusterName=$EKS_CLUSTER_NAME \
--set signalFxRealm=$REAM \
--set agentVersion=$VERSION \
--set kubeletAPI.url=https://localhost:10250 \
--set traceEndpointUrl=https://ingest.$REALM.signalfx.com/v2/trace \
signalfx-agent signalfx/signalfx-agent \
-f workshop/k3s/values.yaml
```

Validate cluster looks healthy in SignalFx Kubernetes Navigator dashboard

---

### 5. Deploy Hotrod Application to EKS

```
kubectl apply -f ~/workshop/apm/hotrod/eks/deployment.yaml
```

To ensure the Hotrod application is running see examples below:

=== "Input"
    ```bash
    kubectl get pods
    ```

=== "Output"
    ```text
    NAME                      READY   STATUS    RESTARTS   AGE
    hotrod-7564774bf5-vjpfw   1/1     Running   0          47h
    signalfx-agent-jmq4f      1/1     Running   0          138m
    signalfx-agent-nk8p9      1/1     Running   0          138m
    signalfx-agent-q5tzh      1/1     Running   0          138m
    ```

You then need find the IP address assigned to the Hotrod service:

=== "Input"
    ```bash
    kubectl get svc
    ```

=== "Output"
    ```text
    NAME         TYPE           CLUSTER-IP       EXTERNAL-IP                                                               PORT(S)          AGE
    hotrod       LoadBalancer   10.100.188.249   af26ce80ef2e14c9292ae5b4bc0d2dd0-1826890352.us-east-2.elb.amazonaws.com   8080:32521/TCP   47h
    kubernetes   ClusterIP      10.100.0.1       <none>                                                                    443/TCP          3d1h
    ```

Create an environment variable for the IP address and port that the Hotrod application is exposed on:

```
HOTROD_ENDPOINT=$(kubectl get svc hotrod -n default -o jsonpath='{.spec.clusterIP}:{.spec.ports[0].port}')
```

You can view / exercise Hotrod yourself in a browser by opening the `EXTERNAL-IP:PORT` as shown above i.e.

https://af26ce80ef2e14c9292ae5b4bc0d2dd0-1826890352.us-east-2.elb.amazonaws.com:8080

---

### 6. Generate some traffic to the application using Apache Benchmark
```bash
ab -n100 -c10 "http://$HOTROD_ENDPOINT/dispatch?customer=392&nonse=0.17041229755366172"
```

Create some errors with an invalid customer number

```bash
ab -n100 -c10 "http://$HOTROD_ENDPOINT/dispatch?customer=391&nonse=0.17041229755366172"
```

You should now be able to exercise SignalFx APM dashboards.

---

### 5. Deleting resources

To delete entire EKS cluster:

```
eksctl delete cluster YOURCLUSTERNAMEHERE`
```

Or to delete individual components:

```
kubectl delete deploy/hotrod svc/hotrod
helm delete signalfx-agent
```

---

To switch back to using K3s cluster
```
sudo kubectl config use-context default
```

### Appendix: Tips, Troubleshooting, and References

Set AWS EKS context to your cluster (i.e. when switching machines)

`aws eks --region YOURAWSREGION update-kubeconfig --name YOURCLUSTERNAME`

Ensure kubectl context is correct

`kubectl config get-contexts`              

Will display list of contexts 

`kubectl config use-context YOURCLUSTERNAME`    

Will set the default context to cluster with ARN: YOURCLUSTERNAME

Set up kubectl for EKS

`aws eks --region YOURREGION update-kubeconfig --name YOURCLUSTERNAME`
`kubectl get pods --kubeconfig ./.kube/config`
`kubectl get svc`

Check SignalFx Agent Values

`helm get values signalfx-agent -a`

`kubectl` reference

[https://kubernetes.io/docs/reference/kubectl/cheatsheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
