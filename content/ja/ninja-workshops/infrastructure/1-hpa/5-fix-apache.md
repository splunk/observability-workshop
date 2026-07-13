---
title: PHP/Apacheの問題を修正する
linkTitle: 5. PHP/Apacheの問題を修正する
weight: 5
---
## 1. Kubernetesリソース

特に本番環境のKubernetesクラスターでは、CPUとメモリは貴重なリソースと見なされます。クラスターオペレーターは通常、デプロイメントでPodやサービスが必要とするCPUとメモリの量を指定するよう求めます。これにより、クラスターがソリューションを配置するノードを自動的に管理できるようになります。

これは、アプリケーション/Podのデプロイメントにリソースセクションを配置することで行います。

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

アプリケーションやPodがデプロイメントで設定されたリミットを超えると、Kubernetesはクラスター上の他のアプリケーションを保護するためにPodを強制終了して再起動します。

もう1つのシナリオは、ノード上に十分なメモリやCPUがない場合です。その場合、クラスターはより空きのある別のノードにPodを再スケジュールしようとします。

それが失敗した場合、またはアプリケーションのデプロイ時に十分な空きがない場合、クラスターは利用可能なノードのいずれかにリミットに従ってPodをデプロイするのに十分な空きができるまで、ワークロード/デプロイメントをスケジュールモードにします。

## 2. PHP/Apacheデプロイメントの修正

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}

開始する前に、PHP/Apacheデプロイメントの現在のステータスを確認しましょう。 **Alerts & Detectors** の下で、どのディテクターが発火しましたか？この情報は他にどこで確認できますか？

{{% /notice %}}

PHP/Apache StatefulSetを修正するには、以下のコマンドを使用して `~/workshop/k3s/php-apache.yaml` を編集し、CPUリソースを減らします。

``` bash
vim ~/workshop/k3s/php-apache.yaml
```

リソースセクションを見つけて、CPUリミットを **1** に、CPUリクエストを **0.5** に減らします。

``` yaml
resources:
  limits:
    cpu: "1"
    memory: "8Mi"
  requests:
    cpu: "0.5"
    memory: "4Mi"
```

変更を保存します（ヒント: `Esc` に続いて `:wq!` で変更を保存します）。

次に、既存のStatefulSetを削除して再作成する必要があります。StatefulSetはイミュータブルなため、既存のものを削除して新しい変更で再作成する必要があります。

``` bash
kubectl delete statefulset php-apache -n apache
```

変更をデプロイします。

``` bash
kubectl apply -f ~/workshop/k3s/php-apache.yaml -n apache
```

## 3. 変更の検証

以下のコマンドを実行して、変更が適用されたことを検証できます。

``` bash
kubectl describe statefulset php-apache -n apache
```

Splunk Observability CloudでPodが実行中であることを確認します。

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
**Apache Web Servers** ダッシュボードにデータが表示されていますか？

**ヒント:** フィルターと時間範囲を使用してデータを絞り込むことを忘れないでください。
{{% /notice %}}

Apache Web Servers Navigatorダッシュボードを数分間モニタリングします。

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}

# Hosts reportingチャートに何が起きていますか？

{{% /notice %}}

## 4. メモリの問題を修正する

Apacheダッシュボードに戻ると、メトリクスが送信されなくなっていることに気づくでしょう。別のリソースの問題があり、今回はメモリ不足（Out of Memory）です。StatefulSetを編集して、以下のイメージに示されている値にメモリを増やしましょう。

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
`kubectl edit` は `vi` エディタで内容を開きます。 `Esc` に続いて `:wq!` で変更を保存します。
{{% /notice %}}

StatefulSetはイミュータブルなため、既存のPodを削除して、StatefulSetに新しい変更で再作成させる必要があります。

``` bash
kubectl delete pod php-apache-0 -n apache
```

以下のコマンドを実行して、変更が適用されたことを検証します。

``` bash
kubectl describe statefulset php-apache -n apache
```
