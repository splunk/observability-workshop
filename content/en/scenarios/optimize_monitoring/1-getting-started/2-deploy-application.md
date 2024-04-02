---
title: Deploy OpenTelemetry Demo Applciation
linkTitle: 1.2 Deploy OpenTelemetry Demo Application
weight: 3
authors: ["Tim Hard"]
time: 10 minutes
draft: false
---

## Introduction

For this workshop, we'll be using the **OpenTelemetry Demo Application** running in Kubernetes. This application is for an online retailer and includes more than a dozen services written in many different languages. While metrics, traces, and logs are being collected from this application, this workshop is primarily focused on how **Splunk Observability Cloud** can be used to more efficiently monitor infrastructure.  

## Pre-requisites

* You should have access to the EC2 instance provided in section [1.1 Access AWS/EC2 Instance](./1-access-ec2)

## Initial Steps

The initial setup can be completed by executing the following steps on the command line of your EC2 instance.

``` bash
cd ~/workshop/optimize-cloud-monitoring && \
./deploy-application.sh
```

You'll be asked to enter your favorite city. This will be used in the OpenTelemetry Collector configuration as a **custom tag** to show how easy it is to add additional context to your observability data. 

{{% notice title="Note" style="info" %}}
Custom tagging will be covered in more detail in the [Standardize Data Collection](../standardize_data_collection/) section of this workshop.
{{% /notice %}}

![Enter Favorite City](../../images/favorite-city.png?width=40vw)

<center>
<b>Your application should now be running and sending data to Splunk Observability Cloud. You'll dig into the data in the next section</b>
</center>