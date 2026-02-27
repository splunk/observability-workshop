---
title: 1. Configure and Start the Stack
weight: 1
---

## Add Your Splunk Credentials

{{% notice title="Exercise" style="green" icon="running" %}}

Navigate to the Phase 1/2 directory and open `docker-compose.yaml` in your editor:

``` bash
cd ~/workshop/obi/02-obi-docker
vim docker-compose.yaml #or editor of choise
```

Find the `splunk-otel-collector` service and replace the four placeholder values with your real credentials:  
**Note:** if needed you can obtain your `ACCESS_TOKEN`, `REALM`, and `INSTANCE` using `env` in your environment

``` yaml
    environment:
      SPLUNK_INGEST_TOKEN: "YOUR_TOKEN_HERE"              # <-- Your Splunk ingest token
      SPLUNK_REALM: "YOUR_REALM"                          # <-- Your realm (us0, us1, eu0, etc.)
      WORKSHOP_HOST_NAME: "<example: shw-ece9>"           # <-- the value from INSTANCE when you use `env` on terminal
      WORKSHOP_ENVIRONMENT: "<example: shw-ece9-ebpf>"    # <-- The hostname value above suffixed with `-ebpf`
```

Save the file.

{{% /notice %}}

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
**Why `WORKSHOP_HOST_NAME` and `WORKSHOP_ENVIRONMENT`?** Everyone in the workshop sends telemetry to the same Splunk org. These values become the `host.name` and `deployment.environment` attributes on all your metrics and traces, so you can filter to **your** data in Splunk.
{{% /notice %}}

## Start the Stack

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
docker-compose up --build -d
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
[+] Building 12.3s (24/24) FINISHED
[+] Running 6/6
 ✔ Container 02-obi-docker-payment-service-1      Started
 ✔ Container 02-obi-docker-order-processor-1       Started
 ✔ Container 02-obi-docker-frontend-1              Started
 ✔ Container 02-obi-docker-splunk-otel-collector-1 Started
 ✔ Container 02-obi-docker-load-generator-1        Started
```

{{% /tab %}}
{{< /tabs >}}

This builds the three application images from source and starts:

- **frontend** on [http://localhost:3000](http://localhost:3000)
- **order-processor** on port 8080
- **payment-service** on port 8081
- **splunk-otel-collector** receiving telemetry on ports 4317/4318
- **load-generator** automatically hitting `/create-order` every 2 seconds
