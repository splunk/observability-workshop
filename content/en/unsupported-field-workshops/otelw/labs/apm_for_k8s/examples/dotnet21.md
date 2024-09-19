---
title: .Net Core 2.1
weight: 3
---
.NET CORE example uses the .NET http client to get non-responding URL so makes valid traces with 403 status code

Containerized with these [instructions from Microsoft](https://docs.microsoft.com/en-us/dotnet/core/docker/build-container?tabs=windows)

**For .NET Core 2.1** 

```
cd ~/otelworkshop/k8s/dotnet21
```

Deploy:  
```
source deploy-client.sh
```

Delete deployment:
```
source delete-all.sh
```