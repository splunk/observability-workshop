---
title: Install Database Agent
time: 2 minutes
weight: 3
description: In this exercise you will upload the database visiblity agent, unzip the downloaded file, and start the database visiblity agent.
---

The AppDynamics Database Agent is a standalone Java program that collects performance metrics about your database instances and database servers. You can deploy the Database Agent on any machine running Java 1.8 or higher. The machine must have network access to the AppDynamics Controller and the database instance that you want to be monitored.

A database agent running on a typical machine with 16 GB of memory can monitor about 25 databases. On larger machines, a database agent can monitor up to 200 databases.

In this exercise you will perform the following tasks:

- Upload the Database Visibility agent file to your Application VM
- Unzip the file into a specific directory on the file system
- Start the Database Visibility agent

## Upload Database Agent to The Application VM

By this point you should have received the information regarding the EC2 instance that you will be using for this workshop. Ensure you have the IP address of your EC2 instance, username and password required to ssh into the instance .

On your local machine, open a terminal window and change into the directory where the database agent file was downloaded to. Upload the file into the EC2 instance using the following command. This may take some time to complete. If you are in a Windows OS, you may have to use a programm such as WinSCP.

* Update the IP address or public DNS for your instance.
* Update the filename to match your exact version.

{{< tabs >}}
{{% tab title="Command" %}}
``` bash
cd ~/Downloads
scp -P 2222 db-agent-*.zip splunk@i-0267b13f78f891b64.splunk.show:/home/splunk
```
{{% /tab %}}
{{% tab title="Example Output" %}}
``` bash
splunk@i-0267b13f78f891b64.splunk.show's password:
db-agent-25.7.0.5137.zip                                                                                                                               100%   70MB   5.6MB/s   00:12
```
{{% /tab %}}
{{< /tabs >}}


## Install the Database Agent

Create the directory structure where you will unzip the Database agent zip file.

```bash
cd /opt/appdynamics
mkdir dbagent
```

Use the following commands to copy the Database agent zip file to the directory and unzip the file. The name of your Database agent file may be slightly different than the example below. 

```bash
cp ~/db-agent-*.zip /opt/appdynamics/dbagent/
cd /opt/appdynamics/dbagent
unzip db-agent-*.zip
```

## Start the Database Visibility agent

Use the following commands to start the Database agent and verify that it started.

**Append your inititals to the db agent name**, this will be used in the following section. example: DBMon-Lab-Agent-IO

```bash
cd /opt/appdynamics/dbagent
nohup java -Dappdynamics.agent.maxMetrics=300000 -Ddbagent.name=DBMon-Lab-Agent-YOURINITIALS -jar db-agent.jar &
ps -ef | grep db-agent
```

You should see output similar to the following image.

![Output](images/04-dbagent-install.png)
