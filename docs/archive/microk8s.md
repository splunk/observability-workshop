__## Summary of this lab:
* Download the workshop and configure Kubernetes ([MicroK8s](https://microk8s.io/)) environment.  
* Use the SignalFx Helm chart to install the Smart Agent in MicroK8s.
* Deploy a NGINX ReplicaSet into MicroK8s and confirm the auto discovery of your NGINX deployment.
* Run a benchmark test to create metrics and confirm them streaming into SignalFX!

---

## Step 1: Let’s bake some K8s
1. Install Multipass for your OS - https://multipass.run/. On a Mac you can also install via `brew` e.g. `brew cask install multipass`

2. Download the App Dev Workshop master zip file, unzip the file and change into the app-dev-workshop-master directory
   ```bash
   curl -LO https://github.com/signalfx/app-dev-workshop/archive/master.zip
   unzip master.zip
   cd app-dev-workshop-master
   ```

3. Launch the Multipass instance which will run Kubernetes. **Note:** Use `[YOUR-INITIALS]-microk8s` this is so the value of the instance hostname is unique e.g. `rwc-microk8s`
   ```bash
   multipass launch --name [YOUR-INITIALS]-microk8s --cloud-init cloud-init/microk8s.yaml --cpus=4 --mem=2G
   ```

4. Once the instance has been successfully created shell into it.
   ```bash
   multipass shell [YOUR-INITIALS]-microk8s
   ```

---

## Step 2: I’ve got the key, I’ve got the secret!
1. You will need to obtain your Access Token from the SignalFx UI once Kubernetes is running. You can find your Access Token by clicking on your profile icon on the top right of the SignalFx UI. Then select _**Organisation Settings → Access Tokens**_.  Expand the Default token, then click on _**Show Token**_ to expose your token. Later in the lab you can come back here and click the _**Copy**_ button which will copy it to your clipboard  so you can paste it when you need to provide an access token in the lab.
![Access Token](https://github.com/signalfx/app-dev-workshop/blob/master/screenshots/m1-l4-access-token.png)

2. You will also need to obtain the name of the Realm for your SignalFx account.  Click on the profile icon again, but this time select 'My Profile'.  The Ream can be found in the middle of the page within the Organizations section.  In this example it is us1.
![Realm](https://github.com/signalfx/app-dev-workshop/blob/master/screenshots/m1-l4-realm.png)

---

## Step 3: Take the Helm!
1. Install the agent using the SignalFx Helm chart. Firstly, add the SignalFx Helm chart repository to Helm.
   ```
   helm repo add signalfx https://dl.signalfx.com/helm-repo
   ```

2. Ensure the latest state of the repository
   ```
   helm repo update
   ```
3. Create the following variables to use in the proceeding helm install command:
   ```
   export ACCESS_TOKEN=<token from Step 2>
   export REALM=<realm from Step 2>
   export INITIALS=<your initials e.g. GH>
   export VERSION=<latest Smart Agent version e.g. 5.0.4>
   ```

4. Install the Smart Agent chart with the following configuration values for the chart.
   ```
   helm install --set signalFxAccessToken=$ACCESS_TOKEN --set clusterName=APP-DEV-WORKSHOP --set kubernetesClusterName=$INITIALS-AD-WORKSHOP --set agentVersion=$VERSION --set signalFxRealm=$REALM --set traceEndpointUrl=https://ingest.$REALM.signalfx.com/v2/trace signalfx-agent signalfx/signalfx-agent -f workshop/microk8s/values.yaml
   ```

5. You can monitor the progress of the deployment by running `kubectl get pods` which should typically report a new pod is up and running after about 30 seconds. Ensure the status is reported as Running before continuing.

   _Input:_
   ```
   kubectl get pods
   ```

   **Output:**
   ```
   NAME                   READY   STATUS    RESTARTS   AGE
   signalfx-agent-66tvr   1/1     Running   0          7s
   ```

6. Ensure there are no errors by tailing the logs from the Smart Agent Pod. Output should look similar to the log output shown below. Use the label set by the `helm` install to tail logs (You will need to press Ctrl-C to exit). Or use the installed `k9s` terminal UI for bonus points!

   **Input:**
   ```
   kubectl logs -l app=signalfx-agent -f
   ```

   **Output:**
   ```
   time="2020-03-20T11:53:33Z" level=info msg="Starting up agent version 5.0.0"
   time="2020-03-20T11:53:33Z" level=info msg="Watching for config file changes"
   time="2020-03-20T11:53:33Z" level=info msg="New config loaded"
   time="2020-03-20T11:53:33Z" level=info msg="Using log level info"
   time="2020-03-20T11:53:33Z" level=info msg="Fetching host id dimensions"
   time="2020-03-20T11:53:33Z" level=info msg="Trying to get fully qualified hostname"
   time="2020-03-20T11:53:33Z" level=info msg="Using hostname rwc-microk8s"
   time="2020-03-20T11:53:34Z" level=info msg="Using host id dimensions map[host:rwc-microk8s kubernetes_node_uid:4350df0d-1849-45ce-b805-d04089f36dd1]"
   time="2020-03-20T11:53:34Z" level=info msg="Sending datapoints to https://ingest.us0.signalfx.com/v2/datapoint"
   time="2020-03-20T11:53:34Z" level=info msg="Sending events to https://ingest.us0.signalfx.com/v2/event"
   time="2020-03-20T11:53:34Z" level=info msg="Sending trace spans to https://ingest.us0.signalfx.com/v1/trace"
   time="2020-03-20T11:53:34Z" level=info msg="Setting cluster:APP-DEV-WORKSHOP property on host:rwc-microk8s dimension"

   ```

7. In the SignalFx UI, got to _**Dashboards → Kubernetes**_ and open the K8s Clusters dashboard to ensure metrics are being sent. (Might take up to 5 minutes for these charts to update as they are 5 minute resolution charts).
![K8S Clusters Dashboard Link](https://github.com/signalfx/app-dev-workshop/blob/master/screenshots/m1-l4-k8s-clusters.png)

8. Use the dashboard filter to narrow down to your K8s cluster e.g. `kubernetes_cluster: [YOUR-INITIALS]-SFX-WORKSHOP`
![K8S Clusters Filter](https://github.com/signalfx/app-dev-workshop/blob/master/screenshots/m1-l4-k8s-clusters-filter.png)

---

## Step 4: Start your NGINX!
1. Still within the Microk8s shell session, change into the `nginx` directory
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

6. Run `kubectl get svc` then make a note of the IP address allocated to NGINX.
   
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

7. Using the IP address reported from **Step #7** above, use Apache Benchmark (ab) to create some traffic to light up your SignalFx NGINX dashboard. Run this a couple of times!
   
   **Input:**
   ```
   ab -n1000 -c20 http://10.110.36.62/
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

8. Validate you are seeing metrics in the UI by going to _**Dashboards → NGINX → NGINX Servers**_ Tip: you can again apply the filter `kubernetes_cluster: [YOUR-INITIALS]-SFX-WORKSHOP` to focus on only your containers.
   ![](https://github.com/signalfx/app-dev-workshop/blob/master/screenshots/m1_l4-nginx-dashboard.png)

---

Once you are finished please proceed to [Lab 5: Monitoring as Code with Detectors](https://github.com/signalfx/app-dev-workshop/wiki/Module-1-Lab-5:-Monitoring-as-Code-with-Detectors)
