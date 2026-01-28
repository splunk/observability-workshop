---
title: ロードジェネレーターのデプロイ
linkTitle: 6. ロードジェネレーターのデプロイ
weight: 6
---

それでは、`php-apache` Pod に負荷をかけてみましょう。これを行うには、クライアントとして動作する別の Pod を起動する必要があります。クライアント Pod 内のコンテナは無限ループで実行され、`php-apache` サービスに HTTP GET を送信し続けます。

## 1. loadgen YAML の確認

YAML ファイル `~/workshop/k3s/loadgen.yaml` を確認し、以下のコマンドで内容を検証します:

``` bash
cat ~/workshop/k3s/loadgen.yaml
```

このファイルには、ロードジェネレーターの設定が含まれており、ロードジェネレーターイメージの2つのレプリカを持つ新しい ReplicaSet を作成します。

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

## 2. 新しい Namespace の作成

``` text
kubectl create namespace loadgen
```

## 3. loadgen YAML のデプロイ

``` text
kubectl apply -f ~/workshop/k3s/loadgen.yaml --namespace loadgen
```

ロードジェネレーターをデプロイすると、`loadgen` Namespace で Pod が実行されているのを確認できます。以前と同様のコマンドを使用して、コマンドラインから Pod のステータスを確認してください。

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
Apache Navigator でどのメトリクスが大幅に増加しましたか？
{{% /notice %}}

## 4. ロードジェネレーターのスケール

ReplicaSet は、Pod の複数のインスタンスを実行し、指定された数の Pod を一定に保つプロセスです。その目的は、Pod が失敗したりアクセスできなくなったりした場合でも、ユーザーがアプリケーションにアクセスできなくならないように、クラスター内で指定された数の Pod インスタンスが常に実行されている状態を維持することです。

ReplicaSet は、既存の Pod が失敗した場合に新しいインスタンスを起動し、実行中のインスタンスが指定された数に達していない場合にスケールアップし、同じラベルを持つ別のインスタンスが作成された場合に Pod をスケールダウンまたは削除するのに役立ちます。ReplicaSet は、指定された数の Pod レプリカが継続的に実行されることを保証し、リソース使用量が増加した場合の負荷分散に役立ちます。

以下のコマンドを使用して、ReplicaSet を 4 レプリカにスケールしましょう:

``` text
kubectl scale replicaset/loadgen --replicas 4 -n loadgen
```

コマンドラインと Splunk Observability Cloud の両方からレプリカが実行されていることを確認します:

``` text
kubectl get replicaset loadgen -n loadgen
```

![ReplicaSet](../images/k8s-workload-replicaset.png)

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
Apache Navigator でどのような影響が見られますか？
{{% /notice %}}

ロードジェネレーターを約2〜3分間実行し、Kubernetes Navigator と Apache Navigator でメトリクスを観察し続けてください。
