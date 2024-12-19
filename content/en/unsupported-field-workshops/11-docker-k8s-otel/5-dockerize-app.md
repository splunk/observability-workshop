---
title: Dockerize the Application
linkTitle: 5. Dockerize the Application
weight: 5
time: 15 minutes
---

Later on in this workshop, we're going to deploy our .NET application into a Kubernetes cluster. 

But how do we do that?  

The first step is to create a Docker image for our application.  This is known as 
"dockerizing" and application, and the process begins with the creation of a `Dockerfile`. 

## Create a Dockerfile 

Let's create a file named `Dockerfile` in the `/home/splunk/workshop/docker-k8s-otel/helloworld directory.  

It should include the following content: 

``` dockerfile
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
USER app
WORKDIR /app
EXPOSE 8080

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
ARG BUILD_CONFIGURATION=Release
WORKDIR /src
COPY ["helloworld.csproj", "helloworld/"]
RUN dotnet restore "./helloworld/./helloworld.csproj"
WORKDIR "/src/helloworld"
COPY . .
RUN dotnet build "./helloworld.csproj" -c $BUILD_CONFIGURATION -o /app/build

FROM build AS publish
ARG BUILD_CONFIGURATION=Release
RUN dotnet publish "./helloworld.csproj" -c $BUILD_CONFIGURATION -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .

ENTRYPOINT ["dotnet", "helloworld.dll"]
```

What does all this mean?  Let's break it down. 

## Walking through the Dockerfile 

TODO 

## Build a Docker Image

Now that we have the `Dockerfile`, we can use it to build a Docker image containing 
our application: 

``` bash
docker build -t helloworld:1.0 .
```

This tells Docker to build an image using a tag of `helloworld:1.0` using the `Dockerfile` in the current directory. 

We can confirm it was created successfully with the following command: 

``` bash
docker images
```

## Test the Docker Image

> Before proceeding, ensure the application we started before is no longer running on your instance. 

We can run our application using the Docker image as follows: 

``` bash
docker run --name diceroll \
--detach \
--expose 8080 \
--network=host \
helloworld:1.0
```

> Note: we've included the `--network=host` parameter to ensure our Docker container 
> is able to access resources on our instance, which is important later on when we need 
> our application to send data to the collector running on localhost. 

We can access our application as before: 

``` bash
curl http://localhost:8080
```

As before, it should return `Hello, World!`. 

Congratulations, if you've made it this far, you've successfully Dockerized a .NET application. 