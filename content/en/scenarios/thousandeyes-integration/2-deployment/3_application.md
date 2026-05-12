---
title: Application
linkTitle: 2.3 Application
weight: 3
time: 10 minutes
description: Deploy the application
---

In this step we will deploy the sample application (Pet Clinic).

## Installation Steps

### Step 1: Deploy the Application

To deploy the app:

```bash
kubectl apply -f ~/workshop/petclinic/deployment.yaml
```

You can check that your app is deployed, along with all the other pods:

```bash
kubectl get pods
```

