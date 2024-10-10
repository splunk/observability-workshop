---
title: 'Node.js- Deploy HTTP Client'
weight: 4
---

Make sure that you still have the Python Flask server from the Python Lab running. If you accidentally shut it down follow steps from the Python lab to restart the Python Flask server.

## Start in the Node example directory

**Open a new terminal window** 

```bash
cd ~/otelworkshop/host/node
```

## Configure Node.js environment

During `npm init` below you can use all defaults when prompted:  

```bash
npm init && \
npm install @splunk/otel --save && \
npm install @opentelemetry/instrumentation-http --save
```

## Run .js HTTP.get requests client

Set up environment and run the node app with HTTP.get requests
!!! important
    If you are doing this workshop as part of a group, before the next step, add your initials do the APM environment:
    edit the `run-client.sh` script below and add your initials to the environment i.e. change:  
    `export OTEL_RESOURCE_ATTRIBUTES=deployment.environment=apm-workshop`  
    to    
    `export OTEL_RESOURCE_ATTRIBUTES=deployment.environment=sjl-apm-workshop`  
      
```bash
source run-client.sh
```

You will see requests printed to the window

## APM Dashboard

Traces / services will now be viewable in the APM dashboard. A new service takes about 90 seconds to register for the firs time, and then all data will be available in real time.

Additionally span IDs will print in the terminal where flask-server.py is running. You can use ++ctrl+c++ to stop the requests and server any time. You should now see a Node requests service alongside the Python and Java ones.  

![Node](../../../images/14-node.png)

![Node Traces](../../../images/15-nodetraces.png)

![Node Spans](../../../images/16-nodespans.png)

## Where is the OpenTelemetry Instrumentation?

You can see in the `run-client.sh` how the environment has been set up for OpenTelemtry and where the autoinstrumentation takes place as the node app runs.

Splunk's Otel autoinstrumentation for node.js is [here](https://github.com/signalfx/splunk-otel-js)