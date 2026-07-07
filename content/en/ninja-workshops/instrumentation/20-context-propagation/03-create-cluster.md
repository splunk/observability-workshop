---
title: Create Cluster
linkTitle: 03. Create Cluster
weight: 3
time: 15 minutes

---
In this step, you'll create a lightweight Kubernetes cluster using k3d with a local container registry for workshop images.

Our setup script creates:

- A single server k3d cluster named `cosmic-shop`
- A local Docker registry on port **5111** for pushing workshop images
- NodePort mappings for the shop UI (**30080**) and RabbitMQ management UI (**15672**)

## Create the Cluster

From the project root:

{{< tabs >}}
{{% tab title="Script" %}}

```bash
make setup-k3d
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
Creating k3d cluster 'cosmic-shop' with local registry on port 5111...
...
k3d cluster 'cosmic-shop' ready.
```

{{% /tab %}}
{{< /tabs >}}

## Validation Checklist

#### 1. Confirm k3d cluster exists

{{< tabs >}}
{{% tab title="Script" %}}

```bash
k3d cluster list
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```
NAME         SERVERS   AGENTS   LOADBALANCER
cosmic-shop   1/1       1/1      true
```
{{% /tab %}}
{{< /tabs >}}

#### 2. Confirm Kubernetes is reachable

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl cluster-info
kubectl get nodes
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```
Kubernetes control plane is running at https://0.0.0.0:6443
...

NAME                       STATUS   ROLES                  AGE   VERSION
k3d-cosmic-shop-server-0   Ready    control-plane,master   45s   v1.28.x+k3s1
k3d-cosmic-shop-agent-0    Ready    <none>                 40s   v1.28.x+k3s1
```

All nodes must show `Ready` in the STATUS column.

{{% /tab %}}
{{< /tabs >}}

#### 3. Confirm k3d containers are running

{{< tabs >}}
{{% tab title="Script" %}}

```bash
docker ps --filter name=k3d-cosmic-shop --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` 
NAMES                     STATUS          PORTS
k3d-cosmic-shop-serverlb  Up 2 minutes    0.0.0.0:30080->30080/tcp, 0.0.0.0:15672->15672/tcp, ...
k3d-cosmic-shop-server-0  Up 2 minutes
k3d-cosmic-shop-agent-0   Up 2 minutes
```

You should see the load balancer exposing ports **30080** and **15672**.

{{% /tab %}}
{{< /tabs >}}

#### 4. Verify the RabbitMQ port mapping explicitly

{{< tabs >}}
{{% tab title="Script" %}}

```bash
docker ps --filter name=k3d-cosmic-shop-serverlb --format '{{.Ports}}'
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```
0.0.0.0:30080->30080/tcp, 0.0.0.0:15672->15672/tcp, ...
```

If **15672 is missing**, the cluster was created without the RabbitMQ port mapping. The management UI will not load at http://localhost:15672 until you recreate the cluster with `make setup-k3d` (see [Troubleshooting](#troubleshooting) below).

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

Here are some of the potential issues you may encounter in this step & suggested remediation steps.

{{< details summary="Click here for Troubleshooting Guidance" >}}
#### Potential Issue 1: Port already in use

If port 30080 or 5111 is taken, either stop the conflicting service or edit `scripts/setup-k3d.sh` to use different ports.

#### Potential Issue 2: RabbitMQ UI not loading (missing 15672 on loadbalancer)

If http://localhost:15672 does not load, check whether k3d mapped the port:

```bash
docker ps --filter name=k3d-cosmic-shop-serverlb --format '{{.Ports}}'
```

**If `15672` is absent: Workaround  without recreating the cluster**  -  port-forward in a separate terminal:

```bash
kubectl -n cosmic-shop port-forward svc/rabbitmq 15672:15672
```

Keep that terminal open, then open http://localhost:15672 (`guest` / `guest`).

#### Potential Issue 3: Cluster already exists

The script skips creation if a cluster named `cosmic-shop` already exists. To start fresh:

```bash
k3d cluster delete cosmic-shop
make setup-k3d
```
{{< /details >}}
