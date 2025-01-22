---
title: Add Instrumentation to Dockerfile
linkTitle: 6. Add Instrumentation to Dockerfile
weight: 6
time: 10 minutes
---

Now that we've successfully Dockerized our application, let's add in OpenTelemetry instrumentation. 

This is similar to the steps we took when instrumenting the application running on Linux, but there 
are some key differences to be aware of. 

## Update the Dockerfile 

Let's update the `Dockerfile` in the `/home/splunk/workshop/docker-k8s-otel/helloworld` directory.  

After the .NET application is built in the Dockerfile, we want to: 

* Add dependencies needed to download and execute `splunk-otel-dotnet-install.sh`
* Download the Splunk OTel .NET installer
* Install the distribution

We can add the following to the build stage of the Dockerfile. Let's open the Dockerfile in vi:

``` bash
vi /home/splunk/workshop/docker-k8s-otel/helloworld/Dockerfile
```
> Press the i key to enter edit mode in vi

> Paste the code beneath 'NEW CODE' into your Dockerfile in the build stage section:

``` dockerfile
# CODE ALREADY IN YOUR DOCKERFILE:
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
ARG BUILD_CONFIGURATION=Release
WORKDIR /src
COPY ["helloworld.csproj", "helloworld/"]
RUN dotnet restore "./helloworld/./helloworld.csproj"
WORKDIR "/src/helloworld"
COPY . .
RUN dotnet build "./helloworld.csproj" -c $BUILD_CONFIGURATION -o /app/build

# NEW CODE:
# Add dependencies for splunk-otel-dotnet-install.sh
RUN apt-get update && \
	apt-get install -y unzip

# Download Splunk OTel .NET installer
RUN curl -sSfL https://github.com/signalfx/splunk-otel-dotnet/releases/latest/download/splunk-otel-dotnet-install.sh -O

# Install the distribution
RUN sh ./splunk-otel-dotnet-install.sh
```

Next, we'll update the final stage of the Dockerfile with the following changes: 

* Copy the /root/.splunk-otel-dotnet/ from the build image to the final image 
* Copy the entrypoint.sh file as well 
* Set the `OTEL_SERVICE_NAME` and `OTEL_RESOURCE_ATTRIBUTES` environment variables 
* Set the `ENTRYPOINT` to `entrypoint.sh` 

It's easiest to simply replace the entire final stage with the following:

> **IMPORTANT** replace `$INSTANCE` in your Dockerfile with your instance name,
> which can be determined by running `echo $INSTANCE`.

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

> To save your changes in vi, press the `esc` key to enter command mode, then type `wq!` followed by pressing the `enter/return` key.

You can find the final version of the Dockerfile in the 
`/home/splunk/workshop/docker-k8s-otel/docker` directory. 


## Create the entrypoint.sh file

We also need to create a file named `entrypoint.sh` in the `/home/splunk/workshop/docker-k8s-otel/helloworld` folder 
with the following content: 

``` bash
vi /home/splunk/workshop/docker-k8s-otel/helloworld/entrypoint.sh
```
Then paste the following code into the newly created file:

``` bash
#!/bin/sh
# Read in the file of environment settings
. /$HOME/.splunk-otel-dotnet/instrument.sh

# Then run the CMD
exec "$@"
```
> To save your changes in vi, press the `esc` key to enter command mode, then type `wq!` followed by pressing the `enter/return` key.

The `entrypoint.sh` script is required for sourcing environment variables from the instrument.sh script, 
which is included with the instrumentation. This ensures the correct setup of environment variables 
for each platform.

> You may be wondering, why can't we just include the following command in the Dockerfile to do this, 
> like we did when activating OpenTelemetry .NET instrumentation on our Linux host? 
> ``` dockerfile
> RUN . $HOME/.splunk-otel-dotnet/instrument.sh
> ```
> The problem with this approach is that each Dockerfile RUN step runs a new container and a new shell. 
> If you try to set an environment variable in one shell, it will not be visible later on.
> This problem is resolved by using an entry point script, as we've done here. 
> Refer to this [Stack Overflow post](https://stackoverflow.com/questions/55921914/how-to-source-a-script-with-environment-variables-in-a-docker-build-process) 
> for further details on this issue. 

## Build the Docker Image 

Let's build a new Docker image that includes the OpenTelemetry .NET instrumentation: 

``` bash
docker build -t helloworld:1.1 .
```

> Note: we've used a different version (1.1) to distinguish the image from our earlier version. 
> To clean up the older versions, run the following command to get the container id:  
> ``` bash
> docker ps -a
> ```
> Then run the following command to delete the container: 
> ``` bash
> docker rm <old container id> --force
> ```
> Now we can get the container image id:
> ``` bash
> docker images | grep 1.0
> ```
> Finally, we can run the following command to delete the old image: 
> ``` bash
> docker image rm <old image id>
> ```

## Run the Application 

Let's run the new Docker image: 

``` bash
docker run --name helloworld \
--detach \
--expose 8080 \
--network=host \
helloworld:1.1
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