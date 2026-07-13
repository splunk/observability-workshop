---
title: Horizontal Pod Autoscaling (HPA) のセットアップ
linkTitle: 7. HPAのセットアップ
weight: 7
---

Kubernetesでは、HorizontalPodAutoscalerがワークロードリソース（DeploymentやStatefulSetなど）を自動的に更新し、需要に合わせてワークロードを自動的にスケールします。

水平スケーリングとは、負荷の増加に対してより多くのPodをデプロイすることで対応することを意味します。これは垂直スケーリングとは異なり、Kubernetesにおける垂直スケーリングは、ワークロードのために既に実行されているPodにより多くのリソース（例: メモリやCPU）を割り当てることを意味します。

負荷が減少し、Podの数が設定された最小値を超えている場合、HorizontalPodAutoscalerはワークロードリソース（Deployment、StatefulSet、またはその他の類似リソース）にスケールダウンを指示します。

## 1. HPAのセットアップ

`~/workshop/k3s/hpa.yaml` ファイルを確認し、以下のコマンドで内容を検証します。

``` bash
cat ~/workshop/k3s/hpa.yaml
```

このファイルにはHorizontal Pod Autoscalerの設定が含まれており、`php-apache` デプロイメント用の新しいHPAを作成します。

``` yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: php-apache
  namespace: apache
spec:
  maxReplicas: 4
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        averageUtilization: 50
        type: Utilization
  - type: Resource
    resource:
      name: memory
      target:
        averageUtilization: 75
        type: Utilization
  minReplicas: 1
  scaleTargetRef:
    apiVersion: apps/v1
    kind: StatefulSet
    name: php-apache
```

デプロイされると、`php-apache` は平均CPU使用率が50%を超えるか、デプロイメントの平均メモリ使用率が75%を超えた場合にオートスケールします。最小1Pod、最大4Podの範囲でスケールします。

``` text
kubectl apply -f ~/workshop/k3s/hpa.yaml
```

## 2. HPAの検証

``` text
kubectl get hpa -n apache
```

Kubernetesの **Workloads** または **Node Detail** タブに移動し、HPAのデプロイメントを確認します。

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}

1. 追加の `php-apache-x` Podはいくつ作成されましたか？
2. **Apache web servers (OTel) Navigator** のどのメトリクスが再び大幅に増加しましたか？

{{% /notice %}}

## 3. HPAのレプリカ数を増やす

`maxReplicas` を8に増やします。

``` bash
kubectl edit hpa php-apache -n apache
```

変更を保存します（ヒント: `Esc` に続けて `:wq!` を使用して変更を保存します）。

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}

1. 現在いくつのPodが実行されていますか？

2. いくつのPodがpending状態ですか？

3. なぜpending状態なのですか？

{{% /notice %}}

**おめでとうございます！** ワークショップを完了しました。
