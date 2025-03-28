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

But first, let's define some key terms. 

## Key Terms 

### What is Docker?  

_"Docker provides the ability to package and run an application in a loosely isolated environment
called a container. The isolation and security lets you run many containers simultaneously on
a given host. Containers are lightweight and contain everything needed to run the application,
so you don't need to rely on what's installed on the host."_

Source:  https://docs.docker.com/get-started/docker-overview/

### What is a container? 

_"Containers are isolated processes for each of your app's components. Each component
...runs in its own isolated environment, 
completely isolated from everything else on your machine."_

Source:  https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/

### What is a container image?

_"A container image is a standardized package that includes all of the files, binaries,
libraries, and configurations to run a container."_

### Dockerfile 

_"A Dockerfile is a text-based document that's used to create a container image. It provides
instructions to the image builder on the commands to run, files to copy, startup command, and more."_

## Create a Dockerfile 

Let's create a file named `Dockerfile` in the `/home/splunk/workshop/docker-k8s-otel/helloworld` directory. 

``` bash
cd /home/splunk/workshop/docker-k8s-otel/helloworld
```

You can use vi or nano to create the file. We will show an example using vi:

``` bash
vi Dockerfile
```
Copy and paste the following content into the newly opened file:

> Press 'i' to enter into insert mode in vi before pasting the text below.

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

> To save your changes in vi, press the `esc` key to enter command mode, then type `:wq!` followed by pressing the `enter/return` key.


What does all this mean?  Let's break it down. 

## Walking through the Dockerfile 

We've used a multi-stage Dockerfile for this example, which separates the Docker image creation process into the following stages: 

* Base
* Build
* Publish
* Final

While a multi-stage approach is more complex, it allows us to create a 
lighter-weight runtime image for deployment.  We'll explain the purpose of 
each of these stages below. 

### The Base Stage

The base stage defines the user that will 
be running the app, the working directory, and exposes 
the port that will be used to access the app. 
It's based off of Microsoft's `mcr.microsoft.com/dotnet/aspnet:8.0` image: 

``` dockerfile
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
USER app
WORKDIR /app
EXPOSE 8080
```

Note that the `mcr.microsoft.com/dotnet/aspnet:8.0` image includes the .NET runtime only, 
rather than the SDK, so is relatively lightweight. It's based off of the Debian 12 Linux 
distribution.  You can find more information about the ASP.NET Core Runtime Docker images 
in [GitHub](https://github.com/dotnet/dotnet-docker/blob/main/README.aspnet.md). 

### The Build Stage

The next stage of the Dockerfile is the build stage.  For this stage, the 
`mcr.microsoft.com/dotnet/sdk:8.0` image is used, which is also based off of 
Debian 12 but includes the full [.NET SDK](https://github.com/dotnet/dotnet-docker/blob/main/README.sdk.md) rather than just the runtime.  

This stage copies the `.csproj` file to the build image, and then uses `dotnet restore` to 
download any dependencies used by the application. 

It then copies the application code to the build image and 
uses `dotnet build` to build the project and its dependencies into a 
set of `.dll` binaries: 

``` dockerfile
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
ARG BUILD_CONFIGURATION=Release
WORKDIR /src
COPY ["helloworld.csproj", "helloworld/"]
RUN dotnet restore "./helloworld/./helloworld.csproj"
WORKDIR "/src/helloworld"
COPY . .
RUN dotnet build "./helloworld.csproj" -c $BUILD_CONFIGURATION -o /app/build
```

### The Publish Stage

The third stage is publish, which is based on build stage image rather than a Microsoft image.  In this stage, `dotnet publish` is used to 
package the application and its dependencies for deployment: 

``` dockerfile
FROM build AS publish
ARG BUILD_CONFIGURATION=Release
RUN dotnet publish "./helloworld.csproj" -c $BUILD_CONFIGURATION -o /app/publish /p:UseAppHost=false
```

### The Final Stage 

The fourth stage is our final stage, which is based on the base 
stage image (which is lighter-weight than the build and publish stages). It copies the output from the publish stage image and 
defines the entry point for our application: 

``` dockerfile
FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .

ENTRYPOINT ["dotnet", "helloworld.dll"]
```

## Build a Docker Image

Now that we have the `Dockerfile`, we can use it to build a Docker image containing 
our application: 

{{< tabs >}}
{{% tab title="Script" %}}
``` bash
docker build -t helloworld:1.0 .
```
{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
DEPRECATED: The legacy builder is deprecated and will be removed in a future release.
            Install the buildx component to build images with BuildKit:
            https://docs.docker.com/go/buildx/

Sending build context to Docker daemon  281.1kB
Step 1/19 : FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
8.0: Pulling from dotnet/aspnet
af302e5c37e9: Pull complete 
91ab5e0aabf0: Pull complete 
1c1e4530721e: Pull complete 
1f39ca6dcc3a: Pull complete 
ea20083aa801: Pull complete 
64c242a4f561: Pull complete 
Digest: sha256:587c1dd115e4d6707ff656d30ace5da9f49cec48e627a40bbe5d5b249adc3549
Status: Downloaded newer image for mcr.microsoft.com/dotnet/aspnet:8.0
 ---> 0ee5d7ddbc3b
Step 2/19 : USER app
etc,
```
{{% /tab %}}
{{< /tabs >}}

This tells Docker to build an image using a tag of `helloworld:1.0` using the `Dockerfile` in the current directory. 

We can confirm it was created successfully with the following command: 

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
docker images
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
helloworld   1.0       db19077b9445   20 seconds ago   217MB
```

{{% /tab %}}
{{< /tabs >}}

## Test the Docker Image

> Before proceeding, ensure the application we started before is no longer running on your instance. 

We can run our application using the Docker image as follows: 

``` bash
docker run --name helloworld \
--detach \
--expose 8080 \
--network=host \
helloworld:1.0
```

> Note: we've included the `--network=host` parameter to ensure our Docker container 
> is able to access resources on our instance, which is important later on when we need 
> our application to send data to the collector running on localhost. 

Let's ensure that our Docker container is running: 

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
docker ps
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
$ docker ps
CONTAINER ID   IMAGE            COMMAND                  CREATED       STATUS       PORTS     NAMES
5f5b9cd56ac5   helloworld:1.0   "dotnet helloworld.d…"   2 mins ago    Up 2 mins              helloworld
```

{{% /tab %}}
{{< /tabs >}}

We can access our application as before:

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
curl http://localhost:8080/hello/Docker
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
Hello, Docker! 
```

{{% /tab %}}
{{< /tabs >}}

Congratulations, if you've made it this far, you've successfully Dockerized a .NET application. 