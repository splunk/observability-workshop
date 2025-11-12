---
title: Troubleshooting
linkTitle: 5. Troubleshooting
weight: 5
---

This section covers common issues you may encounter when deploying and using the ThousandEyes Enterprise Agent in Kubernetes.

## Test Failing with DNS Resolution Error

If your tests are failing with DNS resolution errors, verify DNS from within the ThousandEyes pod:

```bash
# Verify DNS resolution from within the pod
kubectl exec -n te-demo -it <pod-name> -- nslookup api-gateway.production.svc.cluster.local

# Check CoreDNS logs
kubectl logs -n kube-system -l k8s-app=kube-dns
```

**Common causes:**
- Service doesn't exist in the specified namespace
- Typo in the service name or namespace
- CoreDNS is not functioning properly

## Connection Refused Errors

If you're seeing connection refused errors, check the following:

```bash
# Verify service endpoints exist
kubectl get endpoints -n production api-gateway

# Check if pods are ready
kubectl get pods -n production -l app=api-gateway

# Test connectivity from agent pod
kubectl exec -n te-demo -it <pod-name> -- curl -v http://api-gateway.production.svc.cluster.local:8080/health
```

**Common causes:**
- No pods backing the service (endpoints are empty)
- Pods are not in Ready state
- Wrong port specified in the test URL
- Service selector doesn't match pod labels

## Network Policy Blocking Traffic

If network policies are blocking traffic from the ThousandEyes agent:

```bash
# List network policies
kubectl get networkpolicies -n production

# Describe network policy
kubectl describe networkpolicy <policy-name> -n production
```

**Solution:**
Create a network policy to allow traffic from the `te-demo` namespace to your services:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-thousandeyes-agent
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api-gateway
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: te-demo
    ports:
    - protocol: TCP
      port: 8080
```

## Agent Pod Not Starting

If the ThousandEyes agent pod is not starting, check the pod status and events:

```bash
# Get pod status
kubectl get pods -n te-demo

# Describe pod to see events
kubectl describe pod -n te-demo <pod-name>

# Check logs
kubectl logs -n te-demo <pod-name>
```

**Common causes:**
- Insufficient resources (memory/CPU)
- Invalid or missing TEAGENT_ACCOUNT_TOKEN secret
- Security context capabilities not allowed by Pod Security Policy
- Image pull errors

**Solutions:**
- Increase memory limits if OOMKilled
- Verify secret is created correctly: `kubectl get secret te-creds -n te-demo -o yaml`
- Check Pod Security Policy allows NET_ADMIN and SYS_ADMIN capabilities
- Verify image pull: `kubectl describe pod -n te-demo <pod-name>`

## Agent Not Appearing in ThousandEyes Dashboard

If the agent is running but not appearing in the ThousandEyes dashboard:

```bash
# Check agent logs for connection issues
kubectl logs -n te-demo -l app=thousandeyes --tail=100
```

**Common causes:**
- Invalid or incorrect TEAGENT_ACCOUNT_TOKEN
- Network egress blocked (firewall or network policy)
- Agent cannot reach ThousandEyes Cloud servers

**Solutions:**
1. Verify the token is correct and properly base64-encoded
2. Check if egress to `*.thousandeyes.com` is allowed
3. Verify the agent can reach the internet:

```bash
kubectl exec -n te-demo -it <pod-name> -- curl -v https://api.thousandeyes.com
```

## Data Not Appearing in Splunk Observability Cloud

If ThousandEyes data is not appearing in Splunk:

**Verify integration configuration:**
1. Check the OpenTelemetry integration is configured correctly in ThousandEyes
2. Verify the Splunk ingest endpoint URL is correct for your realm
3. Confirm the `X-SF-Token` header contains a valid Splunk access token
4. Ensure tests are assigned to the integration

**Check test assignment:**
```bash
# Use ThousandEyes API to verify integration
curl -v https://api.thousandeyes.com/v7/stream \
  -H "Authorization: Bearer $BEARER_TOKEN"
```

**Common causes:**
- Wrong Splunk realm in endpoint URL
- Invalid or expired Splunk access token
- Tests not assigned to the OpenTelemetry integration
- Integration not enabled or saved properly

## High Memory Usage

If the ThousandEyes agent pod is consuming excessive memory:

```bash
# Check current memory usage
kubectl top pod -n te-demo

# Check for OOMKilled events
kubectl describe pod -n te-demo <pod-name> | grep -i oom
```

**Solutions:**
1. Increase memory limits in the deployment:

```yaml
resources:
  limits:
    memory: 4096Mi  # Increase from 3584Mi
  requests:
    memory: 2500Mi  # Increase from 2000Mi
```

2. Reduce the number of concurrent tests assigned to the agent
3. Check if the agent is running unnecessary services

## Permission Denied Errors

If you see permission denied errors in the agent logs:

**Verify security context:**
```bash
kubectl get pod -n te-demo <pod-name> -o jsonpath='{.spec.containers[0].securityContext}'
```

**Solution:**
Ensure the pod has the required capabilities:

```yaml
securityContext:
  capabilities:
    add:
      - NET_ADMIN
      - SYS_ADMIN
```

{{% notice title="Note" style="info" %}}
Some Kubernetes clusters with strict Pod Security Policies may not allow these capabilities. You may need to work with your cluster administrators to create an appropriate policy exception.
{{% /notice %}}

## Getting Help

If you encounter issues not covered in this guide:

1. **ThousandEyes Support**: Contact ThousandEyes support at [support.thousandeyes.com](https://support.thousandeyes.com)
2. **Splunk Support**: For Splunk Observability Cloud issues, visit [Splunk Support](https://www.splunk.com/en_us/support-and-services.html)
3. **Community Forums**: 
   - [ThousandEyes Community](https://community.thousandeyes.com)
   - [Splunk Community](https://community.splunk.com)

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
When asking for help, always include relevant logs, pod descriptions, and error messages to help troubleshoot more effectively.
{{% /notice %}}
