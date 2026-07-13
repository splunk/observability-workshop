---
title: Portworx Metrics Endpointのデプロイ
linkTitle: 9. Portworx Metrics Endpoint
weight: 9
time: 10 minutes
---

このステップでは、Portworx Metrics Endpointを模倣するPythonサービスをデプロイします。
これはワークショップでPure Storageのモニタリングを設定するために使用されます。

## Portworx Metrics Endpointのデプロイ

以下のコマンドを実行して、Portworx Metrics Endpointサービスをデプロイします。

``` bash
oc new-project portworx
oc apply -f ./portworx/k8s.yaml -n portworx
```

## Portworx Metrics Endpointのテスト

Portworx Metrics Endpointが期待通りに動作していることを確認します。

curlコマンドにアクセスできるPodを起動します。

``` bash
oc run --rm -it -n default curl --image=curlimages/curl:latest -- sh
```

次に、以下のコマンドを実行してエンドポイントにプロンプトを送信します。

{{< tabs >}}
{{% tab title="スクリプト" %}}

``` bash
curl http://portworx-metrics-sim.portworx:17001/metrics
```

{{% /tab %}}
{{% tab title="出力例" %}}

``` bash
# HELP px_cluster_cpu_percent Percentage of CPU Used
# TYPE px_cluster_cpu_percent gauge
px_cluster_cpu_percent{cluster="ocp-pxclus-32430549-ad99-4839-bf9b-d6beb8ddc2d6",clusterUUID="e870909b-6150-4d72-87cb-a012630e42ae",node="worker2.flashstack.local",nodeID="f63312a2-0884-4878-be4e-51935613aa80"} 1.91
...
```

{{% /tab %}}
{{< /tabs >}}
