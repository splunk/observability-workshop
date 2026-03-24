---
title: Deploy the Agentic AI Application
linkTitle: 5. Deploy the Agentic AI Application
weight: 5
time: 20 minutes
---

## Deploy the Agentic AI Application

We'll start by running the application directly on our Linux EC2 instance.

### Set Environment Variables

In the command terminal, configure the following environment variables:

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
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run the Application

Then we can run the application with the following command:

``` bash
python main.py
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