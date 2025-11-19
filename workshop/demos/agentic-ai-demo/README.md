# Agentic AI Demo Application 

## Run in Docker (for development/testing) 

### Prerequisites

* Docker

### Define Environment Variables

Add an `.env.override` file with the following environment variables: 

````
OPENAI_API_KEY=your_key_here
SPLUNK_ACCESS_TOKEN=your_token_here
SPLUNK_API_URL=e.g. https://api.us1.signalfx.com
SPLUNK_MEMORY_LIMIT_MIB=1024 # adjust as needed
SPLUNK_HEC_TOKEN=your_HEC_token_here
SPLUNK_HEC_URL=your_HEC_URL_here
SPLUNK_INGEST_URL=e.g. https://ingest.us1.signalfx.com
OTEL_RESOURCE_ATTRIBUTES=deployment.environment=agentic-ai-demo
````

> Note: ensure this file isn't added to GitHub 

### Run the Application 

Use the following command to run the application: 

``` bash
cd workshop/demos/agentic-ai-demo
docker compose --env-file .env --env-file .env.override up --force-recreate --remove-orphans --detach --build 
```
### Test the Application

Send a pickup order:

``` bash
curl -sS -X POST "http://localhost:8080/chat" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"customer_id":1,"request":"I''d like to order 2 of sku COF-COL-DR-12 and 1 of sku KIT-CB-START, for pickup at store_id 1."}'
```

Send a delivery order:

``` bash
curl -sS -X POST "http://localhost:8080/chat" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"customer_id":1,"request":"I''d like to order 1 of sku COF-COL-DR-12, for delivery to 456 Oak Ave Apt B, Springfield, IL 62704 USA"}'
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
  -d '{"customer_id":1,"request":"What is the inventory for product_id 2 at store_id 1, 2, and 3?"}'
```

## Run in Kubernetes  

### Create Secrets

Create Kubernetes secrets for the OpenAI API key and database passwords: 

``` bash
kubectl create secret generic agentic-ai-secret --from-literal=openai_api_key='<your Open AI API Key>'
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

Build Docker images and push them to the local container repository at `localhost:9999`:

``` bash
docker compose build postgresql
docker compose build app

docker push localhost:9999/agentic-ai-demo-db:1.0
docker push localhost:9999/agentic-ai-demo-app:1.0
```

### Deploy the Application

Next, we can deploy our application to Kubernetes: 

``` bash
kubectl apply -f ./kubernetes.yaml
```

### Test the Application

``` bash
kubectl port-forward service/agentic-ai-demo-app 8080:8080
```

Send a pickup order:

``` bash
curl -sS -X POST "http://localhost:8080/chat" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"customer_id":1,"request":"I''d like to order 2 of sku COF-COL-DR-12 and 1 of sku KIT-CB-START, for pickup at store_id 1."}'
```