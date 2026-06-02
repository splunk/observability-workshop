---
title: Fix PHP/Apache Issue
linkTitle: 5. Fix PHP/Apache Issue
weight: 5
---
## 1. Kubernetes リソース

特に本番環境の Kubernetes クラスターでは、CPU とメモリは貴重なリソースとみなされます。クラスター運用者は通常、Pod やサービスがデプロイ時に必要とする CPU とメモリの量を指定するよう求めます。これにより、クラスターはどの Node にソリューションを配置するかを自動的に管理できます。

これを実現するには、アプリケーションや Pod のデプロイメントに Resource セクションを記述します。

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

詳細はこちらを参照してください: [**Resource Management for Pods and Containers**](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)

アプリケーションや Pod がデプロイメントに設定された制限を超えた場合、Kubernetes は他のアプリケーションを保護するために Pod を停止して再起動します。

もう 1 つ遭遇するシナリオは、Node に十分なメモリや CPU がない場合です。この場合、クラスターはより多くの空きがある別の Node に Pod を再スケジュールしようとします。

それも失敗した場合、またはアプリケーションのデプロイ時に十分な空きがない場合、クラスターはワークロード/デプロイメントをスケジュール待ちモードにし、利用可能な Node のいずれかに、設定された制限に従って Pod をデプロイできる十分な空きが確保されるまで待機します。

## 2. PHP/Apache デプロイメントの修正

{{% notice title="Workshop Question" style="tip" icon="question" %}}

開始する前に、PHP/Apache デプロイメントの現在の状態を確認しましょう。**Alerts & Detectors** の下で、どの Detector が発火していますか? この情報は他にどこで確認できますか?

{{% /notice %}}

PHP/Apache の StatefulSet を修正するには、次のコマンドで `~/workshop/k3s/php-apache.yaml` を編集して CPU リソースを減らします。

``` bash
vim ~/workshop/k3s/php-apache.yaml
```

resources セクションを見つけて、CPU の limits を **1** に、CPU の requests を **0.5** に減らします。

``` yaml
resources:
  limits:
    cpu: "1"
    memory: "8Mi"
  requests:
    cpu: "0.5"
    memory: "4Mi"
```

変更を保存します。(ヒント: `Esc` の後に `:wq!` で変更を保存します)

次に、既存の StatefulSet を削除して再作成する必要があります。StatefulSet はイミュータブルであるため、既存のものを削除し、新しい変更を反映して再作成する必要があります。

``` bash
kubectl delete statefulset php-apache -n apache
```

それでは、変更をデプロイします。

``` bash
kubectl apply -f ~/workshop/k3s/php-apache.yaml -n apache
```

## 3. 変更の検証

次のコマンドを実行して、変更が適用されたことを検証できます。

``` bash
kubectl describe statefulset php-apache -n apache
```

Splunk Observability Cloud で Pod が稼働していることを確認します。

{{% notice title="Workshop Question" style="tip" icon="question" %}}
**Apache Web Servers** ダッシュボードにデータが表示されていますか?

**ヒント:** フィルターと時間範囲を使ってデータを絞り込むことを忘れないでください。
{{% /notice %}}

Apache Web サーバーの Navigator ダッシュボードを数分間モニタリングします。

{{% notice title="Workshop Question" style="tip" icon="question" %}}

# Hosts reporting チャートでは何が起こっていますか?

{{% /notice %}}

## 4. メモリ問題の修正

Apache ダッシュボードに戻ると、メトリクスが届かなくなっていることに気づくでしょう。別のリソース問題が発生しており、今回はメモリ不足です。次の画像のように StatefulSet を編集してメモリを増やしましょう。

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

{{% notice title="Hint" style="info" icon="exclamation" %}}
`kubectl edit` は `vi` エディターでコンテンツを開きます。`Esc` の後に `:wq!` を入力して変更を保存してください。
{{% /notice %}}

StatefulSet はイミュータブルであるため、既存の Pod を削除し、新しい変更を反映して StatefulSet が再作成するようにします。

``` bash
kubectl delete pod php-apache-0 -n apache
```

次のコマンドを実行して、変更が適用されたことを検証します。

``` bash
kubectl describe statefulset php-apache -n apache
```
