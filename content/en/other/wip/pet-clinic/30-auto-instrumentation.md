---
title: Setting up Auto instrumentation for APM
linkTitle: 3. Auto-instrumentation & APM
weight: 30
---

## 1. setting up the Java auto instrumentation

Patch all the deployments (labeled with `app.kubernetes.io/part-of=spring-petclinic`) to add the inject annotation.
 **This automatically causes pods to restart.**

```bash
kubectl get deployments -l app.kubernetes.io/part-of=spring-petclinic -o name | xargs -I % kubectl patch % -p "{\"spec\": {\"template\":{\"metadata\":{\"annotations\":{\"instrumentation.opentelemetry.io/inject-java\":\"true\"}}}}}"
```
