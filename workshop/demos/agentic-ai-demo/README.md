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

## Run in Kubernetes  

Coming soon. 