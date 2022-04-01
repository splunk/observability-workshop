---
title: ECS-Fargate
type: docs
---
### Splunk APM Trace Generator Demo For AWS ECS Fargate

This repo demonstrates reference implemenations for a single AWS ECS Fargate task example of Splunk APM that will send spans to a sidecar OpenTelemetry container.

ECS works very simply: just add the environment variables required by the Otel APM Instrumentation and the Instrumentation will do the rest.

To deploy this example, you must have an ECS environment ready to go with VPC, task roles for logs, etc. Instructions are below:  

- Install ECS CLI: [ECS CLI Setup](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_AWSCLI_Fargate.html)

- Pay critical attention to setting up VPC in advance: [Task Definition Guide](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definitions.html)

- Set up log environment here: [Cloudwatch](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_cloudwatch_logs.html)

---
### Setup

Configure ECS CLI Profile:  
```bash
ecs-cli \
configure profile \
--access-key YOURAWSKEYHERE \
--secret-key YOURAWSSECRETKEYHERE \
--profile-name ecs-ec2-profile
```

Configure ECS Cluster:  
```bash
configure ECS Cluster Config:
ecs-cli configure \
--cluster test-cluster \
--config-name test-cluster \
--region YOURREGIONHEREi.e.:us-east-1
```

Create ECS Cluster:
```bash
aws ecs create-cluster --cluster-name test-cluster
```

---
### Deploy Task 

The task spins up two ECS Fargate containers:

- `splunk-otel-collector` - sidecar to observe ECS host metrics and relay application traces to Splunk APM  
- `tracegen-fargate` - generates traces using a manually instrumented Java app and sends them to the Otel Collector  

Deploy with the following commands- *you must change the variables in caps in* `tracegen-java-otel-fargate-otelcolfargate.json` *to suit your environment:*

Create cluster
```bash
aws ecs create-cluster --cluster-name test-cluster
```

Note that the task definition will increment each time you try it- from 1 to 2 etc. To check which version is current use:  
```bash
aws ecs list-task-definitions
```

Identify your Security Group and Subnet and change them in the deploy script below and then deploy trace generator / otelcollector task to cluster:

```bash
aws ecs create-service \
--cluster test-cluster \
--service-name tracegen-fargate \
--desired-count 1 \
--launch-type "FARGATE" \
--network-configuration "awsvpcConfiguration={subnets=[subnet-YOURSUBNETHERE],securityGroups=[sg-YOURSECURITYGROUPHERE],assignPublicIp=ENABLED}" \
--task-definition tracegen-java-otel-fargate-otelcol:1
```

After a few seconds check Splunk APM and Dashboards->ECS-Fargate to see the trace generator service and Otel collector

---
### Cleanup  
```bash
aws ecs delete-service --cluster test-cluster --service tracegen-java-otel-fargate-otelcol --force
```

---
### Extras

The [ecs-cli-commands.md](../../appendix/ecs-cli-commands/) file offers helpful commands for ECS Fargate management for the AWS CLI.