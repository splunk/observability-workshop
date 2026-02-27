---
title: 1. Build and Load Images
weight: 1
---

## Verify Your Cluster

Your workshop instance has K3s pre-installed. Confirm it's running:

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl get nodes
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
NAME            STATUS   ROLES                  AGE   VERSION
ip-10-0-1-100   Ready    control-plane,master   12h   v1.31.x+k3s1
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

## Import Images into K3s

K3s uses containerd, not Docker, so images must be exported from Docker and imported:

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
docker save obi-workshop-frontend:latest | sudo k3s ctr images import -
docker save obi-workshop-order-processor:latest | sudo k3s ctr images import -
docker save obi-workshop-payment-service:latest | sudo k3s ctr images import -
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
unpacking docker.io/library/obi-workshop-frontend:latest (sha256:...)...done
unpacking docker.io/library/obi-workshop-order-processor:latest (sha256:...)...done
unpacking docker.io/library/obi-workshop-payment-service:latest (sha256:...)...done
```

{{% /tab %}}
{{< /tabs >}}

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
If you're using **k3d** instead of k3s:

``` bash
k3d image import obi-workshop-frontend:latest obi-workshop-order-processor:latest obi-workshop-payment-service:latest
```

For **kind**:

``` bash
kind load docker-image obi-workshop-frontend:latest obi-workshop-order-processor:latest obi-workshop-payment-service:latest
```

{{% /notice %}}
