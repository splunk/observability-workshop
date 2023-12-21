---
title: Creating a Test VM Using Multipass
linkTitle: Multipass
weight: 2
draft: true
---

## Aim

The aim of this module is to guide you through the process of creating a VM locally using Multipass.

Once the configuration of VictorOps is complete you will use this VM to trigger an Alert from SignalFx which in turn will create an Incident within VictorOps, resulting in you getting paged.

---

## 1. Install Multipass

If you do not already have Multipass installed you can download the installer from [here](https://multipass.run/).

Users running macOS can install it using [Homebrew](https://brew.sh/) by running:

=== "Shell Command"

    ```text
    brew cask install multipass
    ```
---

## 2. Create VM using Multipass

### 2.1 Cloud-init

The first step is to pull down the `cloud-init` file to launch a pre-configured VM.

=== "Shell Command"

    ```text
    WSVERSION=2.42
    curl -s \
    https://raw.githubusercontent.com/splunk/observability-workshop/v$WSVERSION/workshop/cloud-init/victorops.yaml \
    -o victorops.yaml
    ```

### 2.2 Launch VM

Remaining in the same directory where you downloaded `victorops.yaml`, run the following commands to create your VM.

The first command will generate a random unique 4 character string. This will prevent clashes in the Splunk UI.

=== "Shell Command"

    ```text
    export INSTANCE=$(cat /dev/urandom | base64 | tr -dc 'a-z' | head -c4)
    multipass launch \
    --name ${INSTANCE} \
    --cloud-init victorops.yaml
    ```

=== "Example Output"

    ```text
    Launched: zevn
    ```

Make a note of your VMs Hostname as you will need it in later steps.

### 2.3 Connect to VM

Once the VM has deployed successfully, in a **new** shell session connect to the VM using the following command.

=== "Shell Command"

    ```text
    multipass shell ${INSTANCE}
    ```

=== "Example Input"

    ```text
    multipass shell zevn
    ```

=== "Example Output"

    ```text
    Last login: Tue Jun  9 15:10:19 2020 from 192.168.64.1
    ubuntu@zevn:~$
    ```

---

## 3. Install SignalFx Agent

An easy way to install the SignalFx Agent into your VM is to copy the install commands from the Splunk UI, then run them directly within your VM.

### 3.1 Splunk UI

Navigate to the **Integrations** tab within the Splunk UI, where you will find the SignalFx SmartAgent tile on the top row.

Click on the SmartAgent tile to open it...

![Integrations](../../../images/integrations-tab.png)

...then select the **Setup** tab...

![SmartAgent](../../../images/smartagent-tile.png)

...then scroll down to 'Step 1' where you will find the commands for installing the agent for both Linux and Windows. You need to copy the commands for Linux, so click the top **copy**{: .label-button .sfx-ui-button-blue} button to place these commands on your clipboard ready for the next step.

![SmartAgent Install](../../../images/smartagent-install.png)

### 3.2 Install Agent

Now paste the linux install commands into your VM Shell, the SignalFx Agent will install and after approx 1 min you should have the following result.

=== "Example Output"

    ```text
    The SignalFx Agent has been successfully installed.

    Make sure that your system's time is relatively accurate or else datapoints may not be accepted.

    The agent's main configuration file is located at /etc/signalfx/agent.yaml.
    ```

---

## 4. Check SignalFx Agent

### 4.1 Agent Status

Once the agent has completed installing run the following command to check the status

=== "Shell Command"

    ```text
    sudo signalfx-agent status
    ```

=== "Example Output"

    ```text
    SignalFx Agent version:           5.3.0
    Agent uptime:                     2m7s
    Observers active:                 host
    Active Monitors:                  9
    Configured Monitors:              9
    Discovered Endpoint Count:        6
    Bad Monitor Config:               None
    Global Dimensions:                {host: zevn}
    GlobalSpanTags:                   map[]
    Datapoints sent (last minute):    237
    Datapoints failed (last minute):  0
    Datapoints overwritten (total):   0
    Events Sent (last minute):        18
    Trace Spans Sent (last minute):   0
    Trace Spans overwritten (total):  0

    Additional status commands:

    signalfx-agent status config - show resolved config in use by agent
    signalfx-agent status endpoints - show discovered endpoints
    signalfx-agent status monitors - show active monitors
    signalfx-agent status all - show everything
    ```

### 4.2 Check the Splunk UI

Navigate to the Splunk UI and click on the **Infrastructure** tab. The click on **Hosts (Smart Agent / collectd)** under the **Hosts** section.

Find your VM and confirm it is reporting in correctly; allow a few minutes for it to appear.

![Infrastructure](../../../images/sfx-infrastructure.png)

If it fails to appear after 3 mins, please let the Splunk Team know so they can help troubleshoot.

---

Because you are using a Multipass VM instead of a Splunk Provided EC2 Instance, you will also need to complete the optional module "Create a Detector".  This will ensure you receive incident notifications for this VM.
