---
title: Load Generatorのデプロイ
linkTitle: 6. Load Generatorのデプロイ
weight: 6
---

`php-apache` Podに負荷をかけてみましょう。これを行うには、クライアントとして動作する別のPodを起動する必要があります。クライアントPod内のコンテナは無限ループで実行され、`php-apache`サービスにHTTP GETリクエストを送信し続けます。

## 1. loadgen YAMLの確認

以下のコマンドを使用して、YAMLファイル `~/workshop/k3s/loadgen.yaml` の内容を確認します。

``` bash
cat ~/workshop/k3s/loadgen.yaml
```

このファイルにはLoad Generatorの設定が含まれており、Load Generatorイメージのレプリカを2つ持つ新しいReplicaSetを作成します。

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

## 2. 新しいnamespaceの作成

``` text
kubectl create namespace loadgen
```

## 3. loadgen YAMLのデプロイ

``` text
kubectl apply -f ~/workshop/k3s/loadgen.yaml --namespace loadgen
```

Load Generatorをデプロイすると、`loadgen` namespaceでPodが実行されていることを確認できます。以前使用した同様のコマンドを使って、コマンドラインからPodのステータスを確認します。

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
Apache Navigatorでどのメトリクスが大幅に増加しましたか？
{{% /notice %}}

## 4. Load Generatorのスケール

ReplicaSetは、Podの複数インスタンスを実行し、指定された数のPodを一定に保つプロセスです。その目的は、Podが障害を起こしたりアクセス不能になったりした場合に、ユーザーがアプリケーションにアクセスできなくなることを防ぐため、クラスター内で常に指定された数のPodインスタンスを実行し続けることです。

ReplicaSetは、既存のPodが障害を起こした場合に新しいインスタンスを起動し、実行中のインスタンスが指定された数に満たない場合にスケールアップし、同じラベルを持つ別のインスタンスが作成された場合にPodをスケールダウンまたは削除します。ReplicaSetは、指定された数のPodレプリカが継続的に実行されることを保証し、リソース使用量が増加した場合の負荷分散に役立ちます。

以下のコマンドを使用して、ReplicaSetを4レプリカにスケールします。

``` text
kubectl scale replicaset/loadgen --replicas 4 -n loadgen
```

コマンドラインとSplunk Observability Cloudの両方からレプリカが実行されていることを確認します。

``` text
kubectl get replicaset loadgen -n loadgen
```

![ReplicaSet](../images/k8s-workload-replicaset.png)

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
Apache Navigatorでどのような影響が見られますか？
{{% /notice %}}

Load Generatorを約2〜3分間実行し続け、Kubernetes NavigatorとApache Navigatorでメトリクスを観察し続けてください。
