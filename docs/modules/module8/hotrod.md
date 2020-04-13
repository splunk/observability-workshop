## Enabling µAPM on EKS
_An organisation needs to be pre-provisioned as a µAPM entitlement is required for the purposes of this module. Please contact someone from SignalFx to get a trial instance with µAPM enabled if you don’t have one already._

_To check if you have an organisation with µAPM enabled, just login to SignalFx and check that you have the µAPM tab on the top navbar next to Dashboards._

---

### 1. Requirements and Document Conventions

This workshop is tested on MacOS and Linux- it should work on Windows as well if requirements are met. Tips, references, and troubleshooting tips for these components are in the appendix.

The previous workshops should have been completed such that you have the following variables at the ready:

SignalFx token

SignalFx realm

#### **Document Conventions**

Variables that require you to alter them based on information in your environment are displayed like this: YOURVARIABLEHERE. For example if you need to set your realm to `us1` in a hostname you'd change `api.YOURREALMHERE.signalfx.com` to `api.us1.signalfx.com`

#### **Requirements**

For this workshop you must have the following installed:

**AWS CLI**

**Helm**

**eksctl**

**kubectl**

Instructions are below- note that official instructions may change over time from this document.

#### <u>1a Step 1: Install AWS CLI</u>

You should have basic familiary with AWS, your account especially access key/ID and default region, and associated administration.

 AWS CLI Official Instructions:  https://docs.aws.amazon.com/cli/ 

**Macos:** `brew install awscli`

**Linux:**

`curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" `

`unzip awscliv2.zip `

`sudo ./aws/install`

**Windows:** Download and execute: https://awscli.amazonaws.com/AWSCLIV2.msi

#### <u>**1a Step 2: Configure AWS CLI for your account:**</u>

`aws configure`

And enter the variables from your AWS account as shown below with sample values:

```
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: us-west-2
Default output format [None]: json
```

#### <u>1b Helm</u> 

Helm Official Instructions: https://helm.sh/docs/intro/install/

**Macos:** `brew install helm`

**Linux:** `sudo snap install helm --classic`

**Windows:** `choco install kubernetes-helm`

#### <u>1c eksctl</u>

eksctl Official Instructions: https://eksctl.io/introduction/installation/

**Macos:** 

`brew tap weaveworks/tap` 

`brew install weaveworks/tap/eksctl`

**Linux: **

`curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp` 

`sudo mv /tmp/eksctl /usr/local/bin`

**Windows:** `chocolatey install eksctl`

#### <u>**1d kubectl:**</u>

**Macos:** `brew install kubectl

**Linux: **

`curl -LO https://storage.googleapis.com/kubernetes-release/release/curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt/bin/linux/amd64/kubectl`

`chmod +x ./kubectl`

`sudo mv ./kubectl /usr/local/bin/kubectl`

**Windows:** `curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.18.0/bin/windows/amd64/kubectl.exe`

---

### 1. Create a cluster running Amazon Elastic Kubernetes (EKS) Service
`eksctl create cluster \`

`--name YOUREKSCLUSTERNAMEHERE \`
`--region YOURAWSREGIONHERE FOR EXAMPLE us-east-2 \`
`--node-type t3.medium \`
`--nodes-min 3 \`
`--nodes-max 7 \`
`--version=1.15`

This may take some time- ensure you see your cluster live in AWS EKS console before proceeding.

---

### 2. Deploy SignalFx SmartAgent to your EKS Cluster
Check release version: https://github.com/signalfx/signalfx-agent/releases i.e. 5.1.1

```bash tab="Input"
helm repo add signalfx https://dl.signalfx.com/helm-repo
```


```text tab="Output"
helm repo update
```

`helm install --set signalFxAccessToken=TOKENHERE --set clusterName=YOURK8SCLUSTERNAME --set signalFxRealm=YOUREALMHERE --set agentVersion=RELEASEVERSIONHERE --set kubeletAPI.url=https://localhost:10250 signalfx-agent signalfx/signalfx-agent`

Validate cluster looks healthy in SignalFx Kubernetes Navigator dashboard

------

### 3. Update SignalFX Agent Deployment in K8S for APM

This repo file: `/app-dev-workshop/apm/hotrod/eks/agent-apm.yaml` has elements needed for APM. 

Substitute `YOURAPMENVIRONMENTHERE` with your chosen application environment name i.e. `KarthikHotRodApp` and `YOUREALMHERE` with your realm as identified in your SignalFx profile i.e. `us1`.

After udpating `/app-dev-workshop/apm/hotrod/eks/agent-apm.yaml` then from the directory above the repo:

`helm upgrade --reuse-values -f ./app-dev-workshop/apm/hotrod/eks/agent-apm.yaml signalfx-agent signalfx/signalfx-agent`

------

### 4. Deploy Hotrod Application to EKS

kubectl apply -f .`/app-dev-workshop/apm/hotrod/eks/deployment.yaml` 

To ensure the Hotrod application is running see examples below:

```bash tab="Input"
kubectl get pods
```

```text tab="Output"
NAME                      READY   STATUS    RESTARTS   AGE
hotrod-7564774bf5-vjpfw   1/1     Running   0          47h
signalfx-agent-jmq4f      1/1     Running   0          138m
signalfx-agent-nk8p9      1/1     Running   0          138m
signalfx-agent-q5tzh      1/1     Running   0          138m
```

You then need find the IP address assigned to the Hotrod service:

```bash tab="Input"
kubectl get svc
```

```text tab="Output"
NAME         TYPE           CLUSTER-IP       EXTERNAL-IP                                                               PORT(S)          AGE
hotrod       LoadBalancer   10.100.188.249   af26ce80ef2e14c9292ae5b4bc0d2dd0-1826890352.us-east-2.elb.amazonaws.com   8080:32521/TCP   47h
kubernetes   ClusterIP      10.100.0.1       <none>                                                                    443/TCP          3d1h
```

Make note of the `CLUSTER-IP` address associated with Hotrod

You can view / exercise Hotrod yourself in a browser by opening the IP:PORT as shown above i.e.

https://af26ce80ef2e14c9292ae5b4bc0d2dd0-1826890352.us-east-2.elb.amazonaws.com:8080

---

### 5. Generate some traffic to the application using Apache Benchmark
```bash
ab -n100 -c10 "http://{CLUSTER-IP}:8080/dispatch?customer=392&nonse=0.17041229755366172" &
```

Create some errors with an invalid customer number

```bash
ab -n100 -c10 "http://{CLUSTER-IP}:8080/dispatch?customer=391&nonse=0.17041229755366172" &
```

You should now be able to exercise SignalFx APM dashboards.

https://af26ce80ef2e14c9292ae5b4bc0d2dd0-1826890352.us-east-2.elb.amazonaws.com:8080

---

### 5. Deleting resources

To delete entire EKS cluster: `eksctl delete cluster YOURCLUSTERNAMEHERE`

Or to delete individual components:

`kubectl delete deploy/hotrod svc/hotrod`

`helm delete signalfx-agent`

---

### Appendix: Tips, Troubleshooting, and References

###### Set AWS EKS context to your cluster (i.e. when switching machines)

`aws eks --region YOURAWSREGION update-kubeconfig --name YOURCLUSTERNAME`

###### Ensure kubectl context is correct

`kubectl config get-contexts`              

Will display list of contexts 

`kubectl config use-context YOURCLUSTERNAME`    

Will set the default context to cluster with ARN: YOURCLUSTERNAME

###### Set up kubectl for EKS

`aws eks --region YOURREGION update-kubeconfig --name YOURCLUSTERNAME`
`kubectl get pods --kubeconfig ./.kube/config`
`kubectl get svc`

###### Check SignalFx Agent Values

`helm get values signalfx-agent -a`

###### kubectl reference

https://kubernetes.io/docs/reference/kubectl/cheatsheet/
