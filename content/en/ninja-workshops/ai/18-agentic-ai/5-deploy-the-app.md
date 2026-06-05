---
title: Deploy the Agentic AI Application
linkTitle: 5. Deploy the Agentic AI Application
weight: 5
time: 15 minutes
---

## Deploy the Agentic AI Application (Linux)

We'll start by running the application directly on our Linux EC2 instance.

### Set Environment Variables

Your EC2 instance includes the following pre-set environment variables, which
tell the application how to connect to an
OpenAI model hosted in Azure (via Lite LLM Proxy).

* `OPENAI_API_KEY`
* `OPENAI_BASE_URL`

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
command to test the application. It should return the suggested travel plans in json format:

{{< tabs >}}
{{% tab title="Script" %}}

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

{{% /tab %}}
{{% tab title="Example Output" %}}

```json
{"activities_summary":"Sure! Here are signature activities for a week in Tokyo:\n\n1. Day 1: Explore Asakusa and Senso-ji Temple, then stroll Nakamise Shopping Street.\n2. Day 2: Visit Tsukiji Outer Market for fresh sushi breakfast, then tour Ginza for upscale shopping.\n3. Day 3: Spend the day in Shibuya\u2014cross the famous scramble, visit Hachiko statue, and shop in trendy boutiques.\n4. Day 4: Explore Harajuku\u2019s Takeshita Street and Meiji Shrine, followed by Omotesando\u2019s stylish cafes.\n5. Day 5: Discover Akihabara\u2019s electronics and anime culture, with a visit to a themed caf\u00e9.\n6. Day 6: Take a day trip to Odaiba for teamLab Borderless digital art museum and waterfront views.\n7. Day 7: Relax in Ueno Park, visit museums, and shop at Ameya-Yokocho market.\n\nWould you like hotel or dining recommendations as well?","agent_steps":[{"agent":"coordinator","status":"completed"},{"agent":"flight_specialist","status":"completed"},{"agent":"hotel_specialist","status":"completed"}
```

{{% /tab %}}
{{< /tabs >}}

### Stop the Application

Once you've confirmed that the application is working successfully, return to your first terminal and stop the application.

## Deploy the Agentic AI Application (Kubernetes)

Now that the application is working successfully, let's deploy it to Kubernetes.

### Build the Docker Image

In this section, we'll use the Dockerfile located at `~/workshop/agentic-ai/base-app/Dockerfile`
to build a Docker image for the application. Run the following commands to build the image:

``` bash
cd ~/workshop/agentic-ai/base-app
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:base-app .
docker push localhost:9999/agentic-ai-app:base-app
```

> [!TIP]
> If the image is taking too long to build, consider using the pre-built
> image instead. To do so, update the image name in
> the `~/workshop/agentic-ai/base-app/k8s.yaml` file to `ghcr.io/splunk/agentic-ai-app:base-app`
> instead of `localhost:9999/agentic-ai-app:base-app`.

### Create Application Namespace

Let's create a new namespace to host our application:

``` bash
kubectl create ns travel-agent
```

### Create Secret with the OpenAI Credentials

We'll use a Kubernetes secret to store the OpenAI endpoint and key:

``` bash
{ [ -z "$OPENAI_API_KEY" ] || \
  [ -z "$OPENAI_BASE_URL" ]; } && \
  echo "Error: Missing variables" || \
  kubectl create secret generic openai-api \
  -n travel-agent \
  --from-literal=openai-api-endpoint=$OPENAI_BASE_URL \
  --from-literal=openai-api-key=$OPENAI_API_KEY
```

> [!NOTE]
> If you get an error that says Missing variables, you’ll need to
> manually define environment variables to connect to OpenAI API before
> running this command.

### Deploy the Application Using the Kubernetes Manifest File

A pre-built Kubernetes manifest can be found in the file named
`~/workshop/agentic-ai/base-app/k8s.yaml`.

We can deploy the application using the manifest file as follows:

``` bash
kubectl apply -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### Ensure the Application is Running

Use the following command to ensure the application pod has a
status of `Running`:

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl get pods -n travel-agent
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
NAME                                        READY   STATUS    RESTARTS   AGE
travel-planner-langchain-68977dc5c4-4w7p9   1/1     Running   0          41s
```

{{% /tab %}}
{{< /tabs >}}

### Test the Application in Kubernetes

Run the following command to test the application:

{{< tabs >}}
{{% tab title="Script" %}}

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

{{% /tab %}}
{{% tab title="Example Output" %}}

```json
{"activities_summary":"Sure! Here are signature activities for a week in Tokyo:\n\n1. Day 1: Explore Asakusa and Senso-ji Temple, then stroll Nakamise Shopping Street.\n2. Day 2: Visit Tsukiji Outer Market for fresh sushi breakfast, then tour Ginza for upscale shopping.\n3. Day 3: Spend the day in Shibuya\u2014cross the famous scramble, visit Hachiko statue, and shop in trendy boutiques.\n4. Day 4: Explore Harajuku\u2019s Takeshita Street and Meiji Shrine, followed by Omotesando\u2019s stylish cafes.\n5. Day 5: Discover Akihabara\u2019s electronics and anime culture, with a visit to a themed caf\u00e9.\n6. Day 6: Take a day trip to Odaiba for teamLab Borderless digital art museum and waterfront views.\n7. Day 7: Relax in Ueno Park, visit museums, and shop at Ameya-Yokocho market.\n\nWould you like hotel or dining recommendations as well?","agent_steps":[{"agent":"coordinator","status":"completed"},{"agent":"flight_specialist","status":"completed"},{"agent":"hotel_specialist","status":"completed"}
```

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

If you need to troubleshoot, use the following command to view the application logs:

```bash
kubectl logs -l app=travel-planner-langchain -n travel-agent -f
```
