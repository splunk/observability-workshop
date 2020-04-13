### Lab Summary
* Download the workshop and configure Kubernetes ([K3s](https://k3s.io/)) environment.
* Use the SignalFx Helm chart to install the Smart Agent in K3s.
* Explore Your cluster in the Kubernetes Navigator

If you have chosen to run the workshop on a AWS/EC2 instance, please follow instructions given and go to [Step 2](https://signalfx.github.io/app-dev-workshop/module3/k3s/#2-ive-got-the-key-ive-got-the-secret).

---

### 1. Let’s bake some K8s

If you are  going to run this localy please install [Multipass](https://multipass.run/) for your OS. On a Mac you can also install via `brew` e.g. `brew cask install multipass`

 
Regardless if you are running this lab locally  or use an EC2 instance, download the App Dev Workshop Master Zip file locally or on to the EC2 instance.then proceed to unzip the file, rename it, and  change into the workshop directory

```bash
curl -LO https://github.com/signalfx/app-dev-workshop/archive/master.zip
unzip master.zip
mv app-dev-workshop-master workshop
cd workshop
```
When using an EC2 instance you can now skip to [Step 2](../module3/k3s/#2-ive-got-the-key-ive-got-the-secret "How to get an Access token")

Launch the Multipass instance which will run Kubernetes (K3s)

!!! note 
    Use `{YOUR_INITIALS}-k3s` so that the value of the instance hostname is unique e.g. `rwc-k3s`

```text
multipass launch \
--name {YOUR_INITIALS}-k3s \
--cloud-init cloud-init/k3s.yaml \
--cpus=2 --disk=10G --mem=4G
```

Once the instance has been successfully created shell into it.

```bash
multipass shell {YOUR_INITIALS}-k3s
```

![Shell](../images/module3/shell.png)

---

### 2. I’ve got the key, I’ve got the secret!

You will need to obtain your Access Token from the SignalFx UI once Kubernetes is running. You can find your Access Token by clicking on your profile icon on the top right of the SignalFx UI. Then select _**Organisation Settings → Access Tokens**_.  Expand the Default token, then click on _**Show Token**_ to expose your token. Later in the lab you can come back here and click the _**Copy**_ button which will copy it to your clipboard  so you can paste it when you need to provide an access token in the lab.
![Access Token](../images/m1-l4-access-token.png)

You will also need to obtain the name of the Realm for your SignalFx account.  Click on the profile icon again, but this time select 'My Profile'.  The Ream can be found in the middle of the page within the Organizations section.  In this example it is `us1`.
![Realm](../images/m1-l4-realm.png)

---

### 3. Take the Helm!

Create the following variables to use in the proceeding helm install command:

```
export ACCESS_TOKEN=<token from Step 2>
export REALM=<realm from Step 2>
export INITIALS=<your initials e.g. RWC>
export VERSION=<Smart Agent version e.g. 5.1.1>
```

!!! note
    The latest version of the Smart Agent can be found on [GitHub](https://github.com/signalfx/signalfx-agent/releases)

Install the agent using the SignalFx Helm chart. Firstly, add the SignalFx Helm chart repository to Helm.

```
helm repo add signalfx https://dl.signalfx.com/helm-repo
```

Ensure the latest state of the SignalFx Helm repository

```
helm repo update
```

Install the Smart Agent Helmchart with the following commands:

```
sed -i -e 's/\[INITIALS\]/'"$INITIALS"'/' workshop/k3s/values.yaml
helm install \
--set signalFxAccessToken=$ACCESS_TOKEN \
--set clusterName=$INITIALS-SFX-WORKSHOP \
--set kubeletAPI.url=https://localhost:10250  \
--set signalFxRealm=$REALM  \
--set agentVersion=$VERSION \
--set traceEndpointUrl=https://ingest.$REALM.signalfx.com/v2/trace \
--set gatherDockerMetrics=false \
signalfx-agent signalfx/signalfx-agent \
-f workshop/k3s/values.yaml
```

You can monitor the progress of the deployment by running `kubectl get pods` which should typically report a new pod is up and running after about 30 seconds. Ensure the status is reported as Running before continuing.

=== "Input"
    ``` bash
    kubectl get pods
    ```

=== "Output"
    ```
    NAME                   READY   STATUS    RESTARTS   AGE
    signalfx-agent-66tvr   1/1     Running   0          7s
    ```

Ensure there are no errors by tailing the logs from the Smart Agent Pod. Output should look similar to the log output shown below. Use the label set by the `helm` install to tail logs (You will need to press Ctrl-C to exit). Or use the installed `k9s` terminal UI for bonus points!

=== "Input"
    ```bash
    kubectl logs -l app=signalfx-agent -f
    ```
=== "Output"
    ```text
    time="2020-03-15T11:30:28Z" level=info msg="Starting up agent version 5.0.0"
    time="2020-03-15T11:30:28Z" level=info msg="Watching for config file changes"
    time="2020-03-15T11:30:28Z" level=info msg="New config loaded"
    time="2020-03-15T11:30:28Z" level=info msg="Using log level info"
    time="2020-03-15T11:30:28Z" level=info msg="Fetching host id dimensions"
    time="2020-03-15T11:30:28Z" level=info msg="Trying to get fully qualified hostname"
    time="2020-03-15T11:30:28Z" level=info msg="Using hostname PH-k3s"
    time="2020-03-15T11:30:29Z" level=info msg="Using host id dimensions map[host:PH-k3s    kubernetes_node_uid:05ba9d7b-89d4-4c70-a3e9-4dc72923423a]"
    time="2020-03-15T11:30:29Z" level=info msg="Sending datapoints to https://ingest.us1.signalfx.com/v2/datapoint"
    time="2020-03-15T11:30:29Z" level=info msg="Sending events to https://ingest.us1.signalfx.com/v2/event"
    time="2020-03-15T11:30:29Z" level=info msg="Creating new monitor" discoveryRule= monitorID=10 monitorType=kubelet-stats
    time="2020-03-15T11:30:29Z" level=info msg="Creating new monitor" discoveryRule= monitorID=11 monitorType=kubernetes-cluster
    time="2020-03-15T11:30:29Z" level=info msg="Done configuring agent"
    ...
    time="2020-03-15T11:30:29Z" level=info msg="Serving internal metrics at localhost:8095"
        I0315 11:30:29.922577       1 leaderelection.go:242] attempting to acquire leader lease  default/signalfx-agent-leader...
        I0315 11:30:29.950448       1 leaderelection.go:252] successfully acquired lease default/signalfx-agent-leader
    time="2020-03-15T11:30:29Z" level=info msg="K8s leader is now node ph-k3s"
    time="2020-03-15T11:30:29Z" level=info msg="Starting K8s API resource sync"
    ...
    ```

---

### 4. Check all is well in the SignalFx UI!

In the SignalFx UI, goto _**INFRASTRUCTURE → Kubernetes Navigator → Cluster Map**_ and open the Kubernetes Navigator Cluster Map to ensure metrics are being sent.

![Selecting the Kubernetes Navigator Map](../images/module3/clustermap-nav.png)

---

Validate that your cluster is discovered and shown (In a workshop you can see many more clusters) by finding your cluster by searching for `{YOUR_INITIALS}-SFX-WORKSHOP`:

![Find Your Cluster](../images/module3/find-cluster.png)

If there are many clusters you can use the dashboard filter to narrow down to your Kubernetes cluster e.g. `kubernetes_cluster: {YOUR_INITIALS}-SFX-WORKSHOP` or do this by clicking on the blue cross ![blue cross](../images/M1-l4-blue-cross.jpg) after selecting your cluster with your mouse.

![K8S Clusters Filter](../images/M1-l4-Selecting-K3-cluster.jpg)

To examine the health of your cluster, open the side bar by clicking on the side bar button to open the Metrics side bar. Once it is open, you can use the slider on the side to explore the various charts relevant to your cluster/node: Cpu%, Mem%, Network in & out. Events and Container list.

![Sidebar metrics](../images/M1-l4-explore-metrics.jpg)


Take some time to explore the Kubernetes Navigator UI.

---

Use the **Next** link in the footer below to continue the workshop