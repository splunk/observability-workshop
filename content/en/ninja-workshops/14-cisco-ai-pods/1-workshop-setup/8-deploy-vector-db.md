---
title: Deploy the Vector Database
linkTitle: 8. Deploy the Vector Database
weight: 8
time: 10 minutes
---

In this step, we'll deploy a vector database to the OpenShift cluster and populate it with
test data that will be used by workshop participants.

## Deploy a Vector Database

For the workshop, we'll deploy an open-source vector database named
[Weaviate](https://weaviate.io/).

First, add the Weaviate helm repo that contains the Weaviate helm chart:

``` bash
helm repo add weaviate https://weaviate.github.io/weaviate-helm
helm repo update
```

The `weaviate/weaviate-values.yaml` file includes the configuration we'll use to deploy
the Weviate vector database.

We've set the following environment variables to `TRUE`, to ensure Weaviate exposes
metrics that we can scrape later with the Prometheus receiver:

````
  PROMETHEUS_MONITORING_ENABLED: true
  PROMETHEUS_MONITORING_GROUP: true
````

Review [Weaviate documentation](https://docs.weaviate.io/deploy/installation-guides/k8s-installation)
to explore additional customization options available.

Let's create a new namespace:

``` bash
oc create namespace weaviate
```

Run the following command to allow Weaviate to run a privileged container:

> Note: this approach is not recommended for production environments

``` bash
oc adm policy add-scc-to-user privileged -z default -n weaviate
```

Then deploy Weaviate:

``` bash
helm upgrade --install \
  "weaviate" \
  weaviate/weaviate \
  --namespace "weaviate" \
  --values ./weaviate/weaviate-values.yaml
```

## Populate the Vector Database

Now that Weaviate is up and running, let's add some data to it 
that we'll use in the workshop with a custom application.

The application used to do this is based on
[LangChain Playbook for NeMo Retriever Text Embedding NIM](https://docs.nvidia.com/nim/nemo-retriever/text-embedding/latest/playbook.html#generate-embeddings-with-text-embedding-nim).

Per the configuration in `./load-embeddings/k8s-job.yaml`, we're going to load
a [datasheet for the NVIDIA H200 Tensor Core GPU](https://nvdam.widen.net/content/udc6mzrk7a/original/hpc-datasheet-sc23-h200-datasheet-3002446.pdf)
into our vector database.

This document includes information about NVIDIA's H200 GPUs that our large language model
isn't trained on. And in the next part of the workshop, we'll build an application that
uses an LLM to answer questions using the context from this document, which will be loaded
into the vector database.

We'll deploy a Kubernetes Job to our OpenShift cluster to load the embeddings.
A Kubernetes Job is used rather than a Pod to ensure that this process runs only once:

``` bash
oc create namespace llm-app
oc apply -f ./load-embeddings/k8s-job.yaml
```

> Note: to build a Docker image for the Python application that loads the embeddings
> into Weaviate, we executed the following commands:
> ``` bash
> cd workshop/cisco-ai-pods/load-embeddings
> docker build --platform linux/amd64 -t derekmitchell399/load-embeddings:1.0 .
> docker push derekmitchell399/load-embeddings:1.0
> ```
