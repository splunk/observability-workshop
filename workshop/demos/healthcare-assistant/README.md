# Healthcare Assistant Demo Application

## Build Docker Image

```bash
cd workshop/demos/healthcare-assistant 
docker build -f ./Dockerfile -t ghcr.io/splunk/healthcare-assistant:demo-v1 .
docker push ghcr.io/splunk/healthcare-assistant:demo-v1
```

## Run Locally

### Create OpenAI Secret

```bash
export OPENAI_API_KEY=your_openai_api_key
export OPENAI_BASE_URL=your_openai_base_url

kubectl create secret generic openai-api \
  --from-literal=openai-api-key="$OPENAI_API_KEY" \
  --from-literal=openai-api-endpoint="$OPENAI_BASE_URL"
```

### Create Base Config Map

```bash
kubectl apply -f ~/observability-workshop/workshop/demos/healthcare-assistant/healthcare-assistant-config.yaml
````

### Deploy PostgreSQL

``` bash
kubectl apply -f ~/observability-workshop/workshop/demos/healthcare-assistant/postgres.yaml
```

### Run the Setup Job

This will populate the vector database:

``` bash
kubectl apply -f ~/observability-workshop/workshop/demos/healthcare-assistant/setup-job.yaml
```

### Create Secret for Splunk Agent Observability (Standalone)

```bash
export GALILEO_API_KEY=your_galileo_api_key

kubectl create secret generic splunk-ao-secret \
  --from-literal=SPLUNK_AO_API_KEY="$GALILEO_API_KEY"
````

### Create Config Maps for Splunk Agent Observability (Standalone)

``` bash
kubectl create configmap splunk-ao-config \
  --from-literal=SPLUNK_AO_CONSOLE_URL="https://console.multitenant.galileocloud.io" \
  --from-literal=SPLUNK_AO_PROJECT="Healthcare Assistant Demo" \
  --from-literal=SPLUNK_AO_AGENT_STREAM="default"

kubectl create configmap splunk-agent-control-config \
  --from-literal=SPLUNK_AO_API_URL="https://api.multitenant.sao.splunkcloud.com" \
  --from-literal=AGENT_CONTROL_URL="https://console.multitenant.sao.splunkcloud.com/api/agent-control" \
  --from-literal=AGENT_CONTROL_AGENT_NAME="agent-control-example" \
  --from-literal=AGENT_CONTROL_API_KEY_HEADER="Splunk-AO-API-Key" \
  --from-literal=AGENT_CONTROL_RUNTIME_AUTH_MODE="jwt" \
  --from-literal=AGENT_CONTROL_TARGET_TYPE="log_stream"
```

### Install the Applications

Install the application and its dependencies using the following commands:

```bash
kubectl apply -f ./k8s-demo-local.yaml
```

### Test the Application

```bash
kubectl port-forward svc/healthcare-assistant-service 8501:8501
```

The application is accessible via the following URLs:

http://localhost:8501

## Deploy to Production

Refer to the following [README](https://github.com/splunk/o11y-field-demos/blob/main/splunk-agent-observability-demo/README.md) file.
