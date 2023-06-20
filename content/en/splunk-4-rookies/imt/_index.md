---
title: Splunk4Rookies - Infrastructure Monitoring
linkTitle: Splunk IM
description: Whether on-prem, hybrid or multicloud, Splunk delivers real-time monitoring and troubleshooting to help you maximize infrastructure performance with complete visibility.
weight: 1
alwaysopen: false
---

Splunk Infrastructure monitoring provides real-time visibility into the health and performance of your entire infrastructure (physical, virtual and cloud) and the applications and services that run on it. It collects metrics and events from more than 200 sources and provides pre-built dashboards and alerts to help you monitor and troubleshoot your environment.

The first part of the workshop will focus on getting familiar with the Splunk Infrastructure Monitoring UI and the various features it provides. We will cover off:

- Dashboards
- Detectors (Alerting)
- Service Bureau

The second part will focus on getting data into Splunk Infrastructure Monitoring and APM where we will cover off:

- Splunk OpenTelemetry Connector (Getting Data In)
- Monitoring Kubernetes
- APM Service Map
- Troubleshooting a microservice application

{{% expand title="{{% badge style=primary icon=user-ninja %}}**Ninja Mode:** Accessing your AWS/EC2 instance{{% /badge %}}" %}}

## 1. Get your allocated AWS/EC2 instance

In preparation for the workshop, Splunk has prepared an Ubuntu Linux instance in AWS/EC2.

To get access to the instance that you will be using in the workshop please visit the URL to access the Google Sheet provided by the workshop leader.

Search for your AWS/EC2 instance by looking for your first  and last name, as provided during registration for this workshop.

Find your allocated IP address, SSH command (for Mac OS, Linux and the latest Windows versions) and password to enable you to connect to your workshop instance.

The sheet also has a URL for SSH-in-browser that you can use in case you cannot connect via SSH.

{{% notice title="Important" style="info" %}}
Please use SSH (or [Putty](https://www.putty.org/) if you are **not** running Windows 10 or above) to gain access to your EC2 instance and make a note of the associated IP address as you will need this during the workshop.
{{% /notice %}}

## 2. SSH (Mac OS/Linux)

Most attendees will be able to connect to the workshop by using SSH from their Mac or Linux device, or on Windows 10 and above.

To use SSH, open a terminal on your system and type:

``` bash
ssh ubuntu@x.x.x.x`
```

replacing `x.x.x.x` with the IP address found in Step #1.

When prompted **`Are you sure you want to continue connecting (yes/no/[fingerprint])?`** please type **`yes`**.

Enter the password provided in the Google Sheet from Step #1.

Upon successful login you will be presented with the Splunk logo and the Linux prompt.

## 3. SSH (Windows 10 and above)

The procedure described above is the same on Windows 10, and the commands can be executed either in the Windows Command Prompt or PowerShell.
However, Windows regards its SSH Client as an "optional feature", which might need to be enabled.

You can verify if SSH is enabled by simply executing `ssh`. If you are shown a help text on how to use the `ssh` command you are all set.

If you don't see the help text you will need to enable the "OpenSSH Client" feature manually. To do that, open the "Settings" menu, and click on "Apps". While being in the "Apps & features" section, click on "Optional features".

You will be presented a list of installed features. On the top, you see a button with a plus icon to "Add a feature". Click it.
In the search input field, type `OpenSSH`, and find a feature called "OpenSSH Client". Click on it, and click the "Install" button.

Now you are set! In case you are not able to access the provided instance in spite of enabling the OpenSSH feature, please let your instructor know.

At this point you are ready to continue and [start the workshop](dashboards)

## 4. Web Browser

If you are blocked from using SSH (Port 22) or unable to install Putty you may be able to connect to the workshop instance by using a web browser.

{{% notice title="Note" style="info" %}}
This assumes that access to port 6501 is not restricted by your company's firewall.
{{% /notice %}}

Open your web browser and type **[http://x.x.x.x:6501](http://x.x.x.x:6501)** (where x.x.x.x is the IP address from the Google Sheet).

Once connected, login in as **ubuntu** using the password that is provided in the Google Sheet. For entering the password, you can enter it either by typing manually or just right click on your browser screen and select 'Paste from browser' and paste the password into the box labelled **Paste into this box**, then click **OK**. This approach will work for any other copy and paste operations you need to do throughout this workshop.

{{% notice title="Note" style="info" %}}
Unlike regular SSH connection, the web browser has a 60 second time out, and you will be disconnected, and a **Connect** button will be shown in the center of the web terminal. Simply click the **Connect** button and you will be reconnected and will be able to continue.
{{% /notice %}}

At this point you are ready to continue and [start the workshop](dashboards).

## 5. Multipass (All)

If you are unable to access AWS, you can spin up a virtual machine locally, follow the instructions for [using Multipass](https://github.com/splunk/observability-workshop/blob/main/multipass/README.md).

{{% /expand %}}
