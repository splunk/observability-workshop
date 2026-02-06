---
title: Connect to the OpenShift Cluster
linkTitle: 2. Connect to the OpenShift Cluster
weight: 2
time: 5 minutes
---

## Connect to your EC2 Instance

We’ve prepared an Ubuntu Linux instance in AWS/EC2 for each attendee.

Using the IP address and password provided by your instructor, connect to your EC2 instance
using one of the methods below:

* Mac OS / Linux
    * ssh splunk@IP address
* Windows 10+
    * Use the OpenSSH client
* Earlier versions of Windows
    * Use Putty 

## Set the Workshop Participant Number

The instructor will provide each participant with a number from 1 to 30. 
Store this in an environment variable, and remember what it is, as
it will be used throughout the workshop: 

``` bash
export PARTICIPANT_NUMBER=<your participant number>
```

## Install the OpenShift CLI

To access the OpenShift cluster, we'll need to install the OpenShift CLI.

We can use the following command to download the OpenShift CLI binary directly
to our EC2 instance:

````
curl -L -O https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/stable/openshift-client-linux.tar.gz
````

Extract the contents:

````
tar -xvzf openshift-client-linux.tar.gz
````

Move the resulting files (`oc` and `kubectl`) to a location that's included as part of your path.  For example:

``` bash
sudo mv oc /usr/local/bin/oc
sudo mv kubectl /usr/local/bin/kubectl
```

## Connect to the OpenShift Cluster

Ensure the Kube config file is modifiable by the splunk user: 

``` bash
chmod 600 /home/splunk/.kube/config
```

Use the cluster API URL and password provided by the workshop 
organizer to log in to the OpenShift cluster: 

``` bash
oc login https://api.<cluster-domain>:443 -u participant$PARTICIPANT_NUMBER -p '<password>'
```

Ensure you're connected to the OpenShift cluster: 

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
oc whoami --show-server 
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
https://api.***.openshiftapps.com:443
```

{{% /tab %}}
{{< /tabs >}}
