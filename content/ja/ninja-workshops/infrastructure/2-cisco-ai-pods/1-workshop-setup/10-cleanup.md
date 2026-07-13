---
title: クリーンアップ
linkTitle: 10. クリーンアップ
weight: 10
time: 5 minutes
---

## クリーンアップ手順

ワークショップが完了したら、このセクションの手順に従ってOpenShiftクラスターをアンインストールします。

以下のコマンドを実行して、クラスターID、クラスター固有のOperatorロールのAmazon Resource Names（ARN）、およびOIDCプロバイダーのエンドポイントURLを取得します。

``` bash
rosa describe cluster --cluster=$CLUSTER_NAME
```

以下のコマンドを使用してクラスターを削除します。

``` bash
rosa delete cluster --cluster=$CLUSTER_NAME --watch
```

クラスター固有のOperator IAMロールを削除します。

> 注意: プロンプトが表示されたら、デフォルト値をそのまま受け入れてください。

``` bash
rosa delete operator-roles --prefix $OPERATOR_ROLES_PREFIX
```

OIDCプロバイダーを削除します。

> 注意: プロンプトが表示されたら、デフォルト値をそのまま受け入れてください。

``` bash
rosa delete oidc-provider --oidc-config-id $OIDC_ID
```

ネットワークを削除します。

> 注意: 以下のコマンドを実行する前に、ネットワークの作成に使用したCloudFormationスタックの名前を追加してください。

``` bash
aws cloudformation delete-stack --region $AWS_REGION --stack-name <stack name i.e. rosa-network-stack-nnnnnnnnnnn>
```

AWSアカウントからRed Hat OpenShift Serviceを完全に削除したい場合は、[OpenShiftドキュメント](https://docs.redhat.com/en/documentation/red_hat_openshift_service_on_aws/4/html/install_clusters/rosa-hcp-deleting-cluster)を参照してください。
