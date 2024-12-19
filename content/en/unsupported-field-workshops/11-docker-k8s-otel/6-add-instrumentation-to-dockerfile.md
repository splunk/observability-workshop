---
title: Add Instrumentation to Dockerfile
linkTitle: 6. Add Instrumentation to Dockerfile
weight: 6
time: 10 minutes
---

Now that we've successfully Dockerized our application, let's add in OpenTelemetry instrumentation. 

This is similar to steps we took when instrumenting the application running on Linux, but there 
are some key differences to be aware of. 

## Update the Dockerfile 

Let's update the `Dockerfile` in the `/home/splunk/workshop/docker-k8s-otel/helloworld` directory.  

After the .NET application is built in the Dockerfile, we want to: 

* Add dependencies needed to download and execute `splunk-otel-dotnet-install.sh`
* Download the Splunk OTel .NET installer
* Install the distribution

We can add the following to the Dockerfile to do so: 

``` dockerfile
RUN dotnet build "./diceroll-app.csproj" -c $BUILD_CONFIGURATION -o /app/build

# Add dependencies for splunk-otel-dotnet-install.sh
RUN apt-get update && \
	apt-get install -y unzip

# Download Splunk OTel .NET installer
RUN curl -sSfL https://github.com/signalfx/splunk-otel-dotnet/releases/latest/download/splunk-otel-dotnet-install.sh -O

# Install the distribution
RUN sh ./splunk-otel-dotnet-install.sh
```

Next, we'll update the Dockerfile to make the following changes to the final image: 

* Copy the /root/.splunk-otel-dotnet/ from the build image to the final image 
* Copy the entrypoint.sh file as well 
* Set the `OTEL_SERVICE_NAME` and `OTEL_RESOURCE_ATTRIBUTES` environment variables 
* Set the `ENTRYPOINT` to `entrypoint.sh` 

``` dockerfile 
FROM base AS final

# Copy instrumentation file tree
WORKDIR "//home/app/.splunk-otel-dotnet"
COPY --from=build /root/.splunk-otel-dotnet/ .

WORKDIR /app
COPY --from=publish /app/publish .
COPY entrypoint.sh .

ENV OTEL_SERVICE_NAME=helloworld
ENV OTEL_RESOURCE_ATTRIBUTES='deployment.environment=otel-$INSTANCE'

ENTRYPOINT ["sh", "entrypoint.sh"]
CMD ["dotnet", "helloworld.dll"]
```

You can find the final version of the Dockerfile in the 
`/home/splunk/workshop/docker-k8s-otel/helloworld/docker` directory. 

> Note: replace `$INSTANCE` in your Dockerfile with your instance name, 
> which can be determined by running `echo $INSTANCE`.

## Create the entrypoint.sh file

We also need to create a file named `entrypoint.sh` in the `/home/splunk/workshop/docker-k8s-otel/helloworld` folder 
with the following content: 

``` bash
#!/bin/sh
# Read in the file of environment settings
. /$HOME/.splunk-otel-dotnet/instrument.sh

# Then run the CMD
exec "$@"
```

## Build the Docker Image 

Let's build a new Docker image that includes the OpenTelemetry .NET instrumentation: 

``` bash
docker build -t diceroll:1.1 .
```

> Note: we've used a different version (1.1) to distinguish the image from our earlier version. 
> To clean up the older versions, run the following command to get the container id:  
> ``` bash
> docker ps -a
> ```
> Then run the following command to delete the container: 
> docker rm <old container id> --force
> Finally, we can run the following command to delete the old image: 
> docker image rm <old image id>

## Run the Application 

Let's run the new Docker image: 

``` bash
docker run --name diceroll \
--detach \
--expose 8080 \
--network=host \
diceroll:1.1
```

We can access the application using: 

``` bash
curl http://localhost:8080/hello
```

Execute the above command a few times to generate some traffic.  

After a minute or so, confirm that you see new traces in Splunk Observability Cloud. 

> Remember to look for traces in your particular Environment. 
 
## Troubleshooting

If you don't see traces appear in Splunk Observability Cloud, what can you do to troubleshoot? 