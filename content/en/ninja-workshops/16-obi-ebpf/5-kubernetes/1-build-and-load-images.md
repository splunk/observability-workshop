---
title: 1. Build and Load Images
weight: 1
---

## Verify Your Cluster

Your workshop instance has K3d pre-installed. Confirm it's running:

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

## Build the Application Images

The K8s manifests reference locally-built images. Build them from the `02-obi-docker/` source:

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

## Import Images into K3d

K3d uses containerd, not Docker, so images must be imported into the cluster. First, find your cluster name:

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

Now import the images, replacing `<YOUR_CLUSTER>` with the name from the output above:

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
CLUSTER_NAME=$(k3d cluster list -o json | jq -r '.[0].name')
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
The script above automatically detects your cluster name. If you have multiple k3d clusters, you can specify it explicitly:

``` bash
k3d image import -c shw-ece9-cluster obi-workshop-frontend:latest obi-workshop-order-processor:latest obi-workshop-payment-service:latest
```

{{% /notice %}}