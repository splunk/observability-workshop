---
title: Deploy OpenShift Cluster in AWS
linkTitle: 3. Deploy OpenShift Cluster in AWS
weight: 3
time: 25 minutes
---

## Deploy an OpenShift Cluster 

You can run `rosa create cluster` and provide the details when prompted. 

Alternatively, you can modify the following command and then execute it 
to begin the cluster deployment process: 

``` bash
rosa create cluster \
    --cluster-name rosa-test \
    --sts \
    --create-admin-user \
    --role-arn arn:aws:iam::<AWS Account>>:role/ManagedOpenShift-HCP-ROSA-Installer-Role \
    --support-role-arn arn:aws:iam::<AWS Account>:role/ManagedOpenShift-HCP-ROSA-Support-Role \
    --worker-iam-role arn:aws:iam::<AWS Account>:role/ManagedOpenShift-HCP-ROSA-Worker-Role \
    --operator-roles-prefix rosa-test-s4f8 \
    --oidc-config-id <OIDC Config ID> \
    --region us-east-2 \
    --version 4.18.23 \
    --ec2-metadata-http-tokens optional \
    --replicas 2 \
    --compute-machine-type m5.xlarge \
    --machine-cidr 10.0.0.0/16 \
    --service-cidr 172.30.0.0/16 \
    --pod-cidr 10.128.0.0/14 \
    --host-prefix 23 \
    --subnet-ids <subnet IDs>> \
    --hosted-cp \
    --additional-compute-security-group-ids <security group ID> \
    --billing-account <AWS Account>
```

Run the following commands to continue the cluster creation:

``` bash
rosa create operator-roles --cluster rosa-test
```

To determine when your cluster is Ready, run:

``` bash
rosa describe cluster -c rosa-test
```

To watch your cluster installation logs, run:

``` bash
rosa logs install -c rosa-test --watch
```

## Connect to the OpenShift Cluster

``` bash
 oc login -u cluster-admin
```

When prompted, specify the server name for your OpenShift cluster, which you can find with the 
`rosa describe cluster -c rosa-test` command. For example, the server name might be something like 
`https://api.rosa-test.aaa.bb.openshiftapps.com:443`. 

Once connected to your cluster, confirm that the nodes are up and running: 

``` bash
oc get nodes

NAME                                       STATUS   ROLES    AGE   VERSION
ip-10-0-1-184.us-east-2.compute.internal   Ready    worker   14m   v1.31.11
ip-10-0-1-50.us-east-2.compute.internal    Ready    worker   20m   v1.31.11
```

