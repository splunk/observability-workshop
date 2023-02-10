--- 
title: OTel Collector and APM for Docker
type: docs
---

## Docker based APM examples

---
### Prep:

Make sure you've stopped your previous workshop examples and stopped all instances of Otel Collector as to not confuse re-used example names.  

Docker must be installed and current for this lab. 

Repo location: [https://github.com/signalfx/otelworkshop/tree/main/misc/docker](https://github.com/signalfx/otelworkshop/tree/main/misc/docker)

Start in k8s directory:
```bash
cd ~/otelworkshop/misc/docker
```

Create environment variables with your Splunk token and realm- substitute yours for the variables in caps:  
```bash
export SPLUNK_ACCESS_TOKEN=YOURTOKENHERE
```
```bash
export SPLUNK_REALM=YOURREALMHERE
```

Add initals to environment i.e. sjl-apm-workshop:
```bash
export SPLUNK_WORKSHOP_ENV=YOURINITIALS-apm-workshop
```

Make sure to re-export these environment variables every time you open a terminal.

---
### Example 1: Python Microservice w/ Local Otel Collector
A local docker network with an OpenTelemetry Collector container and a container with a Python microservice example with a redis client and server in same container.  

Step 1: Create a local docker network called `otel-net`  
```bash
source setup-docker.sh
```

Step 2: Run Otel Collector docker container in the `otel-net` docker bridged network:
```bash
source run-otelcol.sh
```

Step 3: Run the Python Redis client w/ Redis server microservice example container:

Open a new terminal window. Re-export your env variables from the prep section.

```bash
source run-python-autgen.sh
```

Wait a about 60 seconds and check APM Explore map to see the microservices.

Study the run scripts to understand how OpenTelemetry environment variables are configured, and the source code for the microservice example is [here](https://github.com/signalfx/otelworkshop/tree/main/k8s/python/tools/autogen)  

`ctrl-c` in each terminal will stop things and containers can be removed via standard Docker commands.

---
### Example 2: Python Microservice Sending Telmetry Directly to Splunk Observability Cloud  

Run the direct-to-ingest docker container:
```bash
source run-python-autogen-direct.sh 
```
Wait a about 60 seconds and check APM Explore map to see the microservices.

---
### Example 3: .NET Microservice Sending Telemetry Directly to Splunk Observability Cloud

Run the direct-to-ingest docker container:
```bash
source run-dotnet-autogen-direct.sh 
```
Wait a about 60 seconds and check APM Explore map to see the microservices.

### Misc

Docker container instructions for OpenTelemetry Collector are [here](https://github.com/signalfx/splunk-otel-collector/blob/main/docs/getting-started/linux-manual.md)

View Otel Collector trace stats (requires Lynx ascii browser):
```bash
docker exec -it otelcol curl localhost:55679/debug/tracez | lynx -stdin
```