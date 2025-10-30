---
title: Wrap-Up
linkTitle: 10. Wrap-Up
weight: 10
time: 5 minutes
---

## Wrap-Up

We hope you enjoyed this workshop, which provided hands-on experience deploying and working
with several of the technologies that are used to monitor Cisco AI PODs with
Splunk Observability Cloud. Specifically, you had the opportunity to:

* Deploy a RedHat OpenShift cluster with GPU-based worker nodes.
* Deploy the NVIDIA NIM Operator and NVIDIA GPU Operator.
* Deploy Large Language Models (LLMs) using NVIDIA NIM to the cluster.
* Deploy the OpenTelemetry Collector in the Red Hat OpenShift cluster.
* Add Prometheus receivers to the collector to ingest infrastructure metrics.
* Deploy the Weaviate vector database to the cluster.
* Instrument Python services that interact with Large Language Models (LLMs) with OpenTelemetry.
* Understand which details which OpenTelemetry captures in the trace from applications that interact with LLMs.

## Clean Up Steps

Follow the steps in this section to uninstall the OpenShift cluster. 

Get the cluster ID, the Amazon Resource Names (ARNs) for the cluster-specific Operator roles, 
and the endpoint URL for the OIDC provider by running the following command:

``` bash
rosa describe cluster --cluster=$CLUSTER_NAME
```

Delete the cluster using the following command

``` bash
rosa delete cluster --cluster=$CLUSTER_NAME --watch
```

Delete the cluster-specific Operator IAM roles: 

> Note: just accept the default values when prompted.

``` bash
rosa delete operator-roles --prefix $OPERATOR_ROLES_PREFIX
```

Delete the OIDC provider: 

> Note: just accept the default values when prompted.

``` bash
rosa delete oidc-provider --oidc-config-id $OIDC_ID
```

Delete the network: 

> Note: add the name of the CloudFormation stack used to create the network before 
> running the following command

``` bash
aws cloudformation delete-stack --region $AWS_REGION --stack-name <stack name i.e. rosa-network-stack-nnnnnnnnnnn>
```

Refer to [OpenShift documentation](https://docs.redhat.com/en/documentation/red_hat_openshift_service_on_aws/4/html/install_clusters/rosa-hcp-deleting-cluster) 
if you'd like to completely remove the Red Hat OpenShift Service from your AWS account. 

