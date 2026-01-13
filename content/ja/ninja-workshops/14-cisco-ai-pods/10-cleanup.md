---
title: まとめ
linkTitle: 10. まとめ
weight: 10
time: 5 minutes
---

## まとめ

このワークショップをお楽しみいただけたことを願っています。このワークショップでは、Splunk Observability CloudでCisco AI PODsを監視するために使用されるいくつかの技術をデプロイして操作するハンズオン体験を提供しました。具体的には、以下の機会がありました：

* GPUベースのワーカーノードを持つRedHat OpenShiftクラスターのデプロイ。
* NVIDIA NIM OperatorとNVIDIA GPU Operatorのデプロイ。
* NVIDIA NIMを使用してLarge Language Models (LLMs)をクラスターにデプロイ。
* Red Hat OpenShiftクラスターにOpenTelemetry Collectorをデプロイ。
* インフラストラクチャメトリクスを取り込むためにコレクターにPrometheusレシーバーを追加。
* Weaviateベクトルデータベースをクラスターにデプロイ。
* Large Language Models (LLMs)と連携するPythonサービスをOpenTelemetryで計装。
* LLMと連携するアプリケーションからOpenTelemetryがトレースでキャプチャする詳細を理解。

## クリーンアップ手順

このセクションの手順に従って、OpenShiftクラスターをアンインストールします。

以下のコマンドを実行して、クラスターID、クラスター固有のOperatorロール用のAmazon Resource Names (ARNs)、およびOIDCプロバイダーのエンドポイントURLを取得します：

``` bash
rosa describe cluster --cluster=$CLUSTER_NAME
```

以下のコマンドを使用してクラスターを削除します：

``` bash
rosa delete cluster --cluster=$CLUSTER_NAME --watch
```

クラスター固有のOperator IAMロールを削除します：

> 注意: プロンプトが表示されたら、デフォルト値をそのまま使用してください。

``` bash
rosa delete operator-roles --prefix $OPERATOR_ROLES_PREFIX
```

OIDCプロバイダーを削除します：

> 注意: プロンプトが表示されたら、デフォルト値をそのまま使用してください。

``` bash
rosa delete oidc-provider --oidc-config-id $OIDC_ID
```

ネットワークを削除します：

> 注意: 以下のコマンドを実行する前に、ネットワークの作成に使用したCloudFormationスタックの名前を追加してください

``` bash
aws cloudformation delete-stack --region $AWS_REGION --stack-name <stack name i.e. rosa-network-stack-nnnnnnnnnnn>
```

Red Hat OpenShift ServiceをAWSアカウントから完全に削除したい場合は、[OpenShiftドキュメント](https://docs.redhat.com/en/documentation/red_hat_openshift_service_on_aws/4/html/install_clusters/rosa-hcp-deleting-cluster)を参照してください。
