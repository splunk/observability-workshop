---
title: Deploy an LLM
linkTitle: 6. Deploy an LLM
weight: 6
time: 20 minutes
---

In this section, we'll use the NVIDIA NIM Operator to deploy a Large Language Model 
to our OpenShift Cluster. 

## Create a Namespace

``` bash
oc create namespace nim-service
```

## Add Secrets with NGC API Key

Add secrets that include your NGC API key:

> Note: this secret might have already been created with the steps in 
> the previous section. 

``` bash
oc create secret -n nim-service docker-registry ngc-secret \
    --docker-server=nvcr.io \
    --docker-username='$oauthtoken' \
    --docker-password=<ngc-api-key>
```

``` bash
oc create secret -n nim-service generic ngc-api-secret \
    --from-literal=NGC_API_KEY=<ngc-api-key>
```

## Cache Models

Create a new file named `cache-all.yaml` with the following contents:

``` yaml
apiVersion: apps.nvidia.com/v1alpha1
kind: NIMCache
metadata:
  name: meta-llama3-8b-instruct
spec:
  source:
    ngc:
      modelPuller: nvcr.io/nim/meta/llama3-8b-instruct:1.0.3
      pullSecret: ngc-secret
      authSecret: ngc-api-secret
      model:
        engine: tensorrt_llm
        tensorParallelism: "1"
  storage:
    pvc:
      create: true
      storageClass: gp3-csi
      size: "50Gi"
      volumeAccessMode: ReadWriteMany
  resources: {}
---
apiVersion: apps.nvidia.com/v1alpha1
kind: NIMCache
metadata:
  name: nv-embedqa-e5-v5
spec:
  source:
    ngc:
      modelPuller: nvcr.io/nim/nvidia/nv-embedqa-e5-v5:1.0.4
      pullSecret: ngc-secret
      authSecret: ngc-api-secret
      model:
        profiles:
        - all
  storage:
    pvc:
      create: true
      storageClass: gp3-csi
      size: "50Gi"
      volumeAccessMode: ReadWriteMany
  resources: {}
---
apiVersion: apps.nvidia.com/v1alpha1
kind: NIMCache
metadata:
  name: nv-rerankqa-mistral-4b-v3
spec:
  source:
    ngc:
      modelPuller: nvcr.io/nim/nvidia/nv-rerankqa-mistral-4b-v3:1.0.4
      pullSecret: ngc-secret
      authSecret: ngc-api-secret
      model:
        profiles:
        - all
  storage:
    pvc:
      create: true
      storageClass: gp3-csi
      size: "50Gi"
      volumeAccessMode: ReadWriteMany
  resources: {}
```

Then apply the manifest:

``` bash
oc apply -n nim-service -f cache-all.yaml
```

Confirm a persistent volume and claim are created:

``` bash
oc get -n nim-service pvc,pv
```

## Deploy LLMs 

Create a new file named `service-all.yaml` with the following contents: 

``` yaml
apiVersion: apps.nvidia.com/v1alpha1
kind: NIMService
metadata:
  name: meta-llama3-8b-instruct
spec:
  image:
    repository: nvcr.io/nim/meta/llama3-8b-instruct
    tag: 1.0.3
    pullPolicy: IfNotPresent
    pullSecrets:
      - ngc-secret
  authSecret: ngc-api-secret
  storage:
    nimCache:
      name: meta-llama3-8b-instruct
      profile: ''
  replicas: 1
  resources:
    limits:
      nvidia.com/gpu: 1
  expose:
    service:
      type: ClusterIP
      port: 8000
---
apiVersion: apps.nvidia.com/v1alpha1
kind: NIMService
metadata:
  name: nv-embedqa-e5-v5
spec:
  image:
    repository: nvcr.io/nim/nvidia/nv-embedqa-e5-v5
    tag: 1.0.4
    pullPolicy: IfNotPresent
    pullSecrets:
      - ngc-secret
  authSecret: ngc-api-secret
  storage:
    nimCache:
      name: nv-embedqa-e5-v5
      profile: ''
  replicas: 1
  resources:
    limits:
      nvidia.com/gpu: 1
  expose:
    service:
      type: ClusterIP
      port: 8000
---
apiVersion: apps.nvidia.com/v1alpha1
kind: NIMService
metadata:
  name: nv-rerankqa-mistral-4b-v3
spec:
  image:
    repository: nvcr.io/nim/nvidia/nv-rerankqa-mistral-4b-v3
    tag: 1.0.4
    pullPolicy: IfNotPresent
    pullSecrets:
      - ngc-secret
  authSecret: ngc-api-secret
  storage:
    nimCache:
      name: nv-rerankqa-mistral-4b-v3
      profile: ''
  replicas: 1
  resources:
    limits:
      nvidia.com/gpu: 1
  expose:
    service:
      type: ClusterIP
      port: 8000
```

Then apply the manifest: 

``` bash
oc apply -n nim-service -f service-all.yaml
```

Confirm that it's running: 

``` bash
oc describe nimservices.apps.nvidia.com -n nim-service
```