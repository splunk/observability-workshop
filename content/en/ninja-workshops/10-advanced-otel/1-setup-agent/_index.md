---
title: Agent Setup
linkTitle: 1. Agent Setup
time: 10 minutes
---

In the location you are going to run the workshop on you machine, (we will use [WORKSHOP] for this location), create a sub directory called **1-agent** and  move into it.

In *[WORKSHOP]/1-agent* create  a file called **agent.yaml** 



``` text
receivers:

exporters:
    
processors:
  memory_limiter:
    check_interval: 2s
    limit_mib: 512
  
service:
  pipelines:
    traces:
    metrics:
    logs:
```



```text
otelcol_darwin_arm64 --config=agent-file.yaml
```


```text
curl -X POST -i http://localhost:4318/v1/traces \
-H "Content-Type: application/json" \
 -d @trace.json 
```
