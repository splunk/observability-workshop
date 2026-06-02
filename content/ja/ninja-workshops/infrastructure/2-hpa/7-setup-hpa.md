---
title: Setup Horizontal Pod Autoscaling (HPA)
linkTitle: 7. Setup HPA
weight: 7
---

Kubernetes において、HorizontalPodAutoscaler はワークロードリソース（Deployment や StatefulSet など）を自動的に更新し、需要に合わせてワークロードを自動スケールさせます。

水平スケーリングとは、負荷の増加に対してより多くの Pod をデプロイすることで対応することを意味します。これは垂直スケーリングとは異なります。Kubernetes における垂直スケーリングとは、ワークロード用にすでに稼働している Pod により多くのリソース（メモリや CPU など）を割り当てることを指します。

負荷が減少し、Pod の数が設定された最小値を上回っている場合、HorizontalPodAutoscaler はワークロードリソース（Deployment、StatefulSet、またはその他の類似リソース）にスケールダウンするよう指示します。

## 1. Setup HPA

`~/workshop/k3s/hpa.yaml` ファイルを確認し、次のコマンドで内容を検証します:

``` bash
cat ~/workshop/k3s/hpa.yaml
```

このファイルには Horizontal Pod Autoscaler の設定が含まれており、`php-apache` デプロイメント用に新しい HPA を作成します。

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

デプロイされると、`php-apache` は平均 CPU 使用率が 50% を超えるか、デプロイメントの平均メモリ使用率が 75% を超えた場合に、最小 1 Pod から最大 4 Pod の範囲で自動スケールします。

``` text
kubectl apply -f ~/workshop/k3s/hpa.yaml
```

## 2. Validate HPA

``` text
kubectl get hpa -n apache
```

Kubernetes の **Workloads** または **Node Detail** タブに移動し、HPA のデプロイメントを確認します。

{{% notice title="Workshop Questions" style="tip" icon="question" %}}

1. 追加で作成された `php-apache-x` Pod はいくつありますか？
2. **Apache web servers (OTel) Navigator** のどのメトリクスが再び大幅に増加しましたか？

{{% /notice %}}

## 3. Increase the HPA replica count

`maxReplicas` を 8 に増やします。

``` bash
kubectl edit hpa php-apache -n apache
```

変更を保存します。（ヒント: `Esc` を押した後 `:wq!` で変更を保存します）。

{{% notice title="Workshop Questions" style="tip" icon="question" %}}

1. 現在いくつの Pod が稼働していますか？

2. いくつの Pod が pending 状態ですか？

3. なぜ pending 状態なのですか？

{{% /notice %}}

**Congratulations!** ワークショップは完了です。
