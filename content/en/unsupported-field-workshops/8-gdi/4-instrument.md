---
title: Instrument REVIEWS for Tracing
linkTitle: 4. Instrumentation
weight: 4
---

## 1. Use Data Setup to instrument a Python application

Within the O11y Cloud UI:

Data Management -> Add Integration -> Monitor Applications -> Python (traces) -> Add Integration

Provide the following to the Configure Integration Wizard:

- Service: review

- Django: no
- collector endpoint: `http://localhost:4317`
- Environment: rtapp-workshop-[YOURNAME]
- Kubernetes: yes
- Legacy Agent: no

![o11y_cloud_ui](../images/configureintegration.png)

We are instructed to:
  
- Install the instrumentation packages for your Python environment.

``` text
pip install splunk-opentelemetry[all]
  
splunk-py-trace-bootstrap
```

- Configure the Downward API to expose environment variables to Kubernetes resources.

  For example, update a Deployment to inject environment variables by adding `.spec.template.spec.containers.env` like:

``` yaml
apiVersion: apps/v1
kind: Deployment
spec:
  selector:
    matchLabels:
      app: your-application
  template:
    spec:
      containers:
        - name: myapp
          env:
            - name: SPLUNK_OTEL_AGENT
              valueFrom:
                fieldRef:
                  fieldPath: status.hostIP
            - name: OTEL_EXPORTER_OTLP_ENDPOINT
              value: "http://$(SPLUNK_OTEL_AGENT):4317"
            - name: OTEL_SERVICE_NAME
              value: "review"
            - name: OTEL_RESOURCE_ATTRIBUTES
              value: "deployment.environment=rtapp-workshop-stevel"
```

- Enable the Splunk OTel Python agent by editing your Python service command.

  ``` text
  splunk-py-trace python3 main.py --port=8000
  ```

- The actions we must perform include:

  - Update the Dockerfile to install the splunk-opentelemetry packages
  - Update the deployment.yaml for each service to include these environment variables which will be used by the pod and container.
  - Update our Dockerfile for REVIEW so that our program is bootstrapped with splunk-py-trace

{{% notice title="Note" style="info" %}}
We will accomplish this by:

1. generating a new requirements.txt file
2. generating a new container image with an updated Dockerfile for REVIEW and then
3. update the review.deployment.yaml to capture all of these changes.

{{% /notice %}}

## 2. Update the REVIEW container

- Generate a new container image
- Update the Dockerfile for REVIEW (`/workshop/flask_apps_finish/review`)

  ``` dockerfile
  FROM python:3.10-slim

  WORKDIR /app
  COPY requirements.txt /app
  RUN pip install -r requirements.txt
  RUN pip install splunk-opentelemetry[all]
  RUN splk-py-trace-bootstrap

  COPY ./review.py /app

  EXPOSE 5000
  ENTRYPOINT [ "splunk-py-trace" ]
  CMD [ "python", "review.py" ]
  ```

{{% notice title="Note" style="info" %}}
Note that the only lines, in bold, added to the Dockerfile
{{% /notice %}}

- Generate a new container image with docker build in the ‘finished’ directory
- Notice that I have changed the repository name from `localhost:8000/review:0.01` to `localhost:8000/review-splkotel:0.01`

Ensure you are in the correct directory.

``` bash
pwd
./workshop/flask_apps_finish/review
```
  
{{< tabs >}}

{{% tab title="docker build" %}}

``` bash
docker build -f Dockerfile.review -t localhost:8000/review-splkotel:0.01 .
```

{{% /tab %}}
{{% tab title="docker build Output" %}}

``` text
[+] Building 27.1s (12/12) FINISHED
=> [internal] load build definition from Dockerfile                                                        0.0s
=> => transferring dockerfile: 364B                                                                        0.0s
=> [internal] load .dockerignore                                                                           0.0s
=> => transferring context: 2B                                                                             0.0s
=> [internal] load metadata for docker.io/library/python:3.10-slim                                         1.6s
=> [auth] library/python:pull token for registry-1.docker.io                                               0.0s
=> [1/6] FROM docker.io/library/python:3.10-slim@sha256:54956d6c929405ff651516d5ebbc204203a6415c9d2757aad  0.0s
=> [internal] load build context                                                                           0.3s
=> => transferring context: 1.91kB                                                                         0.3s
=> CACHED [2/6] WORKDIR /app                                                                               0.0s
=> [3/6] COPY requirements.txt /app                                                                        0.0s
=> [4/6] RUN pip install -r requirements.txt                                                              15.3s
=> [5/6] RUN splk-py-trace-bootstrap                                                                       9.0s
=> [6/6] COPY ./review.py /app                                                                             0.0s
=> exporting to image                                                                                      0.6s
=> => exporting layers                                                                                     0.6s
=> => writing image sha256:164977dd860a17743b8d68bcc50c691082bd3bfb352d1025dc3a54b15d5f4c4d                0.0s
=> => naming to docker.io/localhost:8000/review-splkotel:0.01                                              0.0s
```

{{% /tab %}}{{< /tabs >}}

- Push the image to Docker Hub with docker push command

{{< tabs >}}

{{% tab title="docker push" %}}

``` bash
docker push localhost:8000/review-splkotel:0.01
```
  
{{% /tab %}}
{{% tab title="docker push Output" %}}
  
``` text
The push refers to repository [docker.io/localhost:8000/review-splkotel]
682f0e550f2c: Pushed
dd7dfa312442: Pushed
917fd8334695: Pushed
e6782d51030d: Pushed
c6b19a64e528: Mounted from localhost:8000/review
8f52e3bfc0ab: Mounted from localhost:8000/review
f90b85785215: Mounted from localhost:8000/review
d5c0beb90ce6: Mounted from localhost:8000/review
3759be374189: Mounted from localhost:8000/review
fd95118eade9: Mounted from localhost:8000/review
0.01: digest: sha256:3b251059724dbb510ea81424fc25ed03554221e09e90ef965438da33af718a45 size: 2412
```

{{% /tab %}}{{< /tabs >}}
  
## 3. Update the REVIEW deployment in Kubernetes
  
- review.deployment.yaml must be updated with the following changes:
  - Load the new container image on Docker Hub
  - Add environment variables so traces can be emitted to the OTEL collector
  
- The deployment must be replaced using the updated review.deployment.yaml

  - Update review.deployment.yaml (updates highlighted in bold)

    ``` yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: review
      labels:
        app: review
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: review
      template:
        metadata:
          labels:
            app: review
        spec:
          imagePullSecrets:
            - name: regcred
          containers:
          - image: localhost:8000/review-splkotel:0.01
            name: review
            volumeMounts:
            - mountPath: /var/appdata
              name: appdata
            env:
            - name: SPLUNK_OTEL_AGENT
              valueFrom:
                fieldRef:
                  fieldPath: status.hostIP
            - name: OTEL_SERVICE_NAME
              value: 'review'
            - name: SPLUNK_METRICS_ENDPOINT
              value: "http://$(SPLUNK_OTEL_AGENT):9943"
            - name: OTEL_EXPORTER_OTLP_ENDPOINT
              value: "http://$(SPLUNK_OTEL_AGENT):4317"
            - name: OTEL_RESOURCE_ATTRIBUTES
              value: 'deployment.environment=rtapp-workshop-stevel'
          volumes:
          - name: appdata
            hostPath:
              path: /var/appdata
    ```

- Apply review.deployment.yaml. Kubernetes will automatically pick up the changes to the deployment and redeploy new pods with these updates

  - Notice that the review-* pod has been restarted

``` bash
kubectl apply -f review.deployment.yaml
```

``` bash
kubectl get pods
```

``` text
NAME                                                              READY   STATUS        RESTARTS   AGE
kafka-client                                                      0/1     Unknown       0          155d
curl                                                              0/1     Unknown       0          155d
kafka-zookeeper-0                                                 1/1     Running       0          26h
kafka-2                                                           2/2     Running       0          26h
kafka-exporter-647bddcbfc-h9gp5                                   1/1     Running       2          26h
mongodb-6f6c78c76-kl4vv                                           2/2     Running       0          26h
kafka-1                                                           2/2     Running       1          26h
kafka-0                                                           2/2     Running       1          26h
splunk-otel-collector-1653114277-agent-n4dfn                      2/2     Running       0          26h
splunk-otel-collector-1653114277-k8s-cluster-receiver-5f48v296j   1/1     Running       0          26h
splunk-otel-collector-1653114277-agent-jqxhh                      2/2     Running       0          26h
review-6686859bd7-4pf5d                                           1/1     Running       0          11s
review-5dd8cfd77b-52jbd                                           0/1     Terminating   0          2d10h

kubectl get pods
NAME                                                              READY   STATUS    RESTARTS   AGE
kafka-client                                                      0/1     Unknown   0          155d
curl                                                              0/1     Unknown   0          155d
kafka-zookeeper-0                                                 1/1     Running   0          26h
kafka-2                                                           2/2     Running   0          26h
kafka-exporter-647bddcbfc-h9gp5                                   1/1     Running   2          26h
mongodb-6f6c78c76-kl4vv                                           2/2     Running   0          26h
kafka-1                                                           2/2     Running   1          26h
kafka-0                                                           2/2     Running   1          26h
splunk-otel-collector-1653114277-agent-n4dfn                      2/2     Running   0          26h
splunk-otel-collector-1653114277-k8s-cluster-receiver-5f48v296j   1/1     Running   0          26h
splunk-otel-collector-1653114277-agent-jqxhh                      2/2     Running   0          26h
review-6686859bd7-4pf5d                                           1/1     Running   0          15s
```
