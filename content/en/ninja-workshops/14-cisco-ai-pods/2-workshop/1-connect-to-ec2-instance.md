---
title: Connect to EC2 Instance
linkTitle: 1. Connect to EC2 Instance
weight: 1
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

Use the cluster API, participant username, and password provided by the workshop 
organizer to log in to the OpenShift cluster: 

``` bash
oc login https://api.<cluster-domain>:443 -u <username> -p '<password>'
```

Ensure you're connected to the OpenShift cluster: 

``` bash
oc whoami --show-server  
```

It should return something like the following: 

````
https://api.***.openshiftapps.com:443
````