# Agentic AI Demo Application 

## Run with Docker Compose

### Prerequisites

* Docker
* Docker Compose

### Clone the Repo

``` bash
git clone https://github.com/splunk/observability-workshop.git
cd observability-workshop/workshop/demos/agentic-ai-demo
```

### Define Environment Variables

Add an `.env.override` file to the `observability-workshop/workshop/demos/agentic-ai-demo`
folder with the following contents:

``` bash
SPLUNK_ACCESS_TOKEN=your_token_here
SPLUNK_API_URL=e.g. https://api.us1.signalfx.com
SPLUNK_INGEST_URL=e.g. https://ingest.us1.signalfx.com
SPLUNK_MEMORY_LIMIT_MIB=1024 # adjust as needed
SPLUNK_HEC_TOKEN=your_HEC_token_here
SPLUNK_HEC_URL=your_HEC_URL_here
OTEL_RESOURCE_ATTRIBUTES=deployment.environment=agentic-ai-demo
```

Add the `SPLUNK_ACCESS_TOKEN` token required to send data to your Splunk
Observability Cloud organization.  Modify the realm in the `SPLUNK_API_URL` and
`SPLUNK_INGEST_URL` environment variables if your org is not in `us1`.

Add the `SPLUNK_HEC_TOKEN` and `SPLUNK_HEC_URL` to send logs to your Splunk Enterprise
or Splunk Cloud instance. For Splunk Cloud, the `SPLUNK_HEC_URL` should be something like
`https://<hostname>.splunkcloud.com:443`.

> Note: ensure this file isn't added to GitHub 

#### Using OpenAI

If using OpenAI, add your OpenAI API key to the `.env.override` file: 

``` bash
# OpenAI
OPENAI_API_KEY=your_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

#### Using Together AI

If using Together AI, add the following to the `.env.override` file:

``` bash
# Together AI
OPENAI_API_KEY=your_key_here
OPENAI_BASE_URL=https://api.together.xyz/v1
OPENAI_MODEL=meta-llama/Llama-3.3-70B-Instruct-Turbo
```

#### Using Cisco Circuit API

If using Cisco APIs for LLM access, add the following to the `.env.override` file:

````
USE_CISCO_API=true
CISCO_CLIENT_ID=your_cisco_client_id
CISCO_CLIENT_SECRET=your_cisco_client_secret
CISCO_APP_KEY=_your_cisco_app_key
````

### Enable LLM Quality Evaluation

Splunk Observability Cloud is able to evaluate the quality of LLM responses, to check 
for relevancy, correctness, bias, etc. 

Currently, this functionality is only available when using an OpenAI API such as `gpt-4o-mini`, 
either directly or via Cisco Circuit API. 

To enable this functionality, uncomment the following two lines of the 
[requirements.txt](./app/requirements.txt) file: 

````
splunk-otel-util-genai-evals==0.1.4
splunk-otel-genai-evals-deepeval==0.1.8
````

If using the Cisco Circuit API, add the following to the `.env.override` file:  

````
DEEPEVAL_LLM_BASE_URL=https://chat-ai.cisco.com/openai/deployments/gpt-4o-mini
DEEPEVAL_LLM_MODEL="gpt-4o-mini"
DEEPEVAL_LLM_PROVIDER=openai
DEEPEVAL_LLM_CLIENT_ID=your_client_id
DEEPEVAL_LLM_CLIENT_SECRET=your_client_secret
DEEPEVAL_LLM_TOKEN_URL=https://id.cisco.com/oauth2/default/v1/token
DEEPEVAL_LLM_CLIENT_APP_NAME=your_app_key
````

### Run the Application 

Use the following command to run the application: 

``` bash
docker compose --env-file .env --env-file .env.override up --force-recreate --remove-orphans --detach --build 
```

This will start the command with the load generator, which will send requests 
to exercise application functionality every 30 to 90 seconds. 

If you'd like to start the application without the load generator, use 
the following command instead: 

``` bash
docker compose --env-file .env --env-file .env.override up --force-recreate --remove-orphans --detach --build postgresql otel-collector app payment
```

### Test the Application

Create an order:

``` bash
curl -sS -X POST "http://localhost:8080/chat" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"customer_id":1,"request":"I''d like to order 2 of sku COF-COL-DR-12 and 1 of sku KIT-CB-START, for pickup at store_id 1."}'
```

Create an order that includes PII in the prompt:

``` bash
curl -sS -X POST "http://localhost:8080/chat" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"customer_id":1,"request":"I''d like to order 2 of sku COF-COL-DR-12 and 1 of sku KIT-CB-START, for pickup at store_id 1. My credit card number is 5555555555554444."}'
```

Ask a question about an order: 

``` bash
curl -sS -X POST "http://localhost:8080/chat" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"customer_id":1,"request":"What products were included in my most recent order?"}'
```

Ask a question about order amounts:

``` bash
curl -sS -X POST "http://localhost:8080/chat" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"customer_id":1,"request":"What was the total dollar amount of my most recent order?"}'
```

Ask a question that requires both order and product info:

``` bash
curl -sS -X POST "http://localhost:8080/chat" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"customer_id":1,"request":"Can you describe the product that I''ve ordered most frequently? Please include the price and total quantity ordered."}'
```


Ask a question that requires product info:

``` bash
curl -sS -X POST "http://localhost:8080/chat" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"customer_id":1,"request":"What''s the most expensive product you sell?"}'
```

Ask a question about inventory:

``` bash
curl -sS -X POST "http://localhost:8080/chat" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"customer_id":1,"request":"What is the inventory for product_sku COF-COL-DR-12 at store_id 1, 2, and 3?"}'
```

Ask a question about inventory with stores that don't exist:

``` bash
curl -sS -X POST "http://localhost:8080/chat" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"customer_id":1,"request":"What is the inventory for product_sku COF-COL-DR-12 at store_id 9 and 10?"}'
```

### Test Maintenance Endpoints

Restore inventory to its original state: 

``` bash
curl "http://localhost:8080/refresh_inventory"
```

Archive orders older than 6 hours: 

``` bash
curl "http://localhost:8080/archive_orders"
```

## Run in Kubernetes  

### Create Secrets

Create Kubernetes secrets for the OpenAI API and Cisco Circuit API keys (if applicable): 

``` bash
kubectl create secret generic agentic-ai-secret \
    --from-literal=openai_api_key='<your Open AI API Key>' \
    --from-literal=cisco_client_id='<your Cisco Client ID>' \
    --from-literal=cisco_client_secret='<your Cisco Client Secret>' \
    --from-literal=cisco_app_key='<your Cisco App Key>'
```

### Deploy the OpenTelemetry Collector

Start by adding the Helm chart and ensuring it's up-to-date: 

``` bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart

helm repo update
```

Then set environment variables that will be used to configure the collector: 

``` bash
export CLUSTER_NAME=<the name of your Kubernetes cluster> 
export ENVIRONMENT_NAME=<which environment to send data to for Splunk Observability Cloud> 
export SPLUNK_ACCESS_TOKEN=<your access token for Splunk Observability Cloud>  
export SPLUNK_REALM=<your realm for Splunk Observability Cloud i.e. us0, us1, eu0, etc.> 
export SPLUNK_HEC_URL=<HEC endpoint to send logs to Splunk platform i.e. https://<hostname>:443/services/collector/event>  
export SPLUNK_HEC_TOKEN=<HEC token to send logs to Splunk platform>  
export SPLUNK_INDEX=<name of index to send logs to in Splunk platform> 
```

Deploy the Splunk Distribution of the OpenTelemetry Collector for Kubernetes:

``` bash
helm install splunk-otel-collector \
--set="clusterName=$CLUSTER_NAME" \
--set="environment=$ENVIRONMENT_NAME" \
--set="splunkObservability.accessToken=$SPLUNK_ACCESS_TOKEN" \
--set="splunkObservability.realm=$SPLUNK_REALM" \
--set="splunkPlatform.endpoint=$SPLUNK_HEC_URL" \
--set="splunkPlatform.token=$SPLUNK_HEC_TOKEN" \
--set="splunkPlatform.index=$SPLUNK_INDEX" \
splunk-otel-collector-chart/splunk-otel-collector
```

### Build Docker Images 

### Build Docker Images (locally)

Build Docker images and push them to the `ghcr.io/splunk` repository:

``` bash
docker compose build app
docker compose build load-generator
docker compose build payment
docker compose build postgresql
```

Push them to the `ghcr.io/splunk` repository:

``` bash
docker push ghcr.io/splunk/agentic-ai-demo-app:1.0
docker push ghcr.io/splunk/agentic-ai-demo-loadgen:1.0
docker push ghcr.io/splunk/agentic-ai-demo-db:1.0
docker push ghcr.io/splunk/agentic-ai-demo-payment:1.0
```

### Create Secrets

Create Kubernetes secrets for the OpenAI API and Cisco Circuit API keys (if applicable):

``` bash
kubectl create ns agentic-ai-demo-app

kubectl create secret generic agentic-ai-secret -n agentic-ai-demo-app \
    --from-literal=openai_api_key='dummy' \
    --from-literal=cisco_client_id='<your Cisco Client ID>' \
    --from-literal=cisco_client_secret='<your Cisco Client Secret>' \
    --from-literal=cisco_app_key='<your Cisco App Key>'
```

### Deploy the Application

Next, we can deploy our application to Kubernetes: 

``` bash
kubectl apply -f ./kubernetes.yaml -n agentic-ai-demo-app
```

### Test the Application

``` bash
kubectl port-forward service/agentic-ai-demo-app -n agentic-ai-demo-app 8080:8080
```

Send a pickup order:

``` bash
curl -sS -X POST "http://localhost:8080/chat" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"customer_id":1,"request":"I''d like to order 2 of sku COF-COL-DR-12 and 1 of sku KIT-CB-START, for pickup at store_id 1."}'
```

## Run on a Cisco AI POD

### Clone the Repo

``` bash
git clone https://github.com/splunk/observability-workshop.git 
cd observability-workshop/workshop/demos/agentic-ai-demo 
```

### Create an OpenShift Project

Create a new OpenShift project to work with, then ensure the anyuid Security Context Constraint (SCC) 
is added to the default service account in the new project: 

``` bash
oc new-project agentic-ai-demo-app
oc adm policy add-scc-to-user anyuid -z default
```

### Create Secrets

Create Kubernetes secrets for the OpenAI API and Cisco Circuit API keys (if applicable):

``` bash
kubectl create secret generic agentic-ai-secret -n agentic-ai-demo-app \
    --from-literal=openai_api_key='dummy' \
    --from-literal=cisco_client_id='<your Cisco Client ID>' \
    --from-literal=cisco_client_secret='<your Cisco Client Secret>' \
    --from-literal=cisco_app_key='<your Cisco App Key>'
```

### Build Docker Images (locally)

Build Docker images and push them to the `ghcr.io/splunk` repository: 

``` bash
docker compose build app
docker compose build load-generator
docker compose build payment
docker compose build postgresql
```

Push them to the `ghcr.io/splunk` repository:

``` bash
docker push ghcr.io/splunk/agentic-ai-demo-app:1.0
docker push ghcr.io/splunk/agentic-ai-demo-loadgen:1.0
docker push ghcr.io/splunk/agentic-ai-demo-db:1.0
docker push ghcr.io/splunk/agentic-ai-demo-payment:1.0
```

### Deploy the Application

Next, we can deploy our application to OpenShift:

``` bash
oc apply -f ./ai-pod.yaml -n agentic-ai-demo-app
```

### Test the Application

``` bash
oc port-forward service/agentic-ai-demo-app -n agentic-ai-demo-app 8080:8080
```

Send a pickup order:

``` bash
curl -sS -X POST "http://localhost:8080/chat" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"customer_id":1,"request":"I''d like to order 2 of sku COF-COL-DR-12 and 1 of sku KIT-CB-START, for pickup at store_id 1."}'
```

## Working with the Database

To connect to the Postgresql database as root, shell into the `db` container then execute 
the following command: 

``` bash
psql -U root -d agentic-ai-demo
```

If you need to clear the existing database contents and initialize a new one from 
scratch, first stop the docker containers, then delete the volumes with the 
following commands: 

``` bash
docker compose stop
docker-compose down --volumes
```