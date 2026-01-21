---
title: Clean Up
linkTitle: 10. Clean Up
weight: 10
time: 5 minutes
---

## Clean Up Steps

Once the workshop is complete, follow the steps in this section to uninstall the OpenShift cluster.

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

