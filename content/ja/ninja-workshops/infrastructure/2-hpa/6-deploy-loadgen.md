---
title: 負荷生成ツールのデプロイ
linkTitle: 6. 負荷生成ツールのデプロイ
weight: 6
---

それでは `php-apache` Pod に対して負荷をかけてみましょう。これを行うには、クライアントとして動作する別の Pod を起動する必要があります。クライアント Pod 内のコンテナは無限ループで動作し、`php-apache` サービスに対して HTTP GET リクエストを送信し続けます。

## 1. loadgen YAML の確認

YAML ファイル `~/workshop/k3s/loadgen.yaml` を確認し、以下のコマンドで内容を検証します。

``` bash
cat ~/workshop/k3s/loadgen.yaml
```

このファイルには負荷生成ツールの設定が含まれており、負荷生成イメージのレプリカを 2 つ持つ新しい ReplicaSet を作成します。

``` yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: loadgen
  labels:
    app: loadgen
spec:
  replicas: 2
  selector:
    matchLabels:
      app: loadgen
  template:
    metadata:
      name: loadgen
      labels:
        app: loadgen
    spec:
      containers:
      - name: infinite-calls
        image: busybox
        command:
        - /bin/sh
        - -c
        - "while true; do wget -q -O- http://php-apache-svc.apache.svc.cluster.local; done"
```

## 2. 新しい namespace を作成する

``` text
kubectl create namespace loadgen
```

## 3. loadgen YAML をデプロイする

``` text
kubectl apply -f ~/workshop/k3s/loadgen.yaml --namespace loadgen
```

負荷生成ツールをデプロイすると、`loadgen` namespace で Pod が稼働している様子を確認できます。これまでと同様のコマンドを使い、コマンドラインから Pod のステータスを確認してください。

{{% notice title="ワークショップの設問" style="tip" icon="question" %}}
Apache Navigator のどのメトリクスが大幅に増加したでしょうか？
{{% /notice %}}

## 4. 負荷生成ツールをスケールする

ReplicaSet は、Pod の複数インスタンスを稼働させ、指定された数の Pod を一定に保つプロセスです。その目的は、クラスター内で指定された数の Pod インスタンスを常に稼働させることで、Pod が障害を起こしたりアクセスできなくなったりした際にユーザーがアプリケーションへアクセスできなくなることを防ぐことにあります。

ReplicaSet は、既存の Pod が障害を起こしたときに新しいインスタンスを立ち上げたり、稼働中のインスタンス数が指定数に満たない場合にスケールアップしたり、同じラベルを持つインスタンスが別途作成された場合に Pod をスケールダウンまたは削除したりすることを支援します。ReplicaSet は、指定された数の Pod レプリカが継続的に稼働していることを保証し、リソース使用率の増加時には負荷分散にも役立ちます。

以下のコマンドで ReplicaSet を 4 レプリカにスケールしてみましょう。

``` text
kubectl scale replicaset/loadgen --replicas 4 -n loadgen
```

コマンドラインと Splunk Observability Cloud の両方から、レプリカが稼働していることを検証してください。

``` text
kubectl get replicaset loadgen -n loadgen
```

![ReplicaSet](../images/k8s-workload-replicaset.png)

{{% notice title="ワークショップの設問" style="tip" icon="question" %}}
Apache Navigator にどのような影響が見られるでしょうか？
{{% /notice %}}

負荷生成ツールを 2〜3 分ほど稼働させ、Kubernetes Navigator と Apache Navigator のメトリクスを継続して観察してください。
