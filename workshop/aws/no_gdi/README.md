# Running the Observability Workshop without the GDI portions

This document will walk through how to run the main Observability Workshop without having the customers use the AWS instance(s) to send data in.

This will be accomplished by having the instructor deploy instance(s) which they can toggle as the workshop goes on.

## Outline

* Setup users as you would for an other workshop
* Deploy a single instance (instead of one per student)
* Login to that instance
* Workshops
  * Splunk IMT
    * Deploy the collector with helm
    * Deploy the Nginx app
* Splunk APM
  * Deploy the Online Boutique shop
  * Generate traffic using Locust
* Splunk RUM
  * Obtain a RUM token
  * Deploy RUM-based Online Boutique
  * Generate traffic using Locust

The subsequent sections will provide more direct instructions; however since the workshop is subject to change it is recommended to refer to the specific steps in the workshop to conduct those steps.

## Steps

Assumption: Users are created for the workshop as you would any other workshop.

### Deploy the instance(s)

Follow the instructions [here](../ec2/README.md) with the instance count of 1.

Take the ip address and login as normal. Username is ubuntu and password can be found [here](../../cloud-init/k3s.yaml).

For example:
```
ssh ubuntu@<ipaddress>
Enter password
```

You can use more than one instance if you want to keep each of the apps running; just amend these instructions to not delete the previous deployment.

### IMT: Deploy Collector

Get the access token and realm for the org you are using and run:
```
export ACCESS_TOKEN=<replace_with_O11y-Workshop-ACCESS_token>
export REALM=<replace_with_splunk_realm>

helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart && helm repo update

helm install splunk-otel-collector \
--set="splunkObservability.realm=$REALM" \
--set="splunkObservability.accessToken=$ACCESS_TOKEN" \
--set="clusterName=$(hostname)-k3s-cluster" \
--set="splunkObservability.logsEnabled=true" \
--set="splunkObservability.profilingEnabled=true" \
--set="environment=$(hostname)-apm-env" \
splunk-otel-collector-chart/splunk-otel-collector \
-f ~/workshop/k3s/otel-collector.yaml
```

You can verify your deployment (as well as the future deployments) with:
```
kubectl get pods
```

### IMT: Deploy Nginx

You can do this ahead of time or during the workshop. It has a little more effect when you do it during the workshop because you can be showing the attendees the pods coming in as they are deployed. It is definitely recommended to run the last command (locust deployment) with the attendees so they can see the effect in the charts.

```
cd ~/workshop/k3s/nginx
kubectl create configmap nginxconfig --from-file=nginx.conf
kubectl create -f nginx-deployment.yaml
kubectl create -f locust-deployment.yaml
```

### APM

Depending on if you are running from a single instance or multiple you may wish to remove the previous app. (It may or may not be necessary to.)

To remove the Nginx app from IMT:
```
cd ~/workshop/k3s/nginx
kubectl delete -f nginx-deployment.yaml
kubectl delete -f locust-deployment.yaml
```

To deploy the APM app:
```
cd ~/workshop/apm
./apm-config.sh
kubectl apply -f deployment.yaml
```

### RUM

The APM app must be removed before running the RUM app. (Or you can use multiple instances.)

You will need a RUM token from your org.

To remove the APM app:
```
cd ~/workshop/apm
kubectl delete -f deployment.yaml
```

To deploy the RUM app:
```
export RUM_TOKEN=<replace_with_O11y-Workshop-RUM-TOKEN>
cd ~/workshop/apm
kubectl delete -f deployment.yaml
./apm-config.sh -r
kubectl apply -f deployment.yaml
```

## Other Notes

In the instructions for the APM and RUM app deployments it makes a mention of if there are any messages about a VARIABLE being unset to run:
```
kubectl delete -f deployment.yaml
```
Then export your variables correctly and redeploy:
```
kubectl apply -f deployment.yaml
```