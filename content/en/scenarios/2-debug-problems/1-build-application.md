---
title: Build the Sample Application
linkTitle: 5.1 Build the Sample Application
weight: 1
---

{{% badge icon="clock" color="#ed0090" %}}10 minutes{{% /badge %}}

## Introduction

For this workshop, we'll be using a Java-based application called `The Door Game`.  It will be hosted in Kubernetes.

## Pre-requisites

You will start with an EC2 instance and perform some [initial steps](#initial-steps) in order to get to the following state:

* Install Kubernetes (k3s) and Docker
* Deploy the **Splunk distribution of the OpenTelemetry Collector**
* Deploy the MySQL database container and populate data 
* Build and deploy the `doorgame` application container

## Initial Steps

The initial setup can be completed by executing the following steps on the command line of your EC2 instance.

You'll be asked to enter a name for your environment.  Please use `profiling-workshop-yourname` (where `yourname` is replaced by your actual name).

``` bash
cd workshop/profiling

./1-docker-setup.sh

# Exit and ssh back to this instance

# return to the same directory as before 
cd workshop/profiling

# ensure Docker is running 
sudo systemctl start docker

./2-deploy-otel-collector.sh
./3-deploy-mysql.sh
./4-deploy-doorgame.sh
```

## Let's Play The Door Game

Now that the application is deployed, let's play with it and generate some observability data.

Get the external IP address for your application instance using the following command:

```` bash
kubectl describe svc doorgame | grep "LoadBalancer Ingress"
````

The output should look like the following:

```` text
LoadBalancer Ingress:     52.23.184.60
````

You should be able to access The Door Game application by pointing your browser to port 81 of the provided IP address.  For example:

```` text
http://52.23.184.60:81
````

You should be met with The Door Game intro screen:

![Door Game Welcome Screen](../images/door_game_initial_screen.png)

Click `Let's Play` then choose a door:

![Door Game Choose Door Screen](../images/door_game_choose_door.png)

Play through a couple of times to get the feel for the application flow... and then play many times to ensure there are enough spans to create usable Profiling data...

## View your application in Splunk Observability Cloud

Now that the setup is complete, let's confirm that it's sending data to **Splunk Observability Cloud**.  Note that when the application is deployed for the first time, it may take a few minutes for the data to appear.

Navigate to APM, then use the Environment dropdown to select your environment (i.e. `profiling-workshop-name`).

If everything was deployed correctly, you should see `doorgame` displayed in the list of services:

![APM Overview](../images/apm_overview.png)

Click on **Explore** on the right-hand side to view the service map.  We should the `doorgame` application on the service map:

![Service Map](../images/service_map.png)

Next, click on **Traces** on the right-hand side to see the traces captured for this application. You'll see that some traces run relatively fast (i.e. just a few milliseconds), whereas others take a few seconds.

![Traces](../images/traces.png)
