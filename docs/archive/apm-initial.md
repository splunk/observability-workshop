## Before We Start - SignalFx Org Access
_An organisation needs to be pre-provisioned as a µAPM entitlement is required for the purposes of this module. Please contact someone from SignalFx to get a trial instance with µAPM enabled if you don’t have one already._

_To check if you have an organisation with µAPM enabled, just login to SignalFx and check that you have the µAPM tab on the top navbar next to Dashboards._

---

## Step 1: Create an instance with Multipass and deploy the SmartGateway
1. If you have executed Module 1 of this workshop, then skip the multipass installation and zip download as you already have this, and go straight to Step#1.5

2. Install Multipass for your OS - https://multipass.run/. On a Mac you can also install via brew, e.g. `brew cask install multipass`

3. Obtain your Access Token (and take note of your Realm from under My Profile) in the SignalFx UI

4. Download the App Dev Workshop master zip file and unzip it
   ```
   curl -LO https://github.com/signalfx/app-dev-workshop/archive/master.zip
   unzip master.zip
   ```

5. Change into the `app-dev-workshop-master` directory
   ```
   cd app-dev-workshop-master
   ```

6. Edit `cloud-init/smart-gateway.yaml` and on line #30 replace ACCESS_TOKEN with your SignalFx token, REALM with the SignalFx realm you are running in, HOSTNAME with YOUR_INITIALS-sg and CLUSTER_NAME with YOUR_INITIALS-sg-cluster. NOTE: The hostname defined here will be the same hostname that we will use to launch the instance in Step #1.7
   ```yaml
   #cloud-config
   package_update: true
   package_upgrade: true

   write_files:
    - content: |
         [Unit]
         Description=SignalFx Smart Gateway
         After=network.target
         [Service]
         ExecStart=/usr/local/bin/smart-gateway --configfile /var/lib/gateway/etc/gateway.conf
         KillMode=mixed
         Restart=on-failure
         Type=simple
         User=root
         Group=root
         [Install]
         WantedBy=multi-user.target
      path: /lib/systemd/system/smart-gateway.service
      permissons: '0644'
   runcmd:
    - 'curl https://raw.githubusercontent.com/signalfx/app-dev-workshop/master/etc/motd -o /etc/motd'
    - 'curl https://raw.githubusercontent.com/signalfx/app-dev-workshop/master/smart-gateway/install.sh -o /home/ubuntu/smartgateway-install.sh'
    - chown ubuntu:ubuntu /home/ubuntu/smartgateway-install.sh
    - chmod 755 /home/ubuntu/smartgateway-install.sh
    # Replace ACCESS_TOKEN, REALM, HOSTNAME & CLUSTER_NAME accordingly
    - ./home/ubuntu/smartgateway-install.sh ACCESS_TOKEN REALM HOSTNAME CLUSTER_NAME
    - systemctl enable smart-gateway.service
    - systemctl daemon-reload
    - systemctl restart smart-gateway
   ```
   
7. Now we can start up the SmartGateway instance, replacing YOUR_INITIALS accordingly.
   ```
   multipass launch --name YOUR_INITIALS-sg --cloud-init cloud-init/smart-gateway.yaml
   ```

8. Find out which IP address has been assigned for the newly created instance and make a note of the IPv4 address that has been assigned.
   ```
   multipass list
   ```

   ```
   Name                    State             IPv4             Image
   rwc-sg                  Running           192.168.64.30    Ubuntu 18.04 LTS
   ```

9. Shell into the newly created Smart-Gateway instance. Please use your initials to prefix `sg` for the name of the instance.
   ```
   multipass shell YOUR_INITIALS-sg
   ```

10. Test the gateway is running and working with the following `curl` command
    ```
    curl -d'[]' -H'Content-Type:application/json' 127.0.0.1:8080/v1/trace
    ```

    If result is `"OK"` we can continue, else validate the steps above.

---

## Step 2: Deploy the SmartAgent in the SmartGateway instance to monitor the SmartGateway (now that’s a really smart instance!)
1. Remaining in the shell for the SmartGateway instance, next we need to install a SmartAgent to monitor SmartGateway. Using the same `ACCESS_TOKEN` that was used in **Step #1** above.
   ```bash
   curl -sSL https://dl.signalfx.com/signalfx-agent.sh > /tmp/signalfx-agent.sh
   sudo sh /tmp/signalfx-agent.sh --realm YOUR_REALM YOUR_ACCESS_TOKEN
   ```

2. Once the Agent has installed edit `sudo vi /etc/signalfx/agent.yaml` and add the `extraDimensions` under the `signalfx-metadata` plugin. For the cluster parameter you will need to set it to exactly what was used for the SmartGateway installation above e.g. `YOUR_INITIALS-sg-cluster`. You do not need to restart the agent for this change to take effect.
   ```yaml
   - type: collectd/signalfx-metadata
     extraDimensions:
       source: gateway
       cluster: YOUR_INITIALS-sg-cluster
   ```

3. Once the installation and configuration is complete, validate the agent is running.
   ```
   signalfx-agent status
   ```

   ```
   SignalFx Agent version:           4.18.3
   Agent uptime:                     3s
   Observers active:                 host
   Active Monitors:                  10
   Configured Monitors:              10
   Discovered Endpoint Count:        6
   Bad Monitor Config:               None
   Global Dimensions:                {host: rwc}
   Datapoints sent (last minute):    0
   Datapoints failed (last minute):  0
   Datapoints overwritten (total):   0
   Events Sent (last minute):        0
   Trace Spans Sent (last minute):   0
   Trace Spans overwritten (total):  0
   ```

---

## Step 3: Create the Application instance with Multipass and deploy the SmartAgent
1. Open a new terminal and create a Multipass instance to host the application and the SmartAgent. We shall refer to this as the Application instance. Please use your initials to prefix `app` for the name of the instance.
   ```
   multipass launch --name YOUR_INITIALS-app --cloud-init cloud-init/application.yaml
   ```

2. Find out which IP address has been assigned for the newly created instance and make a note of the IPv4 address that has been assigned.
   ```
   multipass list
   ```

   ```
   Name                    State             IPv4             Image
   rwc-app                 Running           192.168.64.31    Ubuntu 18.04 LTS
   rwc-sg                  Running           192.168.64.30    Ubuntu 18.04 LTS
   ```

3. Once the instance has been successfully created shell into it.
   ```
   multipass shell YOUR_INITIALS-app
   ```

4. Next we need to install the SmartAgent itself using the same `ACCESS_TOKEN` that was used in **Step #1** above.
   ```bash
   curl -sSL https://dl.signalfx.com/signalfx-agent.sh > /tmp/signalfx-agent.sh
   sudo sh /tmp/signalfx-agent.sh --realm YOUR_REALM YOUR_ACCESS_TOKEN
   ```

5. Once the installation is complete, validate the agent is running.
   ```
   signalfx-agent status
   ```

   ```
   SignalFx Agent version:           4.18.3
   Agent uptime:                     3s
   Observers active:                 host
   Active Monitors:                  10
   Configured Monitors:              10
   Discovered Endpoint Count:        6
   Bad Monitor Config:               None
   Global Dimensions:                {host: rwc}
   Datapoints sent (last minute):    0
   Datapoints failed (last minute):  0
   Datapoints overwritten (total):   0
   Events Sent (last minute):        0
   Trace Spans Sent (last minute):   0
   Trace Spans overwritten (total):  0
   ```

---

## Step 4: Update the Application instance to accept traces and to send traces to the SmartGateway
1. Remaining in the Application instance, edit `sudo vi /etc/signalfx/cluster` with the cluster name used in the SmartGateway configuration from **Step #1** e.g. `YOUR_INITIALS-sg-cluster`

2. Edit `/etc/signalfx/agent.yaml` and add `traceEndpointUrl` parameter and value just before `intervalSeconds` parameter. Please use the IP address from **Step #1.7**.
   ```yaml
   traceEndpointUrl: http://SMART_GATEWAY_IP_ADDRESSS:8080/v1/trace 
   ```

3. Under the monitors section of the `agent.yaml` add the following (best placed at the end of the list of monitors)
   ```yaml
   - type: trace-forwarder
     listenAddress: 127.0.0.1:9080
   ```

4. Check the trace-forwarder is responding
   ```
   curl -d'[]' -H'Content-Type:application/json' 127.0.0.1:9080/v1/trace
   ```

   If result is "OK" we can continue, else validate the steps above.

---

## Step 5: Confirm the SignalFx Agents have been installed correctly and are sending data back to our platform
1. Navigate to the Infrastructure Tab within the SignalFx UI, and then select Hosts (Smart Agent / collectd) from the navigation pane on the left

2. In the Filter at the top of the main page, enter host:<your initials>*  (notice the * at the end), to only display your VMs which should have a hostname starting with your initials.

3. Select the System Metrics option

4. You should now have a heat map with two squares representing your two hosts, plus a selection of charts showing their metrics. This confirms the SignalFx Agent is installed correctly on each VM.

---

## Step 6: Confirm the Smart Gateway has been installed correctly and is sending data back to our platform
1. Navigate to the Dashboards tab within the SignalFx UI, and then enter smart into the search box to quickly find the Smart Gateway Dashboard Group.

2. Select the Cluster(s) dashboard to open it.

3. Select your cluster name from the Cluster Override dropdown in the tool bar.

4. You should now see a display similar to below showing your Smart Gateway Heat Map, and its Activity, which should be minimal at this time.

Once you finish, please proceed to [Lab 2: Traced Python Application Example](https://github.com/signalfx/app-dev-workshop/wiki/Module-2-Lab-2:-Traced-Python-Application-Example)
