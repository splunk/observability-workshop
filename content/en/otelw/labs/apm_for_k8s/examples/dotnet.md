---
title:  .Net Setup
weight: 2
---

.NET CORE example uses the .NET http client to get non-responding URL so makes valid traces with 403 status code

Containerized with these [instructions from Microsoft](https://docs.microsoft.com/en-us/dotnet/core/docker/build-container?tabs=windows)

**.NET Core 5** 

```
cd ~/otelworkshop/k8s/dotnet
```

Deploy:  
```
source deploy-client.sh
```

Delete deployment:
```
source delete-all.sh
```

**.NET Core 2.1** 
.NET Core 2.1 [located here](dotnet21.md)