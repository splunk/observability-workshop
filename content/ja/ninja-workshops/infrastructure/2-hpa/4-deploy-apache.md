---
title: Deploy Apache
linkTitle: 4. Deploy Apache
weight: 4
---

## 1. PHP/Apache のデプロイメント YAML を確認する

YAML ファイル `~/workshop/k3s/php-apache.yaml` を確認し、以下のコマンドで内容を検証します。

``` bash
cat ~/workshop/k3s/php-apache.yaml
```

 このファイルには PHP/Apache のデプロイメント構成が含まれており、PHP/Apache イメージのレプリカを 1 つ持つ新しい StatefulSet を作成します。

ステートレスなアプリケーションは、使用するネットワークを問わず、永続的なストレージも必要としません。ステートレスアプリの例としては、Apache、Nginx、Tomcat などの Web サーバーが挙げられます。

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

## 2. PHP/Apache をデプロイする

`apache` ネームスペースを作成し、PHP/Apache アプリケーションをクラスターにデプロイします。

`apache` ネームスペースを作成します。

``` bash
kubectl create namespace apache
```

PHP/Apache アプリケーションをデプロイします。

``` bash
kubectl apply -f ~/workshop/k3s/php-apache.yaml -n apache
```

デプロイメントが作成されたことを確認します。

``` bash
kubectl get statefulset -n apache
```

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
**Apache web servers (OTel) Navigator** では、Apache インスタンスに関するどのようなメトリクスがレポートされていますか？
{{% /notice %}}

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
Log Observer を使用して、PHP/Apache デプロイメントの問題点は何ですか？

**ヒント:** フィルターを次のように調整してください: `k8s.namespace.name = apache` および `k8s.cluster.name = <your_cluster>`。
{{% /notice %}}
