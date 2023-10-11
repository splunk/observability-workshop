---
title: Environment Setup
weight: 60
---

Notes for the Splunk Show team on how the environment is configured.

## GitHub Repository

[https://github.com/splunk/o11y-field-demos/tree/main/o11y-datagens/online-boutique](https://github.com/splunk/o11y-field-demos/tree/main/o11y-datagens/online-boutique)

## Setup EC2 Instance

Run `install.sh` to install all the pre-requisites (K3s, Helm, etc.)

## Install cert-manager

``` bash
helm repo add jetstack https://charts.jetstack.io && helm repo update
```

``` bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.12.4/cert-manager.crds.yaml
```

``` bash
helm install \
  cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.12.4 \
  --set prometheus.enabled=false \
  --set webhook.timeoutSeconds=4
```

### Configure Issuer

``` yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    # The ACME server URL
    server: https://acme-v02.api.letsencrypt.org/directory
    # Email address used for ACME registration
    email: user@example.com
    # Name of a secret used to store the ACME account private key
    privateKeySecretRef:
      name: letsencrypt-prod
    # Enable the HTTP-01 challenge provider
    solvers:
      - http01:
          ingress:
            ingressClassName: traefik
```

### Deploy Ingress Resource

``` yaml
apiVersion: networking.k8s.io/v1 
kind: Ingress
metadata:
  name: frontend
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    traefik.ingress.kubernetes.io/custom-response-headers: "Access-Control-Allow-Origin:*||Access-Control-Allow-Methods:GET,POST,OPTIONS||Access-Control-Allow-Headers:DNT,User-Age
nt,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range||Access-Control-Expose-Headers:Content-Length,Content-Range"
    ingress.kubernetes.io/custom-response-headers: "Access-Control-Allow-Origin:*||Access-Control-Allow-Methods:GET,POST,OPTIONS||Access-Control-Allow-Headers:DNT,User-Agent,X-Req
uested-With,If-Modified-Since,Cache-Control,Content-Type,Range||Access-Control-Expose-Headers:Content-Length,Content-Range"
spec:
  ingressClassName: traefik
  tls:
  - hosts:
    - example.example.com
    secretName: quickstart-example-tls
  rules:
  - host: example.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend
            port:
              number: 80
```

## Deploy Splunk OpenTelemetry Collector

### Frontend Demo Collector

Change into the `opentelemetry-collector` directory and edit the `frontend-setup-eu.sh` or `frontend-setup-us.sh` scripts and change **<ACCESS_TOKEN>** and **<HEC_TOKEN>** to your own tokens.

Make sure `otel-base.yaml` and `splunk-defaults.yaml` are in the same directory as the setup script.

### Profiling Demo Collector

Change into the `opentelemetry-collector` directory and edit the `profiling-setup-eu.sh` or `profiling-setup-us.sh` scripts and change **<ACCESS_TOKEN>** and **<HEC_TOKEN>** to your own tokens.

Make sure `otel-base.yaml` and `splunk-defaults.yaml` are in the same directory as the setup script.

## Deploy the Online Boutique

### Frontend Demo

Change into the `frontend-demo` directory and edit `frontend-eu-deployment.yaml` and `frontend-us-deployment.yaml` and search for **<RUM_ACCESS_TOKEN>** and replace with a valid RUM Access Token for the respective Observability Cloud Org.

Apply the deployment files into their respective Observability Cloud Orgs:

{{< tabs >}}
{{% tab title="EU Splunk Show" %}}

```bash
kubectl apply -f frontend-eu-deployment.yaml
```

{{% /tab %}}
{{% tab title="US Splunk Show" %}}

```bash
kubectl apply -f frontend-us-deployment.yaml
```

{{% /tab %}}
{{< /tabs >}}

### Profiling Demo

Change into the `profiling-demo` directory and edit `profiling-eu-deployment.yaml` and `profiling-us-deployment.yaml` and search for **<RUM_ACCESS_TOKEN>** and replace with a valid RUM Access Token for the respective Observability Cloud Org.

Apply the deployment files into their respective Observability Cloud Orgs:

{{< tabs >}}
{{% tab title="EU Splunk Show" %}}

```bash
kubectl apply -f frontend-eu-deployment.yaml
```

{{% /tab %}}
{{% tab title="US Splunk Show" %}}

```bash
kubectl apply -f frontend-us-deployment.yaml
```

{{% /tab %}}
{{< /tabs >}}
