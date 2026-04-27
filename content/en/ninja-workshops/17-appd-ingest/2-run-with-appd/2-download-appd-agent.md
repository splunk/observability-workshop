---
title: 2. Download the AppD Agent
weight: 2
---

You need the AppDynamics Java Agent (version 25.6.0 or higher) to use dual signal mode. We'll add it to your instance.

## Unzip the Agent

SSH into your instance, run the download script, and the agent will be extracted to the `agent` directory we created:

```bash
cd ~/workshop/appd
mkdir -p agent
chmod +x ./download-appd-agent.sh
./download-appd-agent.sh
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
