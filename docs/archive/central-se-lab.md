# Goals

1. Set up the workshop environment
1. Obtain Credentials
1. Deploy SignalFx Smart Agent via install script on a VM
1. Confirm the Smart Agent is working and sending data
1. Use the SignalFx Helm chart to install the Smart Agent in K3s.
1. Deploy a NGINX ReplicaSet into K3s and confirm the auto discovery of your NGINX deployment.
1. Run a benchmark test to create metrics and confirm them streaming into SignalFx!

## Step 1: Let’s bake some K8s

1. Install [Multipass][] for your OS -  On a Mac you can install via [brew][], e.g. `brew cask install multipass`

[Multipass]: https://multipass.run/
[brew]: https://brew.sh

2. Clone the workshop repo:

    ```bash
    git clone https://github.com/signalfx/app-dev-workshop
    ```

3. Change into the `app-dev-workshop-master` directory

    ```bash
    cd app-dev-workshop
    ```

4. Launch the Multipass instance which will run Kubernetes. **Note:** Use `[YOUR-INITIALS]-k3s` this is so the value of the instance hostname is unique e.g. `rwc-k3s`

    ```bash
    multipass launch --name [YOUR-INITIALS]-k3s --cloud-init cloud-init/k3s.yaml --cpus=2 --mem=4G --disk=12G
    ```

5. Once the instance has been successfully created shell into it.

    ```bash
    multipass shell [YOUR-INITIALS]-k3s
    ```

## Step 2: I’ve got the key, I’ve got the secret!

1. You will need to obtain your Access Token from the SignalFx UI once Kubernetes is running. You can find your Access Token by clicking on your profile icon on the top right of the SignalFx UI. Then select _**Organisation Settings → Access Tokens**_.  Expand the Default token, then click on _**Show Token**_ to expose your token. Later in the lab you can come back here and click the _**Copy**_ button which will copy it to your clipboard  so you can paste it when you need to provide an access token in the lab.

![Access Token](https://github.com/signalfx/app-dev-workshop/blob/master/screenshots/m1-l4-access-token.png)

2. You will also need to obtain the name of the Realm for your SignalFx account.  Click on the profile icon again, but this time select 'My Profile'.  The Ream can be found in the middle of the page within the Organizations section.  In this example it is `us1`.

![Realm](https://github.com/signalfx/app-dev-workshop/blob/master/screenshots/m1-l4-realm.png)

3. Adjust and set the following env vars in the multipass shell. We will refer to them at various stages during the workshop.

    ```bash
    ACCESS_TOKEN=<token from Step 2>
    REALM=<realm from Step 2>
    INITIALS=<your initials e.g. GH>
    VERSION=<Smart Agent version e.g. 5.0.4>
    export ACCESS_TOKEN REALM INITIALS VERSION
    alias kc=kubectl
    ```

4. Finally, change into the workshop directory:

    ```bash
    cd workshop
    ```

## Step 3: Deploy SignalFx Smart Agent via install script on a VM

SignalFx maintains a shell script to install on supported distributions:

```
curl -sSL https://dl.signalfx.com/signalfx-agent.sh > /tmp/signalfx-agent.sh
sudo sh /tmp/signalfx-agent.sh --realm $REALM $ACCESS_TOKEN
```

1. Once the installation is complete, validate the agent is running.

    ```
    signalfx-agent status
    ```

    ```
    SignalFx Agent version:           5.0.4
    Agent uptime:                     9m34s
    Observers active:                 k8s-api
    Active Monitors:                  13
    Configured Monitors:              13
    Discovered Endpoint Count:        15
    Bad Monitor Config:               None
    Global Dimensions:                {kubernetes_cluster:    AS-SFX-WORKSHOP, host: as-k3s, kubernetes_node_uid:    a58cf908-0536-478d-aa63-8ba381ef2c33}
    GlobalSpanTags:                   map[]
    Datapoints sent (last minute):    726
    Datapoints failed (last minute):  0
    Datapoints overwritten (total):   0
    Events Sent (last minute):        6
    Trace Spans Sent (last minute):   0
    Trace Spans overwritten (total):  0
    Kubernetes Leader Node:           as-k3s
    
    Additional status commands:
    
    signalfx-agent status config - show resolved config in use    by agent
    signalfx-agent status endpoints - show discovered endpoints
    signalfx-agent status monitors - show active monitors
    signalfx-agent status all - show everything
    ```

## Step 4: Confirm the Smart Agent is working and sending data

In the SignalFX UI, go to Infrastructure, Hosts and make sure you see your multipass instance in the list of hosts. You can also set a filter for just your instance.

## Step 5: Take the Helm!

0. Stop the agent running on the host

```
sudo service signalfx-agent stop
```

1. Install the agent using the SignalFx Helm chart. Firstly, add the SignalFx Helm chart repository to Helm.

    ```
    helm repo add signalfx https://dl.signalfx.com/helm-repo
    ```

2. Ensure the latest state of the repository

    ```
    helm repo update
    ```

3. Install the Smart Agent chart with the following configuration values for the chart.

    ```
    sed -i -e 's/\[INITIALS\]/'"$INITIALS"'/' k3s/values.yaml
    helm install --set signalFxAccessToken=$ACCESS_TOKEN --set clusterName=SFX-WORKSHOP --set kubernetesClusterName=$INITIALS-SFX-WORKSHOP --set kubeletAPI.url=https://localhost:10250 --set signalFxRealm=$REALM --set agentVersion=5.0.4 --set traceEndpointUrl=https://ingest.$REALM.signalfx.com/v2/trace --set gatherDockerMetrics=false signalfx-agent signalfx/signalfx-agent -f k3s/values.yaml
    ```

4. You can monitor the progress of the deployment by running `kubectl get pods` which should typically report a new pod is up and running after about 30 seconds. Ensure the status is reported as Running before continuing.

    _Input:_

    ```
    kubectl get pods
    ```

    **Output:**

    ```
    NAME                   READY   STATUS    RESTARTS   AGE
    signalfx-agent-66tvr   1/1     Running   0          7s
    ```

5. Ensure there are no errors by tailing the logs from the Smart Agent Pod. Output should look similar to the log output shown below. Use the label set by the `helm` install to tail logs (You will need to press Ctrl-C to exit). Or use the installed `k9s` terminal UI for bonus points!

    **Input:**

    ```
    kubectl logs -l app=signalfx-agent -f
    ```

    **Output:**

    ```
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
    time="2020-03-15T11:30:29Z" level=info msg="Sending trace spans to https://ingest.us1.signalfx.com/v1/trace"
    time="2020-03-15T11:30:29Z" level=info msg="Setting cluster:SFX-WORKSHOP property on host:PH-k3s dimension"
    time="2020-03-15T11:30:29Z" level=info msg="Creating new monitor" discoveryRule= monitorID=1 monitorType=cpu
    time="2020-03-15T11:30:29Z" level=info msg="Creating new monitor" discoveryRule= monitorID=2 monitorType=filesystems
    time="2020-03-15T11:30:29Z" level=info msg="Creating new monitor" discoveryRule= monitorID=3 monitorType=disk-io
    time="2020-03-15T11:30:29Z" level=info msg="Creating new monitor" discoveryRule= monitorID=4 monitorType=net-io
    time="2020-03-15T11:30:29Z" level=info msg="Creating new monitor" discoveryRule= monitorID=5 monitorType=load
    time="2020-03-15T11:30:29Z" level=info msg="Creating new monitor" discoveryRule= monitorID=6 monitorType=memory
    time="2020-03-15T11:30:29Z" level=info msg="Creating new monitor" discoveryRule= monitorID=7 monitorType=host-metadata
    time="2020-03-15T11:30:29Z" level=info msg="Creating new monitor" discoveryRule= monitorID=8 monitorType=processlist
    time="2020-03-15T11:30:29Z" level=info msg="Creating new monitor" discoveryRule= monitorID=9 monitorType=vmem
    time="2020-03-15T11:30:29Z" level=info msg="Creating new monitor" discoveryRule= monitorID=10 monitorType=kubelet-stats
    time="2020-03-15T11:30:29Z" level=info msg="Creating new monitor" discoveryRule= monitorID=11 monitorType=kubernetes-cluster
    time="2020-03-15T11:30:29Z" level=info msg="Done configuring agent"
    time="2020-03-15T11:30:29Z" level=info msg="Serving internal metrics at localhost:8095"
    I0315 11:30:29.922577       1 leaderelection.go:242] attempting to acquire leader lease  default/signalfx-agent-leader...
    I0315 11:30:29.950448       1 leaderelection.go:252] successfully acquired lease default/signalfx-agent-leader
    time="2020-03-15T11:30:29Z" level=info msg="K8s leader is now node ph-k3s"
    time="2020-03-15T11:30:29Z" level=info msg="Starting K8s API resource sync"
    ```

6. In the SignalFx UI, goto _**INFRASTRUCTURE → Kubernetes Navigator → Cluster Map**_ and open the Kubernetes Navigator Cluster Map to ensure metrics are being sent. 

![Selecting the Kubernetes Navigator Map](https://github.com/signalfx/app-dev-workshop/blob/master/screenshots/M1-l4-select-kubenetes-map.jpg)

Validate that your cluster is discovered and shown (In a workshop you can see many more clusters) by searching for `[YOUR-INITIALS]-SFX-WORKSHOP`:

![Find Your Cluster](https://github.com/signalfx/app-dev-workshop/blob/master/screenshots/M1-l4-All-clusters.jpg)

7. If there are many clusters you can use the dashboard filter to narrow down to your K8s cluster e.g. `kubernetes_cluster: [YOUR-INITIALS]-SFX-WORKSHOP` or do this by clicking on the blue cross ![blue cross](https://github.com/signalfx/app-dev-workshop/blob/master/screenshots/M1-l4-blue-cross.jpg) after selecting your cluster with your mouse. 
![K8S Clusters Filter](https://github.com/signalfx/app-dev-workshop/blob/master/screenshots/M1-l4-Selecting-K3-cluster.jpg)

8. To examine the health of your cluster, open the side bar by clicking on the ![side bar button](https://github.com/signalfx/app-dev-workshop/blob/master/screenshots/M1-l4-sidebar-button.jpg) button to open the Metrics side bar. Once it is open, you can use the slider on the side to explore the various charts relevant to your cluster/node: Cpu%, Mem%, Network in & out. Events and Container list.

![side bar metrics](https://github.com/signalfx/app-dev-workshop/blob/master/screenshots/M1-l4-explore-metrics.jpg)

---

## Step 6: Start your NGINX!

1. Still within the k3s shell session, change into the `nginx` directory

    ```bash
    cd ~/workshop/k3s/nginx
    ```

2. Create the NGINX configmap using the `nginx.conf` file

    ```
    kubectl create configmap nginxconfig --from-file=nginx.conf
    ```

3. Create the NGINX deployment

    ```
    kubectl create -f nginx-deployment.yaml
    ```

4. Validate the deployment has been successful and that the NGINX pods are running, it should only take around 20 seconds for the pods to transition into a Running state. More bonus points for using the `k9s` terminal UI!

    **Input:**

    ```
    kubectl get pods
    ```

    **Output:**

    ```
    NAME                               READY   STATUS    RESTARTS   AGE
    signalfx-agent-n7nz2               1/1     Running   0          11m
    nginx-deployment-f96cf6966-jhmjp   1/1     Running   0          21s
    nginx-deployment-f96cf6966-459vf   1/1     Running   0          21s
    nginx-deployment-f96cf6966-vrnfc   1/1     Running   0          21s
    nginx-deployment-f96cf6966-7z4tm   1/1     Running   0          21s
    ```

5. Next we need to expose port 80 (HTTP)

    **Input:**

    ```
    kubectl create service nodeport nginx --tcp=80:80
    ```

    **Output:**

    ```
    service/nginx created
    ```

6. Run `kubectl get svc` then make a note of the IP address allocated to the NGINX service.

    **Input:**

    ```
    kubectl get svc
    ```

    **Output:**

    ```
    NAME         TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
    kubernetes   ClusterIP   10.96.0.1      <none>        443/TCP        9m3s
    nginx        NodePort    10.110.36.62   <none>        80:30995/TCP   8s
    ```

## Step 7: Run a benchmark test to create metrics and confirm them streaming into SignalFx!

1. Using the NGINX Cluster-IP address reported from **Step #6** above, use Apache Benchmark (`ab`) to create some traffic to light up your SignalFx NGINX dashboard. Run this a couple of times to generate some metrics!

    **Input:**

    ```
    NGX_ENDPOINT=$(kubectl get svc nginx -o jsonpath='{.spec.clusterIP}')
    ab -n1000 -c20 http://${NGX_ENDPOINT}/
    ```

    **Output:** 

    ```
    This is ApacheBench, Version 2.3 <$Revision: 1826891 $>
    Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
    Licensed to The Apache Software Foundation, http://www.apache.org/
 
    Benchmarking localhost (be patient)
    Completed 100 requests
    ...
    Completed 1000 requests
    Finished 1000 requests
 
    Server Software:        nginx/1.17.5
    Server Hostname:        localhost
    Server Port:            30995...
    ```

2. Validate you are seeing metrics in the UI by going to _**Dashboards → NGINX → NGINX Servers**_ Tip: you can again apply the filter `kubernetes_cluster: [YOUR-INITIALS]-SFX-WORKSHOP` to focus on only your containers.
    ![](https://github.com/signalfx/app-dev-workshop/blob/master/screenshots/m1_l4-nginx-dashboard.png)

## Cleaning up

1. Once you are done with *all* modules of the workshop and no longer need your instance `exit` from the Multipass instance you are in and get back to your system command prompt and enter the following to delete the Multipass instance (replace `[YOUR-INITIALS]` with the ones you used in **Step #1.3**):

    ```
    multipass delete --purge [YOUR-INITIALS]-k3s
    ```

