---
title: 1. イメージのビルドとロード
weight: 1
---

## クラスターの確認

ワークショップインスタンスには K3d がプリインストールされています。動作していることを確認します。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl get nodes
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
NAME                            STATUS   ROLES                  AGE    VERSION
k3d-shw-ece9-cluster-agent-0    Ready    <none>                 4h6m   v1.33.4+k3s1
k3d-shw-ece9-cluster-agent-1    Ready    <none>                 4h6m   v1.33.4+k3s1
k3d-shw-ece9-cluster-server-0   Ready    control-plane,master   4h6m   v1.33.4+k3s1
```

{{% /tab %}}
{{< /tabs >}}

## アプリケーションイメージのビルド

K8s マニフェストはローカルでビルドしたイメージを参照します。`02-obi-docker/` のソースからビルドします。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
cd ~/workshop/obi/03-obi-k8s
docker build -t obi-workshop-frontend:latest ../02-obi-docker/frontend
docker build -t obi-workshop-order-processor:latest ../02-obi-docker/order-processor
docker build -t obi-workshop-payment-service:latest ../02-obi-docker/payment-service
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
[+] Building 8.2s (10/10) FINISHED
 => => naming to docker.io/library/obi-workshop-frontend:latest
[+] Building 12.1s (11/11) FINISHED
 => => naming to docker.io/library/obi-workshop-order-processor:latest
[+] Building 11.8s (11/11) FINISHED
 => => naming to docker.io/library/obi-workshop-payment-service:latest
```

{{% /tab %}}
{{< /tabs >}}

## イメージを K3d にインポート

K3d は Docker ではなく containerd を使用するため、イメージをクラスターにインポートする必要があります。まず、クラスター名を確認します。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
k3d cluster list
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
NAME               SERVERS   AGENTS   LOADBALANCER
shw-ece9-cluster   1/1       2/2      true
```

{{% /tab %}}
{{< /tabs >}}

次にイメージをインポートします。`CLUSTER_NAME` は `env` で利用可能になっているはずですが、設定されていない場合は次を実行してください。

```
export CLUSTER_NAME=$(k3d cluster list -o json |  jq -r '.[].name')
```

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
k3d image import -c $CLUSTER_NAME \
  obi-workshop-frontend:latest \
  obi-workshop-order-processor:latest \
  obi-workshop-payment-service:latest
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
INFO[0000] Importing image(s) into cluster 'shw-ece9-cluster'
INFO[0000] Starting new tools node...
INFO[0000] Starting node 'k3d-shw-ece9-cluster-tools'
INFO[0000] Saving 3 image(s) from runtime...
INFO[0003] Importing images into nodes...
INFO[0003] Importing images from tarball '/k3d/images/k3d-shw-ece9-cluster-images-20260227211818.tar' into node 'k3d-shw-ece9-cluster-server-0'...
INFO[0003] Importing images from tarball '/k3d/images/k3d-shw-ece9-cluster-images-20260227211818.tar' into node 'k3d-shw-ece9-cluster-agent-1'...
INFO[0003] Importing images from tarball '/k3d/images/k3d-shw-ece9-cluster-images-20260227211818.tar' into node 'k3d-shw-ece9-cluster-agent-0'...
INFO[0015] Removing the tarball(s) from image volume...
INFO[0016] Removing k3d-tools node...
INFO[0020] Successfully imported image(s)
INFO[0020] Successfully imported 3 image(s) into 1 cluster(s)
```

{{% /tab %}}
{{< /tabs >}}

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
上記のスクリプトはクラスター名を自動検出します。複数の k3d クラスターがある場合は、明示的に指定できます。

``` bash
k3d image import -c shw-ece9-cluster obi-workshop-frontend:latest obi-workshop-order-processor:latest obi-workshop-payment-service:latest
```

{{% /notice %}}
