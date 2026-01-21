# Portworx Metrics 

Portworx is a software defined persistent storage solution designed and purpose 
built for applications deployed as containers, via container orchestrators 
such as Kubernetes. 

Portworx provides a Prometheus-style metrics endpoint that we scrape using the 
Splunk OpenTelemetry Collector to capture metrics from an AI POD that uses 
Pure Storage. 

This project simulates the metrics endpoint that Portworx provides, so we can 
capture metrics as part of the AI POD workshop where Portworx and 
Pure Storage are not available. 

## Build Docker Image 

Execute the following steps to build a Docker image for this functionality: 

``` bash
cd workshop/cisco-ai-pods/portworx
docker build --platform linux/amd64 -t derekmitchell399/portworx-metrics-sim:1.0 .
docker push derekmitchell399/portworx-metrics-sim:1.0
```

## Test the Functionality

Execute the following command to test the Docker image: 

``` bash
docker run -d -p 17001:17001 derekmitchell399/portworx-metrics-sim:1.0 
```

Then use curl to test the metrics endpoint: 

``` bash
curl http://localhost:17001/metrics
```

You should see output such as the following: 

````
# HELP px_cluster_cpu_percent Percentage of CPU Used
# TYPE px_cluster_cpu_percent gauge
px_cluster_cpu_percent{cluster="ocp-pxclus-32430549-ad99-4839-bf9b-d6beb8ddc2d6",clusterUUID="e870909b-6150-4d72-87cb-a012630e42ae",node="worker2.flashstack.local",nodeID="f63312a2-0884-4878-be4e-51935613aa80"} 1.91
````
