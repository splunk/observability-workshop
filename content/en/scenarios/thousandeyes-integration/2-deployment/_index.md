---
title: Deployment
linkTitle: 2. Deployment
weight: 2
---

This section guides you through deploying the ThousandEyes Enterprise Agent in your Kubernetes cluster.

## Components

The deployment consists of two files:

### 1. Secrets File (`credentialsSecret.yaml`)

Contains your ThousandEyes agent token (base64 encoded). This secret is referenced by the deployment to authenticate the agent with ThousandEyes Cloud.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: te-creds
type: Opaque
data:
  TEAGENT_ACCOUNT_TOKEN: <base64-encoded-token>
```

### 2. Deployment Manifest (`thousandEyesDeploy.yaml`)

Defines the Enterprise Agent pod configuration with the following key settings:

- **Namespace**: `te-demo` (customize as needed)
- **Image**: `thousandeyes/enterprise-agent:latest` from Docker Hub
- **Hostname**: `te-agent-aleccham` (appears in ThousandEyes dashboard)
- **Capabilities**: Requires `NET_ADMIN` and `SYS_ADMIN` for network testing
- **Resources**: 
  - Memory limit: 3584Mi
  - Memory request: 2000Mi

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  namespace: te-demo
  name: thousandeyes
  labels:
    app: thousandeyes
spec:
  replicas: 1
  selector:
    matchLabels:
      app: thousandeyes
  template:
    metadata:
      labels:
        app: thousandeyes
    spec:
      hostname: te-agent-aleccham
      containers:
      - name: thousandeyes
        image: 'thousandeyes/enterprise-agent:latest'
        imagePullPolicy: Always
        command:
          - /sbin/my_init
        securityContext:
          capabilities:
            add:
              - NET_ADMIN
              - SYS_ADMIN
        env:
          - name: TEAGENT_ACCOUNT_TOKEN
            valueFrom:
              secretKeyRef:
                name: te-creds
                key: TEAGENT_ACCOUNT_TOKEN
          - name: TEAGENT_INET
            value: "4"
        resources:
          limits:
            memory: 3584Mi
          requests:
            memory: 2000Mi
```

{{% notice title="Important Notes" style="warning" %}}
- The agent requires elevated privileges (`NET_ADMIN`, `SYS_ADMIN`) to perform network tests
- The `TEAGENT_INET: "4"` environment variable forces IPv4-only mode (required for some network configurations)
- The `/sbin/my_init` command is required for proper agent initialization and service management
- The `imagePullPolicy: Always` ensures you always pull the latest image version
- Adjust the `hostname` field to uniquely identify your agent in the ThousandEyes dashboard
- Modify the `namespace` to match your Kubernetes environment
- The ThousandEyes Enterprise Agent has relatively high hardware requirements; you may need to adjust these depending on your environment
{{% /notice %}}

## Installation Steps

### Step 1: Create the ThousandEyes Token

1. Log in to the ThousandEyes platform at [app.thousandeyes.com/login](https://app.thousandeyes.com/login)

2. Navigate to **Cloud & Enterprise Agents > Agent Settings > Add New Enterprise Agent**

3. Copy your **Account Group Token**

4. Base64 encode the token:

   ```bash
   echo -n 'your-token-here' | base64
   ```

5. Save the base64-encoded output for the next step

![Get ThousandEyes Token](../images/te1.gif)

### Step 2: Create the Namespace

Create the namespace (if it doesn't exist):

```bash
kubectl create namespace te-demo
```

### Step 3: Create the Secret

Create a file named `credentialsSecret.yaml` with your base64-encoded token:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: te-creds
  namespace: te-demo
type: Opaque
data:
  TEAGENT_ACCOUNT_TOKEN: <your-base64-encoded-token-here>
```

Apply the secret:

```bash
kubectl apply -f credentialsSecret.yaml
```

### Step 4: Create the Deployment

Create a file named `thousandEyesDeploy.yaml` with the deployment manifest shown above (customize the hostname and namespace as needed).

Apply the deployment:

```bash
kubectl apply -f thousandEyesDeploy.yaml
```

### Step 5: Verify the Deployment

Verify the agent is running:

```bash
kubectl get pods -n te-demo
```

Expected output:
```
NAME                            READY   STATUS    RESTARTS   AGE
thousandeyes-xxxxxxxxxx-xxxxx   1/1     Running   0          2m
```

Check the logs to ensure the agent is connecting:

```bash
kubectl logs -n te-demo -l app=thousandeyes
```

### Step 6: Verify in ThousandEyes Dashboard

Verify in the ThousandEyes dashboard that the agent has registered successfully:

Navigate to **Cloud & Enterprise Agents > Agent Settings** to see your newly registered agent.

{{% notice title="Success" style="success" icon="check" %}}
Your ThousandEyes Enterprise Agent is now running in Kubernetes! Next, we'll integrate it with Splunk Observability Cloud.
{{% /notice %}}

## Background

ThousandEyes does not provide official Kubernetes deployment documentation. Their standard deployment method uses `docker run` commands, which makes it challenging to translate into reusable Kubernetes manifests. This guide bridges that gap by providing production-ready Kubernetes configurations.
