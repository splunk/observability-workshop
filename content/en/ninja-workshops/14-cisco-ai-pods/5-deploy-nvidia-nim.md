---
title: Deploy the NVIDIA NIM Operator
linkTitle: 5. Deploy the NVIDIA NIM Operator
weight: 5
time: 20 minutes
---

The NVIDIA NIM Operator is used to deploy LLMs in Kubernetes environments, such 
as the OpenShift cluster we created earlier in this workshop. 

This section of the workshop walks through the steps necessary to deploy the 
NVIDIA NIM operator in our OpenShift cluster. 

## Create a NVIDIA NGC Account

An NVIDIA GPU CLOUD (NGC) account is required to download LLMs and deploy them 
using the NVIDIA NIM operator. You can register [here](https://ngc.nvidia.com/signin) 
to create an account. 

## Register with the NVIDIA Developer Program 

Registering with the [NVIDIA Developer Program](https://developer.nvidia.com/) allows us 
to get access to NVIDIA NIM, which we'll use later in the workshop to deploy LLMs. 

Ensure that `NVIDIA Developer Program` appears on your list of NVIDIA subscriptions in NGC: 

![NVIDIA Subscriptions](../images/NVIDIA-Subscriptions.png)

## Generate an NGC API Key

Once you're logged in to the NGC website, click on your user account icon on the 
top-right corner of the screen and select **Setup**. 

Then click **Generate API Key** and follow the instructions. Ensure the key is associated 
with the **NGC Catalog** and **Secrets Manager** services. 

Save the generated key in a safe place as we'll use it later in the workshop. 

Refer to [NVIDIA Documentation](https://docs.nvidia.com/ngc/gpu-cloud/ngc-user-guide/index.html#generating-api-key) 
for further details on generating an NGC API key. 

## Install the Node Feature Discovery Operator

Follow the steps [here](https://docs.redhat.com/en/documentation/openshift_container_platform/4.18/html/specialized_hardware_and_driver_enablement/psap-node-feature-discovery-operator) 
to install the Node Feature Discovery Operator in the OpenShift cluster. 

Ensure you follow the steps under [Creating a NodeFeatureDiscovery CR by using the web console](https://docs.redhat.com/en/documentation/openshift_container_platform/4.18/html/specialized_hardware_and_driver_enablement/psap-node-feature-discovery-operator#creating-nfd-cr-web-console_psap-node-feature-discovery-operator) 
as well. 

## Install the NVIDIA GPU Operator

Follow the steps [here](https://docs.nvidia.com/datacenter/cloud-native/openshift/latest/install-gpu-ocp.html#installing-the-nvidia-gpu-operator-using-the-cli)
to install the NVIDIA GPU Operator in the OpenShift cluster. 

## Install the Operator SDK

Follow the steps [here](https://sdk.operatorframework.io/docs/installation/)
to install the Operator SDK in the OpenShift cluster.

## Install the NGC CLI

Follow the steps [here](https://org.ngc.nvidia.com/setup/installers/cli)
to install the NGC CLI.

## Install the NVIDIA NIM Operator

Log into your OpenShift cluster console using the console URL provided 
from the `rosa describe cluster -c rosa-test` command. 

Navigate to Operators -> OperatorHub and then search for `The NVIDIA NIM Operator for Kubernetes`. 

Use the wizard to install this Operator in your OpenShift cluster. 

![Operator Install](../images/OperatorInstall.png)
