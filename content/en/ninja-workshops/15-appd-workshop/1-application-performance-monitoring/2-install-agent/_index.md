---
title: 2. Install the Java Agent
weight: 2
description: In this exercise you will SSH into your server and proceed to install the Java agent.
---

In this exercise you will perform the following actions:

- Upload the Java agent file to your EC2 instance
- Unzip the file into a specific directory
- Update the Java agents XML configuration file (optional)
- Modify the Apache Tomcat startup script to add the Java agent

## Upload Java Agent to Application VM

By this point you should have received the information regarding the EC2 instance that you will be using for this workshop. Ensure you have the IP address of your EC2 instance, username and password required to ssh into the instance .

On your local machine, open a terminal window and change into the directory where the java agent file was downloaded to. Upload the file into the EC2 instance using the following command. This may take some time to complete.

- Update the IP address or public DNS for your instance.
- Update the filename to match your exact version.

{{< tabs >}}
{{% tab title="Command" %}}

``` bash
cd ~/Downloads
scp -P 2222 AppServerAgent-22.4.0.33722.zip splunk@i-0b6e3c9790292be66.splunk.show:/home/splunk
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
(splunk@44.247.206.254) Password:
AppServerAgent-22.4.0.33722.zip                                                                    100%   22MB 255.5KB/s   01:26
```

{{% /tab %}}
{{< /tabs >}}

## Unzip the Java Agent

SSH into your EC2 instance using the instance and password assigned to you by the instructor.

``` bash
ssh -P 2222 splunk@i-0b6e3c9790292be66.splunk.show
```

Unzip the java agent bundle into a new directory.

``` bash
cd /opt/appdynamics
mkdir javaagent
cp /home/splunk/AppServerAgent-*.zip /opt/appdynamics/javaagent
cd /opt/appdynamics/javaagent
unzip AppServerAgent-*.zip
```

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}
We pre-configured the Java agent using the Controller's Getting Started Wizard. If you download the agent from the AppDynamics Portal, you will need to manually update the Java agent’s XML configuration file.

There are three primary ways to set the configuration properties of the Java agent. These take precedence in the following order:

1. System environment variables.
2. JVM properties passed on the command line.
3. Properties within the ```controller-info.xml``` file.
{{% /notice %}}

## Add the Java Agent to the Tomcat Server

First we want to make sure that the Tomcat server is not running

``` bash
cd /usr/local/apache/apache-tomcat-9/bin
./shutdown.sh
```

We will now modify the catalina script to set an environment variable with the java agent.

``` bash
cd /usr/local/apache/apache-tomcat-9/bin
nano catalina.sh
```

Add the following line at 125 (after the initial comments) & save the file

``` bash
export CATALINA_OPTS="$CATALINA_OPTS -javaagent:/opt/appdynamics/javaagent/javaagent.jar"
```

Restart the server

``` bash
./startup.sh
```

Validate that the Tomcat server is running, this can take a few minutes

{{< tabs >}}
{{% tab title="Command" %}}

``` bash
curl localhost:8080
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <title>Apache Tomcat/9.0.50</title>
        <link href="favicon.ico" rel="icon" type="image/x-icon" />
        <link href="tomcat.css" rel="stylesheet" type="text/css" />
    </head>

    <body>
        <div id="wrapper"
....
```

{{% /tab %}}
{{< /tabs >}}
