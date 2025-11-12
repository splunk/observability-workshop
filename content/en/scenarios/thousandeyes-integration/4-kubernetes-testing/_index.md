---
title: Kubernetes Service Testing
linkTitle: 4. Kubernetes Testing
weight: 4
---

## Replicating AppDynamics Test Recommendations

AppDynamics offers a feature called "Test Recommendations" that automatically suggests synthetic tests for your application endpoints. With ThousandEyes deployed inside your Kubernetes cluster, you can replicate this capability by leveraging Kubernetes service discovery combined with Splunk Observability Cloud's unified view.

Since the ThousandEyes Enterprise Agent runs **inside the cluster**, it can directly test internal Kubernetes services using their service names as hostnames. This provides a powerful way to monitor backend services that may not be exposed externally.

## How It Works

1. **Service Discovery**: Use `kubectl get svc` to enumerate services in your cluster
2. **Hostname Construction**: Build test URLs using Kubernetes DNS naming convention: `<service-name>.<namespace>.svc.cluster.local`
3. **Test Creation**: Configure ThousandEyes HTTP Server tests targeting these internal services
4. **Correlation in Splunk**: View synthetic test results alongside APM traces and infrastructure metrics

## Benefits of In-Cluster Testing

- **Internal Service Monitoring**: Test backend services not exposed to the internet
- **Service Mesh Awareness**: Monitor services behind Istio, Linkerd, or other service meshes
- **DNS Resolution Testing**: Validate Kubernetes DNS and service discovery
- **Network Policy Validation**: Ensure network policies allow proper communication
- **Latency Baseline**: Measure cluster-internal network performance
- **Pre-Production Testing**: Test services before exposing them via Ingress/LoadBalancer

## Step-by-Step Guide

### 1. Discover Kubernetes Services

List all services in your cluster or a specific namespace:

```bash
# Get all services in all namespaces
kubectl get svc --all-namespaces

# Get services in a specific namespace
kubectl get svc -n production

# Get services with detailed output including ports
kubectl get svc -n production -o wide
```

Example output:
```
NAMESPACE    NAME           TYPE        CLUSTER-IP      PORT(S)    AGE
production   api-gateway    ClusterIP   10.96.100.50    8080/TCP   5d
production   payment-svc    ClusterIP   10.96.100.51    8080/TCP   5d
production   auth-service   ClusterIP   10.96.100.52    9000/TCP   5d
production   postgres       ClusterIP   10.96.100.53    5432/TCP   5d
```

### 2. Build Test Hostnames

Kubernetes services are accessible via DNS using the following naming pattern:

```
<service-name>.<namespace>.svc.cluster.local
```

For the services above:
- `api-gateway.production.svc.cluster.local:8080`
- `payment-svc.production.svc.cluster.local:8080`
- `auth-service.production.svc.cluster.local:9000`

**Shorthand within the same namespace:**
If testing services in the same namespace as the ThousandEyes agent, you can use just the service name:
- `api-gateway:8080`
- `payment-svc:8080`

### 3. Create ThousandEyes Tests for Internal Services

For each service endpoint, create an HTTP Server test in ThousandEyes:

#### Via ThousandEyes UI

1. Navigate to **Cloud & Enterprise Agents > Test Settings**
2. Click **Add New Test** → **HTTP Server**
3. Configure the test:
   - **Test Name**: `[K8s] API Gateway Health`
   - **URL**: `http://api-gateway.production.svc.cluster.local:8080/health`
   - **Interval**: 2 minutes (or desired frequency)
   - **Agents**: Select your Kubernetes-deployed Enterprise Agent
   - **HTTP Response Code**: `200` (expected)
4. Click **Create Test**

#### Via ThousandEyes API

```bash
curl -X POST https://api.thousandeyes.com/v6/tests/http-server/new \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BEARER_TOKEN" \
  -d '{
    "testName": "[K8s] API Gateway Health",
    "url": "http://api-gateway.production.svc.cluster.local:8080/health",
    "interval": 120,
    "agents": [
      {"agentId": "<your-k8s-agent-id>"}
    ],
    "httpTimeLimit": 5000,
    "targetResponseTime": 1000,
    "alertsEnabled": 1
  }'
```

### 4. Configure Alerting Rules

Set up alerts for common failure scenarios:

- **Availability Alert**: Trigger when HTTP response is not 200
- **Performance Alert**: Trigger when response time exceeds baseline
- **DNS Resolution Alert**: Trigger when service DNS cannot be resolved

### 5. View Results in Splunk Observability Cloud

Once tests are running and integrated with Splunk:

1. **Navigate to the ThousandEyes Dashboard** in Splunk Observability Cloud
2. **Filter by test name** (e.g., `[K8s]` prefix) to see all Kubernetes internal tests
3. **Correlate with APM data**:
   - View synthetic test failures alongside APM error rates
   - Identify if issues are network-related (ThousandEyes) or application-related (APM)
4. **Create custom dashboards** combining:
   - ThousandEyes HTTP availability metrics
   - APM service latency and error rates
   - Kubernetes infrastructure metrics (CPU, memory, pod restarts)

## Example Use Cases

### Use Case 1: Microservices Health Checks

Test multiple microservice health endpoints:

```bash
http://user-service.production.svc.cluster.local:8080/actuator/health
http://order-service.production.svc.cluster.local:8080/actuator/health
http://inventory-service.production.svc.cluster.local:8080/actuator/health
```

### Use Case 2: API Gateway Endpoint Testing

Test API gateway routes:

```bash
http://api-gateway.production.svc.cluster.local:8080/api/v1/users
http://api-gateway.production.svc.cluster.local:8080/api/v1/orders
http://api-gateway.production.svc.cluster.local:8080/api/v1/products
```

### Use Case 3: Database Connection Testing

While ThousandEyes is primarily for HTTP testing, you can test database proxies:

```bash
# Test PgBouncer or database HTTP management interfaces
http://pgbouncer.production.svc.cluster.local:8080/stats
http://redis-exporter.production.svc.cluster.local:9121/metrics
```

### Use Case 4: External Service Dependencies

One of the most valuable capabilities of the in-cluster ThousandEyes agent is monitoring your application's external dependencies from the same network perspective as your services. This helps identify whether issues originate from your infrastructure, network path, or the external service itself.

#### Testing Payment Gateways

Create tests for critical payment gateway endpoints to ensure availability and performance:

**Stripe API:**
```bash
# Via ThousandEyes UI
Test Name: [External] Stripe API Health
URL: https://api.stripe.com/healthcheck
Interval: 2 minutes
Agents: Your Kubernetes Enterprise Agent
Expected Response: 200
```

**PayPal API:**
```bash
Test Name: [External] PayPal API Health
URL: https://api.paypal.com/v1/notifications/webhooks
Interval: 2 minutes
Agents: Your Kubernetes Enterprise Agent
Expected Response: 401 (authentication required, but endpoint is reachable)
```

**Via ThousandEyes API:**

```bash
curl -X POST https://api.thousandeyes.com/v6/tests/http-server/new \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BEARER_TOKEN" \
  -d '{
    "testName": "[External] Stripe API Availability",
    "url": "https://api.stripe.com/healthcheck",
    "interval": 120,
    "agents": [
      {"agentId": "<your-k8s-agent-id>"}
    ],
    "httpTimeLimit": 5000,
    "targetResponseTime": 2000,
    "alertsEnabled": 1
  }'
```

#### Why Monitor External Dependencies?

- **Proactive Issue Detection**: Know about payment gateway outages before your customers report them
- **Network Path Validation**: Ensure your Kubernetes egress network can reach external services
- **Performance Baseline**: Track latency from your cluster to external APIs
- **Compliance & SLA Monitoring**: Verify third-party services meet their SLA commitments
- **Root Cause Analysis**: Quickly determine if issues are network-related, your infrastructure, or the external provider

#### Recommended External Services to Monitor

- **Payment Processors**: Stripe, PayPal, Square, Braintree
- **Authentication Providers**: Auth0, Okta, Azure AD
- **Email Services**: SendGrid, Mailgun, AWS SES
- **SMS/Communications**: Twilio, MessageBird
- **CDN Endpoints**: Cloudflare, Fastly, Akamai
- **Cloud Storage**: AWS S3, Google Cloud Storage, Azure Blob Storage
- **Third-Party APIs**: Any critical business partner APIs

{{% notice title="Best Practice" style="success" icon="check" %}}
Use the `[External]` prefix in test names to easily distinguish between internal Kubernetes services and external dependencies in your dashboards.
{{% /notice %}}

## Best Practices

1. **Use Consistent Naming**: Prefix test names with `[K8s]` or `[Internal]` for easy filtering
2. **Test Health Endpoints First**: Start with `/health` or `/readiness` endpoints before testing business logic
3. **Set Appropriate Intervals**: Use shorter intervals (1-2 minutes) for critical services
4. **Tag Tests**: Use ThousandEyes labels/tags to group tests by:
   - Environment (dev, staging, production)
   - Service type (API, database, cache)
   - Team ownership
5. **Monitor Test Agent Health**: Ensure the ThousandEyes agent pod is healthy and has sufficient resources
6. **Correlate with APM**: Create Splunk dashboards that show both synthetic and real user metrics side-by-side

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
By testing internal services before they're exposed externally, you can catch issues early and ensure your infrastructure is healthy before user traffic reaches it.
{{% /notice %}}
