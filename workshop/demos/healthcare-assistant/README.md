# Healthcare Assistant Demo Application

> **Architecture:** this app is split into an always-on **front-end** (Streamlit UI,
> single URL) and **back-end** agent services created on demand — one per
> `(agent stream, target)` — so parallel presenters get isolated traces and
> Agent Control. See [CLAUDE.md](./CLAUDE.md) for the full design. The same image
> runs both roles (front-end: `streamlit run app.py`; back-end: `uvicorn server:app`).

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

### Install the Front-end

`k8s-demo-local.yaml` deploys only the always-on front-end plus the RBAC the
orchestrator needs to create back-end pods. Back-ends are created at runtime —
one per `(agent stream, target)` you choose in the UI — so they are not in this file.

```bash
kubectl apply -f ./k8s-demo-local.yaml
```

> Point `BACKEND_IMAGE` in `k8s-demo-local.yaml` at your locally built/pushed tag.
> A back-end only mounts the ConfigMaps/Secrets for the target you pick, so for
> local testing you only need the config for the target(s) you'll demo (e.g. the
> standalone ones created above). Picking a target whose Secret is missing will
> leave its back-end stuck in `ContainerCreating` and the launch spinner will time out.

### Test the Application

```bash
kubectl port-forward svc/healthcare-assistant-service 8501:8501
```

Open http://localhost:8501 — enter an **agent stream name** and **target**, wait for
the back-end to provision (first launch pays a cold start), then chat. Inspect the
back-ends it creates with:

```bash
kubectl get deploy,svc,pod -l component=healthcare-backend
```

## Deploy to Production

Refer to the following [README](https://github.com/splunk/o11y-field-demos/blob/main/splunk-agent-observability-demo/README.md) file.
