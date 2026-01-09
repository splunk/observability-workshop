---
title: Apache のデプロイ
linkTitle: 4. Apache のデプロイ
weight: 4
---

## 1. PHP/Apache デプロイメント YAML の確認

YAML ファイル `~/workshop/k3s/php-apache.yaml` を確認し、以下のコマンドで内容を検証します:

``` bash
cat ~/workshop/k3s/php-apache.yaml
```

このファイルには、PHP/Apache デプロイメントの設定が含まれており、PHP/Apache イメージの単一レプリカを持つ新しい StatefulSet を作成します。

ステートレスアプリケーションは、どのネットワークを使用しているかを気にせず、永続ストレージを必要としません。ステートレスアプリの例としては、Apache、Nginx、Tomcat などの Web サーバーがあります。

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: php-apache
spec:
  updateStrategy:
    type: RollingUpdate
  selector:
    matchLabels:
      run: php-apache
  serviceName: "php-apache-svc"
  replicas: 1
  template:
    metadata:
      labels:
        run: php-apache
    spec:
      containers:
      - name: php-apache
        image: ghcr.io/splunk/php-apache:latest
        ports:
        - containerPort: 80
        resources:
          limits:
            cpu: "8"
            memory: "8Mi"
          requests:
            cpu: "6"
            memory: "4Mi"

---
apiVersion: v1
kind: Service
metadata:
  name: php-apache-svc
  labels:
    run: php-apache
spec:
  ports:
  - port: 80
  selector:
    run: php-apache
```

## 2. PHP/Apache のデプロイ

`apache` Namespace を作成し、PHP/Apache アプリケーションをクラスターにデプロイします。

`apache` Namespace を作成します:

``` bash
kubectl create namespace apache
```

PHP/Apache アプリケーションをデプロイします:

``` bash
kubectl apply -f ~/workshop/k3s/php-apache.yaml -n apache
```

デプロイメントが作成されたことを確認します:

``` bash
kubectl get statefulset -n apache
```

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
**Apache web servers (OTel) Navigator** で、Apache インスタンスのどのメトリクスが報告されていますか？
{{% /notice %}}

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
Log Observer を使用して、PHP/Apache デプロイメントの問題は何ですか？

**ヒント:** フィルターを調整して、`k8s.namespace.name = apache` および `k8s.cluster.name = <your_cluster>` を使用してください。
{{% /notice %}}
