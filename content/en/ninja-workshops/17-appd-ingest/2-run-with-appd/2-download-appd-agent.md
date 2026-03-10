---
title: 2. Download the AppD Agent
weight: 2
---

You need the AppDynamics Java Agent (version 25.6.0 or higher) to use dual signal mode. You'll download it from the AppDynamics Controller's Getting Started Wizard.

## Log in to the AppDynamics Controller

Open the [AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) in your browser and log in with your Cisco credentials.

## Launch the Getting Started Wizard

1. Select **Overview** on the left navigation panel
2. Click on the **Getting Started** tab
3. Click on the [**Getting Started Wizard**](https://se-lab.saas.appdynamics.com/controller/#/location=GETTING_STARTED_JAVA&timeRange=last_15_minutes.BEFORE_NOW.-1.-1.15) button

## Configure Your Application

1. Select **Java** as the Application Type
2. Select **JDK8+** for the JVM type
3. Accept defaults for the Controller connection
4. Under **Set Application and Tier**:
   - **Application Name**: `Dual-Ingest-<YOURINITIALS>` (must be unique -- append your initials)
   - **Tier Name**: `OrderService`
   - **Node Name**: `OrderService-Node`
5. Click **Continue**
6. Click **Click Here to Download**

![AppDynamics Agent](../../_images/appd-agent.png?width=30vw)

## Transfer the Agent to Your EC2 Instance

The agent ZIP downloads to your local machine. Upload it to your EC2 instance:

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
Replace the filename with the exact version you downloaded, and use your instance's hostname.
{{% /notice %}}

```bash
scp -P 2222 ~/Downloads/AppServerAgent-<your-downloaded-version>.zip splunk@<your-instance>.splunk.show:~/workshop/appd/
```
**Example:** `scp -P 2222 ~/Downloads/AppServerAgent-1.8-26.1.0.37621.zip splunk@i-0e279f0be5347a79e.splunk.show:~/workshop/appd/`

## Unzip the Agent

SSH into your instance and unzip the agent:

```bash
cd ~/workshop/appd
mkdir -p agent
unzip AppServerAgent-*.zip -d agent/
```

You should now have the agent JAR at `~/workshop/appd/agent/javaagent.jar`.

## Note Your Account Access Key

You'll need the [**Account Access Key**](https://se-lab.saas.appdynamics.com/controller/#/licensing/license-management-account?timeRange=last_15_minutes.BEFORE_NOW.-1.-1.15) when running the app. You can find it in the AppDynamics Controller:

1. Go to **Settings** (gear icon) → **License** 
2. Click the left side bar for **Account***
2. Under **Account**, note the **Name** (`se-lab`) and **Access Key**

{{% notice title="Keep it handy" style="primary" icon="lightbulb" %}}
You'll use the Account Name and Access Key in the next step as JVM properties. They authenticate the agent to the controller.
{{% /notice %}}
