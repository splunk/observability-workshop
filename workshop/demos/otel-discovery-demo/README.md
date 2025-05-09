# OpenTelemetry Discovery Demo

Please refer to the demo script in Google Docs for details on how to 
setup and run this demo.  It can be run on both Linux as well as 
Kubernetes. 

## Build steps (not required for demo)

The Kubernetes version of this demo can be delivered using the pre-built Docker images. 
Follow the instructions below in the event that you need to build your own images.

### Build the loan service image and push to Docker Hub

Change the platform architecture to `linux/arm64` if required:

``` bash
    docker build --tag loanservice --platform linux/amd64 src/loanservice
    docker tag loanservice:latest derekmitchell399/loanservice:v0.0.1
    docker image push derekmitchell399/loanservice:v0.0.1
```

### Build the risk service image and push to Docker Hub

Change the platform architecture to `linux/arm64` if required:

``` bash
    docker build --tag riskservice --platform linux/amd64 src/riskservice
    docker tag riskservice:latest derekmitchell399/riskservice:v0.0.1
    docker image push derekmitchell399/riskservice:v0.0.1
```

