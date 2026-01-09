---
title: PHP/Apache の問題の修正
linkTitle: 5. PHP/Apache の問題の修正
weight: 5
---
## 1. Kubernetes リソース

特に本番環境の Kubernetes クラスターでは、CPU とメモリは貴重なリソースと見なされています。クラスター運用者は通常、デプロイメントで Pod またはサービスが必要とする CPU とメモリの量を指定するよう求めます。これにより、クラスターがソリューションを配置するノードを自動的に管理できます。

これは、アプリケーション/Pod のデプロイメントにリソースセクションを配置することで行います。

**例:**

``` yaml
resources:
  limits:         # Maximum amount of CPU & memory for peek use
    cpu: "8"      # Maximum of 8 cores of CPU allowed at for peek use
    memory: "8Mi" # Maximum allowed 8Mb of memory
  requests:       # Request are the expected amount of CPU & memory for normal use
    cpu: "6"      # Requesting 4 cores of a CPU
    memory: "4Mi" # Requesting 4Mb of memory
```

詳細については、こちらを参照してください: [**Resource Management for Pods and Containers**](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)

アプリケーションまたは Pod がデプロイメントで設定された制限を超えると、Kubernetes はクラスター上の他のアプリケーションを保護するために Pod を強制終了して再起動します。

もう1つのシナリオは、ノードに十分なメモリまたは CPU がない場合です。その場合、クラスターはより多くのスペースがある別のノードに Pod を再スケジュールしようとします。

それが失敗した場合、またはアプリケーションをデプロイするときに十分なスペースがない場合、クラスターはワークロード/デプロイメントをスケジュールモードにして、利用可能なノードのいずれかに制限に従って Pod をデプロイするのに十分なスペースができるまで待機します。

## 2. PHP/Apache デプロイメントの修正

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}

開始する前に、PHP/Apache デプロイメントの現在の状態を確認しましょう。**Alerts & Detectors** で、どのディテクターが発火しましたか？この情報は他にどこで見つけることができますか？

{{% /notice %}}

PHP/Apache StatefulSet を修正するには、以下のコマンドを使用して `~/workshop/k3s/php-apache.yaml` を編集し、CPU リソースを削減します:

``` bash
vim ~/workshop/k3s/php-apache.yaml
```

リソースセクションを見つけて、CPU limits を **1** に、CPU requests を **0.5** に削減します:

``` yaml
resources:
  limits:
    cpu: "1"
    memory: "8Mi"
  requests:
    cpu: "0.5"
    memory: "4Mi"
```

変更を保存します（ヒント: `Esc` を押してから `:wq!` を入力して変更を保存します）。

次に、既存の StatefulSet を削除して再作成する必要があります。StatefulSet は不変（イミュータブル）であるため、既存のものを削除して新しい変更で再作成する必要があります。

``` bash
kubectl delete statefulset php-apache -n apache
```

次に、変更をデプロイします:

``` bash
kubectl apply -f ~/workshop/k3s/php-apache.yaml -n apache
```

## 3. 変更の検証

以下のコマンドを実行して、変更が適用されたことを確認できます:

``` bash
kubectl describe statefulset php-apache -n apache
```

Pod が Splunk Observability Cloud で実行中であることを確認します。

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
**Apache Web Servers** ダッシュボードにデータが表示されていますか？

**ヒント:** フィルターと時間枠を使用してデータを絞り込むことを忘れないでください。
{{% /notice %}}

数分間、Apache web servers Navigator ダッシュボードを監視してください。

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
# Hosts reporting チャートでは何が起きていますか？
{{% /notice %}}

## 4. メモリの問題の修正

Apache ダッシュボードに戻ると、メトリクスが送信されなくなっていることに気付くでしょう。別のリソースの問題があり、今回はメモリ不足です。StatefulSet を編集して、以下に示す値にメモリを増やしましょう:

``` bash
kubectl edit statefulset php-apache -n apache
```

``` yaml
resources:
  limits:
    cpu: "1"
    memory: 16Mi
  requests:
    cpu: 500m
    memory: 12Mi
```

変更を保存します。

{{% notice title="ヒント" style="info" icon="exclamation" %}}
`kubectl edit` は内容を `vi` エディターで開きます。`Esc` を押してから `:wq!` を入力して変更を保存します。
{{% /notice %}}

StatefulSet は不変（イミュータブル）であるため、既存の Pod を削除して、StatefulSet が新しい変更で再作成できるようにする必要があります。

``` bash
kubectl delete pod php-apache-0 -n apache
```

以下のコマンドを実行して、変更が適用されたことを確認します:

``` bash
kubectl describe statefulset php-apache -n apache
```
