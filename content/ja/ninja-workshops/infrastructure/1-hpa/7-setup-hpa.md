---
title: Horizontal Pod Autoscaling (HPA) のセットアップ
linkTitle: 7. HPA のセットアップ
weight: 7
---

Kubernetesでは、HorizontalPodAutoscalerがワークロードリソース（DeploymentやStatefulSetなど）を自動的に更新し、需要に合わせてワークロードを自動的にスケーリングします。

水平スケーリングとは、負荷の増加に対応してより多くのPodをデプロイすることを意味します。これは垂直スケーリングとは異なります。Kubernetesにおける垂直スケーリングは、ワークロードですでに実行されているPodにより多くのリソース（メモリやCPUなど）を割り当てることを意味します。

負荷が減少し、Podの数が設定された最小値を超えている場合、HorizontalPodAutoscalerはワークロードリソース（Deployment、StatefulSet、またはその他の類似リソース）にスケールダウンするよう指示します。

## 1. HPA のセットアップ

`~/workshop/k3s/hpa.yaml` ファイルを確認し、以下のコマンドで内容を検証します:

``` bash
cat ~/workshop/k3s/hpa.yaml
```

このファイルには、Horizontal Pod Autoscalerの設定が含まれており、`php-apache` デプロイメント用の新しいHPAを作成します。

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

デプロイされると、`php-apache` は平均CPU使用率が50% を超えるか、デプロイメントの平均メモリ使用率が75% を超えると自動スケールします。最小1 Pod、最大4 Podです。

``` text
kubectl apply -f ~/workshop/k3s/hpa.yaml
```

## 2. HPA の検証

``` text
kubectl get hpa -n apache
```

Kubernetesの **Workloads** または **Node Detail** タブに移動し、HPAデプロイメントを確認します。

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}

1. 追加で作成された `php-apache-x` Podはいくつありますか？
2. **Apache web servers (OTel) Navigator** でどのメトリクスが再び大幅に増加しましたか？

{{% /notice %}}

## 3. HPA レプリカ数の増加

`maxReplicas` を8に増やします

``` bash
kubectl edit hpa php-apache -n apache
```

変更を保存します（ヒント: `Esc` を押してから `:wq!` を入力して変更を保存します）。

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}

1. 現在実行中のPodはいくつありますか？

2. 保留中のPodはいくつありますか？

3. なぜ保留中なのですか？

{{% /notice %}}

**おめでとうございます！** ワークショップが完了しました。
