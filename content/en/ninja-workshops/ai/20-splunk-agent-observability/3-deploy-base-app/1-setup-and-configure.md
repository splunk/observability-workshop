---
title: Set Up and Configure
linkTitle: 1. Set Up and Configure
weight: 1
time: 10 minutes
---

Work in the `1-base-app` folder for this chapter. These steps create the Python
environment, configure secrets, start the database, and load the sample data the agent
needs.

{{< exercise title="Set up the base application" >}}

{{< step title="Log into your lab instance" >}}

Connect to your workshop EC2 instance (your instructor will provide the connection details).
The healthcare assistant is pre-loaded under `~/workshop/healthcare-assistant/`, and your
`OPENAI_API_KEY` is already configured in the environment.

{{< /step >}}

{{< step title="Temporary step: get the latest application code" >}}

```bash
rm -Rf ~/workshop/healthcare-assistant
cd ~
git clone https://github.com/splunk/observability-workshop.git
cd observability-workshop
git checkout agent-observability-lab-te
cd workshop
cp -R healthcare-assistant ~/workshop
```

{{< /step >}}


{{< step title="Create a Kubernetes Secret" >}}

Run the following command to create a Kubernetes secret, which the application will use to 
connect to OpenAI models: 

```bash
kubectl create secret generic openai-api \
  --from-literal=openai-api-key="$OPENAI_API_KEY" \
  --from-literal=openai-api-endpoint="$OPENAI_BASE_URL"
```

{{< /step >}}

{{< step title="Create a Kubernetes Config Map" >}}

Run the following command to create a Kubernetes config map, which the store additional 
configuration parameters used by the application: 

```bash
cd ~/workshop/healthcare-assistant/1-base-app
kubectl apply -f healthcare-assistant-config.yaml
```

{{< /step >}}

{{< step title="Start the PostgreSQL Database" >}}

The healthcare assistant stores the medicine FAQ embeddings and patient records in PostgreSQL with the
`pgvector` extension. Start PostgreSQL in Kubernetes using the following command:

```bash
cd ~/workshop/healthcare-assistant/1-base-app
kubectl apply -f postgres.yaml
```

Ensure that PostgreSQL is running: 

```bash
kubectl get pods -l app=postgres
NAME                        READY   STATUS    RESTARTS   AGE
postgres-66ffcf4b8c-8s5lp   1/1     Running   0          16s
```

{{< /step >}}

{{< step title="Build the Docker Image" >}}

Change into the base app directory, then run the following command to build the Docker image
for the application: 

```bash
cd ~/workshop/healthcare-assistant
docker build -f 1-base-app/Dockerfile -t localhost:9999/healthcare-assistant:base-app .
docker push localhost:9999/healthcare-assistant:base-app
```

{{< /step >}}


{{< step title="Load vector data and relational tables" >}}

Embed the medicine FAQ into pgvector and load the patient registry into PostgreSQL. The
helper script does both:

```bash
cd ~/workshop/healthcare-assistant/1-base-app
kubectl apply -f setup-job.yaml 
```

This runs `python helpers/setup_vectordb.py local`, which creates the
`healthcare_local_index` pgvector collection from `docs/qa.csv` and the
`healthcare_patient` table from `docs/relational_patient.csv`.

Monitor the job with the following command: 

```bash
kubectl logs -f job/vectordb-setup
```

If successful, the output should include the following: 

````
Setting up vector database for healthcare in hosted environment
🔧 Environment setup complete
Using chunk_size: 1000, chunk_overlap: 200
Using embedding model: text-embedding-3-large
Creating PostgreSQL/pgvector collection: healthcare_hosted_index
Adding documents to vector store...
Loading relational tables for healthcare...
✓ Loaded relational table healthcare_patient (30 rows) from relational_patient.csv
✅ Successfully created vector database for healthcare
📊 Total documents embedded: 15
🔗 PostgreSQL collection: healthcare_hosted_index
````

{{< /step >}}

{{< /exercise >}}
