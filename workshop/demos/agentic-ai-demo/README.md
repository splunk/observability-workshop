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

Ask a question about an order: 

``` bash
curl -sS -X POST "http://localhost:8080/chat" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"customer_id":1,"request":"What products were included in my most recent order?"}'
```

Ask a question about an order amounts:

``` bash
curl -sS -X POST "http://localhost:8080/chat" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"customer_id":1,"request":"What was the total dollar amount of my most recent order?"}'
```

Ask a question that requires product info? 

``` bash
curl -sS -X POST "http://localhost:8080/chat" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"customer_id":1,"request":"Can you describe the product that I''ve ordered most frequently? Please include the price and total quantity ordered."}'
```

### Send a test order 

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

## Run in Kubernetes  

Coming soon. 