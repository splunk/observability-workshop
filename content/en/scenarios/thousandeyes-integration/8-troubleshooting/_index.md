---
title: Troubleshooting
linkTitle: 8. Troubleshooting
weight: 8
time: 15 minutes
description: Diagnose common deployment, connectivity, metrics-streaming, and trace-correlation issues in the ThousandEyes scenario.
---

This section covers common issues you may encounter when deploying and using the ThousandEyes Enterprise Agent in Kubernetes.

## Test Failing with DNS Resolution Error

If your tests are failing with DNS resolution errors, verify DNS from within the ThousandEyes pod:

```bash
# Verify DNS resolution from within the pod
kubectl exec -n te-demo -it <pod-name> -- nslookup api-gateway.default.svc.cluster.local

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
kubectl get endpoints -n default api-gateway

# Check if pods are ready
kubectl get pods -n default -l app=api-gateway

# Test connectivity from agent pod
kubectl exec -n te-demo -it <pod-name> -- curl -v http://api-gateway.default.svc.cluster.local:82/api/customer/owners
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
kubectl get networkpolicies -n default

# Describe network policy
kubectl describe networkpolicy <policy-name> -n default
```

**Solution:**
Create a network policy to allow traffic from the `te-demo` namespace to your services:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-thousandeyes-agent
  namespace: default
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

## Distributed Tracing Not Appearing in ThousandEyes

If your metric stream is working but the ThousandEyes **Service Map** is empty or no trace is found:

**Verify the monitored endpoint:**

- It accepts HTTP headers
- It is instrumented with OpenTelemetry
- It propagates trace context downstream
- It sends traces to Splunk APM

**Common causes:**

- The endpoint is a page URL rather than an HTTP Server or API target
- The service is not instrumented, so ThousandEyes can inject headers but no trace is emitted
- The endpoint only returns a local health response and does not exercise downstream services

**Recommended fixes:**

1. Switch the ThousandEyes test to an instrumented backend API route
2. Confirm traces for that route already exist in Splunk APM
3. Re-run the test after enabling ThousandEyes distributed tracing

## Missing ThousandEyes Link in Splunk APM

If the trace opens in Splunk APM but you do not see the ThousandEyes backlink or metadata:

**Common cause:**

The `b3` propagator can override `trace_state` and clear the value that ThousandEyes expects to preserve for the reverse link.

**Fix:**

Set the propagators explicitly on the instrumented service:

```bash
OTEL_PROPAGATORS=baggage,b3,tracecontext
```

After changing the environment variable, restart the instrumented workload and generate new traffic.

## Splunk APM Connector Authentication Errors

If the **Generic Connector** in ThousandEyes cannot query Splunk APM:

**Check the following:**

1. The connector target is `https://api.<REALM>.signalfx.com`
2. The token used in the connector has the **API** scope
3. The user creating the token has the required role in Splunk Observability Cloud

{{% notice title="Token Reminder" style="info" %}}
The OpenTelemetry metrics stream uses a Splunk **Ingest** token. The ThousandEyes **Generic Connector** for APM uses a Splunk **API** token. Mixing them up is one of the most common causes of partial integration.
{{% /notice %}}

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
