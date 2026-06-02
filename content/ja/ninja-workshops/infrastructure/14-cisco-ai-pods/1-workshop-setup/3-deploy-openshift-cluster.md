---
title: AWS への OpenShift クラスターのデプロイ
linkTitle: 3. AWS への OpenShift クラスターのデプロイ
weight: 3
time: 25 minutes
---

## OpenShift クラスターのデプロイ

ROSA CLI を使って OpenShift クラスターをデプロイします。

まず、いくつかの環境変数を設定する必要があります。

> 注意: EXPORT コマンドを実行する前に、Subnet ID と OIDC ID を必ず記入してください。

``` bash
export CLUSTER_NAME=rosa-test
export AWS_REGION=us-east-2
export AWS_INSTANCE_TYPE=g5.4xlarge
export SUBNET_IDS=<comma separated list of subnet IDs from earlier rosa create network command>
export OIDC_ID=<the oidc-provider id returned from the rosa create oidc-config command> 
export OPERATOR_ROLES_PREFIX=rosa-test-a6x9
```

次のコマンドで、OIDC 構成用のオペレーターロールを作成します。

> 注意: プロンプトが表示されたら、デフォルト値をそのまま受け入れてください。

``` bash
rosa create operator-roles --hosted-cp --prefix $OPERATOR_ROLES_PREFIX --oidc-config-id $OIDC_ID
```

続いて、以下のようにクラスターを作成します。

``` bash
rosa create cluster \
    --cluster-name $CLUSTER_NAME \
    --mode auto \
    --hosted-cp \
    --sts \
    --create-admin-user \
    --operator-roles-prefix $OPERATOR_ROLES_PREFIX \
    --oidc-config-id $OIDC_ID \
    --subnet-ids $SUBNET_IDS \
    --compute-machine-type $AWS_INSTANCE_TYPE \
    --replicas 2 \
    --region $AWS_REGION \
    --tags "splunkit_environment_type:non-prd,splunkit_data_classification:private"
```

> ここでは `g5.4xlarge` インスタンスタイプを指定しています。これにはワークショップの後半で使用する NVIDIA
> GPU が含まれています。このインスタンスタイプは比較的高価で、執筆時点で 1 時間あたり約 $1.64 です。
> さらに 2 つのレプリカを要求しているため、コストが急速に積み上がる点に注意して、
> クラスターの稼働時間を意識してください。

クラスターが Ready になったかどうかを確認するには、次を実行します。

``` bash
rosa describe cluster -c $CLUSTER_NAME
```

クラスターのインストールログを監視するには、次を実行します。

``` bash
rosa logs install -c $CLUSTER_NAME --watch
```

## OpenShift クラスターへの接続

以下のコマンドを使用して、oc CLI を OpenShift クラスターに接続します。

> 注意: `rosa describe cluster -c $CLUSTER_NAME` コマンドを実行し、結果として得られた
> API Server URL を以下のコマンドに置き換えてから実行してください。例えば、
> サーバー名は `https://api.rosa-test.aaa.bb.openshiftapps.com:443` のような形式になります。

``` bash
 oc login <API Server URL> -u cluster-admin
```

クラスターに接続したら、ノードが起動して動作していることを確認します。

``` bash
oc get nodes

NAME                                       STATUS   ROLES    AGE   VERSION
ip-10-0-1-184.us-east-2.compute.internal   Ready    worker   14m   v1.31.11
ip-10-0-1-50.us-east-2.compute.internal    Ready    worker   20m   v1.31.11
```
