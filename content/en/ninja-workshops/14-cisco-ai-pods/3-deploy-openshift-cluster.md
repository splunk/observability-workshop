---
title: Deploy OpenShift Cluster in AWS
linkTitle: 3. Deploy OpenShift Cluster in AWS
weight: 3
time: 25 minutes
---

## Deploy an OpenShift Cluster 

We'll use the ROSA CLI to deploy an OpenShift Cluster. 

First, we'll need to set a few environment variables: 

> Note: be sure to fill in the Subnet IDs and OIDC ID before running the EXPORT commands

``` bash
export CLUSTER_NAME=rosa-test
export AWS_REGION=us-east-2
export AWS_INSTANCE_TYPE=g5.2xlarge
export SUBNET_IDS=<comma separated list of subnet IDs from earlier rosa create network command>
export OIDC_ID=<the oidc-provider id returned from the rosa create oidc-config command> 
export OPERATOR_ROLES_PREFIX=rosa-test-a6x9
```

Create operator roles for the OIDC configuration using the following command: 

``` bash
rosa create operator-roles --hosted-cp --prefix $OPERATOR_ROLES_PREFIX --oidc-config-id $OIDC_ID
```

Then we can create the cluster as follows: 

``` bash
rosa create cluster \
    --cluster-name=$CLUSTER_NAME \
    --mode=auto \
    --hosted-cp \
    --sts \
    --create-admin-user \
    --oidc-config-id=$OIDC_ID \
    --subnet-ids=$SUBNET_IDS \
    --compute-machine-type $AWS_INSTANCE_TYPE \
    --replicas 2 \
    --region $AWS_REGION
```

> Note that we've specified the `g5.2xlarge` instance type, which includes NVIDIA 
> GPUs that we'll be using later in the workshop.  This instance type is relatively expensive, 
> about $1.21 per hour at the time of writing, and we've requested 2 replicas, 
> so be mindful of how long your cluster is running for, as costs will accumulate quickly.

To determine when your cluster is Ready, run:

``` bash
rosa describe cluster -c $CLUSTER_NAME
```

To watch your cluster installation logs, run:

``` bash
rosa logs install -c $CLUSTER_NAME --watch
```

## Connect to the OpenShift Cluster

Use the command below to connect the oc CLI to your OpenShift cluster: 

> Note: Run the `rosa describe cluster -c $CLUSTER_NAME` command and substitute the
> resulting API Server URL into the command below before running it. For example, 
> the server name might be something like `https://api.rosa-test.aaa.bb.openshiftapps.com:443`.

``` bash
 oc login <API Server URL> -u cluster-admin
```

Once connected to your cluster, confirm that the nodes are up and running: 

``` bash
oc get nodes

NAME                                       STATUS   ROLES    AGE   VERSION
ip-10-0-1-184.us-east-2.compute.internal   Ready    worker   14m   v1.31.11
ip-10-0-1-50.us-east-2.compute.internal    Ready    worker   20m   v1.31.11
```

