---
title: Deploy a .NET Application
linkTitle: 3. Deploy a .NET Application
weight: 3
time: 10 minutes
---

## Prerequisites 

Before deploying the application, we'll need to install the .NET 8 SDK on our instance.

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
sudo apt-get update && \
  sudo apt-get install -y dotnet-sdk-8.0
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
TBD
```

{{% /tab %}}
{{< /tabs >}}

Refer to [Install .NET SDK or .NET Runtime on Ubuntu](https://learn.microsoft.com/en-us/dotnet/core/install/linux-ubuntu-install?tabs=dotnet8&pivots=os-linux-ubuntu-2404)
for further details.

## Review the .NET Application

In the terminal, navigate to the application directory: 

``` bash
cd ~/workshop/docker-k8s-otel/helloworld
```

We'll use a simple "Hello World" .NET application for this workshop.  The main logic is found 
in the Program.cs file: 

``` cs 
using System.Globalization;

using Microsoft.AspNetCore.Mvc;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

string Hello([FromServices]ILogger<Program> logger, string? name)
{
    if (string.IsNullOrEmpty(name))
    {
        logger.LogInformation("Hello, World!);
    }
    else
    {
        logger.LogInformation("Hello, {result}!", name);
    }

    return result.ToString(CultureInfo.InvariantCulture);
}

app.MapGet("/hello/{name?}", Hello);

app.Run();
```

## Build and Run the .NET Application

We can build the application using the following command: 

``` bash 
dotnet build
```

If that's successful, we can run it as follows: 

``` bash
dotnet run
```

Once it's running, open a second SSH terminal and access the application using curl: 

``` bash
curl http://localhost:8080/hello
```

It should return `Hello, World!`. 

## Next Steps

What are the two methods that we can use to instrument our application with OpenTelemetry?  

Hint:  see [Instrument your .NET application for Splunk Observability Cloud](https://docs.splunk.com/observability/en/gdi/get-data-in/application/otel-dotnet/instrumentation/instrument-dotnet-application.html) 
for a discussion of the options. 
