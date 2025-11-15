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

### Send a test order 

Send a pickup order: 

``` bash
curl -X POST "http://localhost:8080/orders" \
-H "Content-Type: application/json" \
-d '{
  "customer_info": {
    "customer_id": 1
  },
  "order_type": "pickup",
  "items": [
    {"sku": "COF-COL-DR-12", "quantity": 2},
    {"sku": "KIT-CB-START", "quantity": 1}
  ],
  "store_id": 1
}'
```

Send a delivery order: 

``` bash
curl -X POST "http://localhost:8080/orders" \
-H "Content-Type: application/json" \
-d '{
  "customer_info": {
    "customer_id": 1
  },
  "order_type": "delivery",
  "items": [
    {"sku": "COF-COL-DR-12", "quantity": 1}
  ],
  "shipping_address": {
    "line1": "456 Oak Ave",
    "line2": "Apt B",
    "city": "Springfield",
    "state": "IL",
    "postal_code": "62704",
    "country": "USA"
  }
}'
```

Get orders for a specific customer:

``` bash
curl "http://localhost:8080/get_orders_for_customer?customer_id=1"
```

Send a question: 

``` bash
curl -sS -X POST "http://localhost:8080/ask_question" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"customer_id":1,"question":"What is the total dollar amount of all my orders? Just provide the amount, not the details."}'
```

## Run in Kubernetes  

Coming soon. 