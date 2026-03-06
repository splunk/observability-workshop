---
title: クリーンアップ
linkTitle: 10. クリーンアップ
weight: 10
time: 5 minutes
---

## クリーンアップ手順

ワークショップが完了したら、このセクションの手順に従って OpenShift クラスターをアンインストールします。

以下のコマンドを実行して、クラスター ID、クラスター固有の Operator ロールの Amazon Resource Names（ARN）、および OIDC プロバイダーのエンドポイント URL を取得します。

``` bash
rosa describe cluster --cluster=$CLUSTER_NAME
```

以下のコマンドを使用してクラスターを削除します。

``` bash
rosa delete cluster --cluster=$CLUSTER_NAME --watch
```

クラスター固有の Operator IAM ロールを削除します。

> 注意: プロンプトが表示されたら、デフォルト値をそのまま受け入れてください。

``` bash
rosa delete operator-roles --prefix $OPERATOR_ROLES_PREFIX
```

OIDC プロバイダーを削除します。

> 注意: プロンプトが表示されたら、デフォルト値をそのまま受け入れてください。

``` bash
rosa delete oidc-provider --oidc-config-id $OIDC_ID
```

ネットワークを削除します。

> 注意: 以下のコマンドを実行する前に、ネットワークの作成に使用した CloudFormation スタックの名前を追加してください。

``` bash
aws cloudformation delete-stack --region $AWS_REGION --stack-name <stack name i.e. rosa-network-stack-nnnnnnnnnnn>
```

AWS アカウントから Red Hat OpenShift Service を完全に削除したい場合は、[OpenShift のドキュメント](https://docs.redhat.com/en/documentation/red_hat_openshift_service_on_aws/4/html/install_clusters/rosa-hcp-deleting-cluster)を参照してください。
