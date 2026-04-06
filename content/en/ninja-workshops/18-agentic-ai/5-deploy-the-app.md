---
title: Deploy the Agentic AI Application
linkTitle: 5. Deploy the Agentic AI Application
weight: 5
time: 15 minutes
---

## Deploy the Agentic AI Application (Linux)

We'll start by running the application directly on our Linux EC2 instance.

### Set Environment Variables

In the command terminal, configure the following environment variables which 
tell the application how to connect to an OpenAI model hosted in Azure:  

> Note: the workshop instructor will provide the values for `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_API_KEY`.

``` bash
export AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4.1-mini
export AZURE_OPENAI_API_VERSION=2024-12-01-preview
export AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
export AZURE_OPENAI_API_KEY=your_azure_openai_api_key
```

### Create Virtual Environment

Next, we'll create a Python virtual environment and install the packages needed to
run the application:

``` bash
cd ~/workshop/agentic-ai/base-app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run the Application

Then we can run the application with the following command:

``` bash
python3 main.py
```

### Test the Application

Open a second terminal session connected to your EC2 instance, and run the following
command to test the application:

``` bash
curl http://localhost:8080/travel/plan \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "Seattle",
    "destination": "Tokyo",
    "user_request": "We are planning a week-long trip to Seattle from Tokyo. Looking for boutique hotel, business-class flights and unique experiences.",
    "travelers": 2
  }'
```

## Deploy the Agentic AI Application (Kubernetes)

Now that the application is working successfully, let's deploy it to Kubernetes. 

### Create a Dockerfile

A pre-built the Dockerfile can be found in the file named
`~/workshop/agentic-ai/base-app/Dockerfile`. We can see that all the 
packages in the `requirements.txt` file are installed as part of building 
the Docker image: 

````
RUN pip install --no-cache-dir -r requirements.txt
````

The container is started with the following command: 

````
CMD ["python", "main.py"]
````

### Build the Docker Image 

``` bash
cd ~/workshop/agentic-ai/base-app
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:base-app .
docker push localhost:9999/agentic-ai-app:base-app
```

### Create Secret with Azure Credentials

We'll use a Kubernetes secret to store the Azure OpenAI endpoint and key:

> Note: the workshop instructor will provide the values for `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_API_KEY`.

``` bash
kubectl create ns travel-agent

kubectl create secret generic azure-openai-api -n travel-agent --from-literal=azure-openai-api-endpoint=your_azure_openai_api_endpoint --from-literal=azure-openai-api-key=your_azure_openai_api_key
```

### Deploy the Application Using the Kubernetes Manifest File

A pre-built Kubernetes manifest can be found in the file named
`~/workshop/agentic-ai/base-app/k8s.yaml`.

We can deploy the application using the manifest file as follows: 

``` bash
kubectl apply -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### Test the Application in Kubernetes 

Run the following command to test the application:

``` bash
curl http://travel-planner.localhost/travel/plan \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "Seattle",
    "destination": "Tokyo",
    "user_request": "We are planning a week-long trip to Seattle from Tokyo. Looking for boutique hotel, business-class flights and unique experiences.",
    "travelers": 2
  }'
```