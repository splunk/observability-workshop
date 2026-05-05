---
title: Connect to EC2 Instance
linkTitle: 1. Connect to EC2 Instance
weight: 1
time: 5 minutes
---

## Connect to your EC2 Instance

We’ve prepared an Ubuntu Linux instance in AWS/EC2 for each attendee: 

* Access the **Splunk Show** event by clicking on the link for your region
* Click **Enroll** on the top-right corner
* Then look near the bottom of the page for your EC2 instance details

You should see connection information such as the following: 

![Connection Information](../images/ConnectionInformation.png)

Using the IP address (which is part of the **SSH Command**) 
and **SSH Password** provided as part of the **Connection Information**, 
connect to your EC2 instance using one of the methods below:

* Mac OS / Linux
    * ssh splunk@IP address
* Windows 10+
    * Use the OpenSSH client
* Earlier versions of Windows
    * Use Putty 

{{% notice title="VPN Connection" style="green" icon="running" %}}

If you're working from an office and having trouble connecting, try connecting 
to your corporate VPN first. 

{{% /notice %}}

## Retrieve your Instance Name 

Once you've logged into your EC2 instance via ssh, use the following command to 
get your instance name: 

```bash
echo $INSTANCE
```

Make a note of this, as your instance name is unique to you and will be 
used later in the workshop to find your data in Splunk Observability Cloud. 
