---
title: Build the Sample Application
linkTitle: 5.0 Build the Sample Application
weight: 0
---

For this workshop, we'll be using a microservices-based application. This application is for an online retailer and normally includes more than a dozen services.  However, to keep the workshop simple, we'll be focusing on two services only:  the credit check service and the credit processor service. 

## Pre-requisites
You will start with an EC2 environment that already has some useful components, but we will perform some [initial steps](#initial-steps) in order to get to the following state:
* Install Kubernetes (k3s)
* Deploy the **Splunk distribution of the OpenTelemetry Collector**
* Build and deploy `creditcheckservice` and `creditprocessorservice`
* Deploy a load generator to send traffic to the services

## Initial Steps
To begin the exercise you will need to:
* Get an "Observability Portfolio Demo" environment
* Clone this repo
* Run the setup scripts in order
```
cd workshop/tagging
./1-docker-setup.sh
# Exit and ssh back to this instance
./2-deploy-otel-collector.sh
./3-deploy-creditcheckservice.sh
./4-deploy-creditprocessorservice.sh
```