---
title: Verification
weight: 6
---

## Verify All Components

Run this comprehensive check to ensure everything is running:

```bash
echo "=== Cluster Nodes ==="
kubectl get nodes

echo -e "\n=== Cilium Components ==="
kubectl get pods -n kube-system -l k8s-app=cilium

echo -e "\n=== Hubble Components ==="
kubectl get pods -n kube-system | grep hubble

echo -e "\n=== Tetragon ==="
kubectl get pods -n tetragon

echo -e "\n=== Splunk OTel Collector ==="
kubectl get pods -n otel-splunk
```

**Expected Output:**
- 2 nodes in `Ready` state
- Cilium pods: 2 running (one per node)
- Hubble relay and timescape: running
- Tetragon pods: 2 running + operator
- Splunk collector pods: running

## Verify Metrics Endpoints

Test that metrics are accessible from each component:

```bash
# Test Cilium metrics
kubectl exec -n kube-system ds/cilium -- curl -s localhost:9962/metrics | head -20

# Test Hubble metrics
kubectl exec -n kube-system ds/cilium -- curl -s localhost:9965/metrics | head -20

# Test Tetragon metrics
kubectl exec -n tetragon ds/tetragon -- curl -s localhost:2112/metrics | head -20
```

Each command should return Prometheus-formatted metrics.

## Verify in Splunk Observability Cloud

### Check Infrastructure Navigator

1. Log in to your Splunk Observability Cloud account
2. Navigate to **Infrastructure** → **Kubernetes**
3. Find your cluster: `isovalent-demo`
4. Verify the cluster is reporting metrics

### Search for Isovalent Metrics

Navigate to **Metrics** and search for:
- `cilium_*` - Cilium networking metrics
- `hubble_*` - Network flow metrics
- `tetragon_*` - Runtime security metrics

{{% notice title="Tip" style="tip" %}}
It may take 2-3 minutes after installation for metrics to start appearing in Splunk Observability Cloud.
{{% /notice %}}

## View Dashboards

### Create Custom Dashboard

1. Navigate to **Dashboards** → **Create**
2. Add charts for key metrics:

**Cilium Endpoint State:**
```
cilium_endpoint_state{cluster="isovalent-demo"}
```

**Hubble Flow Processing:**
```
hubble_flows_processed_total{cluster="isovalent-demo"}
```

**Tetragon Events:**
```
tetragon_dns_total{cluster="isovalent-demo"}
```

### Example Queries

**DNS Query Rate:**
```
rate(hubble_dns_queries_total{cluster="isovalent-demo"}[1m])
```

**Dropped Packets:**
```
sum by (reason) (hubble_drop_total{cluster="isovalent-demo"})
```

**Network Policy Enforcements:**
```
rate(cilium_policy_l7_total{cluster="isovalent-demo"}[5m])
```

## Troubleshooting

### No Metrics in Splunk

If you don't see metrics:

1. **Check collector logs:**
   ```bash
   kubectl logs -n otel-splunk -l app=splunk-otel-collector --tail=200
   ```

2. **Verify scrape targets:**
   ```bash
   kubectl describe configmap -n otel-splunk splunk-otel-collector-otel-agent
   ```

3. **Check network connectivity:**
   ```bash
   kubectl exec -n otel-splunk -it deployment/splunk-otel-collector -- \
     curl -v https://ingest.<YOUR-REALM>.signalfx.com
   ```

### Pods Not Running

If Cilium or Tetragon pods are not running:

1. **Check pod status:**
   ```bash
   kubectl describe pod -n kube-system <cilium-pod-name>
   ```

2. **View logs:**
   ```bash
   kubectl logs -n kube-system <cilium-pod-name>
   ```

3. **Verify node readiness:**
   ```bash
   kubectl get nodes -o wide
   ```

## Cleanup

To remove all resources and avoid AWS charges:

```bash
# Delete the OpenTelemetry Collector
helm uninstall splunk-otel-collector -n otel-splunk

# Delete the EKS cluster (this removes everything)
eksctl delete cluster --name isovalent-demo --region us-east-1
```

{{% notice title="Warning" style="warning" %}}
The cleanup process takes 10-15 minutes. Ensure all resources are deleted to avoid charges.
{{% /notice %}}

## Next Steps

Now that your integration is working:

- Deploy sample applications to generate network traffic
- Create network policies and monitor enforcement
- Set up alerts in Splunk for dropped packets or security events
- Explore Hubble's L7 visibility for HTTP/gRPC traffic
- Use Tetragon to monitor process execution and file access

{{% notice title="Success!" style="success" %}}
Congratulations! You've successfully integrated Isovalent Enterprise Platform with Splunk Observability Cloud.
{{% /notice %}}
