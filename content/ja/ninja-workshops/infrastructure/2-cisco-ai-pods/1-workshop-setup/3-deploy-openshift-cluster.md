---
title: AWSにOpenShiftクラスターをデプロイする
linkTitle: 3. AWSにOpenShiftクラスターをデプロイする
weight: 3
time: 25 minutes
---

## OpenShiftクラスターのデプロイ

ROSA CLIを使用してOpenShiftクラスターをデプロイします。

まず、いくつかの環境変数を設定する必要があります。

> [!NOTE]
> EXPORTコマンドを実行する前に、Subnet IDとOIDC IDを必ず入力してください

``` bash
export CLUSTER_NAME=rosa-test
export AWS_REGION=us-east-2
export AWS_INSTANCE_TYPE=g5.4xlarge
export SUBNET_IDS=<comma separated list of subnet IDs from earlier rosa create network command>
export OIDC_ID=<the oidc-provider id returned from the rosa create oidc-config command>
export OPERATOR_ROLES_PREFIX=rosa-test-a6x9
```

次のコマンドを使用して、OIDC構成のオペレーターロールを作成します。

> 注意: プロンプトが表示されたら、デフォルト値をそのまま受け入れてください。

``` bash
rosa create operator-roles --hosted-cp --prefix $OPERATOR_ROLES_PREFIX --oidc-config-id $OIDC_ID
```

次に、以下のようにクラスターを作成します。

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

> ワークショップの後半で使用するNVIDIA GPUを搭載した `g5.4xlarge` インスタンスタイプを指定しています。このインスタンスタイプは比較的高価で、執筆時点で1時間あたり約$1.64です。2つのレプリカを要求しているため、クラスターの稼働時間に注意してください。コストは急速に蓄積されます。

クラスターがReadyになったかどうかを確認するには、次のコマンドを実行します。

``` bash
rosa describe cluster -c $CLUSTER_NAME
```

クラスターのインストールログを監視するには、次のコマンドを実行します。

``` bash
rosa logs install -c $CLUSTER_NAME --watch
```

## OpenShiftクラスターへの接続

以下のコマンドを使用して、oc CLIをOpenShiftクラスターに接続します。

> 注意: `rosa describe cluster -c $CLUSTER_NAME` コマンドを実行し、結果のAPI Server URLを以下のコマンドに代入してから実行してください。例えば、サーバー名は `https://api.rosa-test.aaa.bb.openshiftapps.com:443` のようになります。

``` bash
 oc login <API Server URL> -u cluster-admin
```

クラスターに接続したら、ノードが稼働していることを確認します。

``` bash
oc get nodes

NAME                                       STATUS   ROLES    AGE   VERSION
ip-10-0-1-184.us-east-2.compute.internal   Ready    worker   14m   v1.31.11
ip-10-0-1-50.us-east-2.compute.internal    Ready    worker   20m   v1.31.11
```
