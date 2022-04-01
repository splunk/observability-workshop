---
title: ECS-EC2
type: docs
---
### Splunk APM Trace Generator Demo For AWS ECS EC2

This repo demonstrates a reference implemenation for a single AWS ECS EC2 task example of Splunk APM that will send spans directly to Splunk Observability Cloud.  

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

Configure ECS EC2 Cluster:  
```bash
configure ECS Cluster Config:
ecs-cli configure \
--cluster test-cluster \
--config-name test-cluster \
--region YOURREGIONHEREi.e.:us-east-1
```

Deploy ECS EC2 Cluster:
```bash
ecs-cli up \
--cluster test-cluster \
--region YOURREGIONHEREi.e.:us-east-1\
--size 1 \
--capability-iam \
--instance-type t2.xlarge \
--launch-type EC2 \
--ecs-profile test-profile \
--force
```
---
### Deploy Task

Deploy with the following commands- *you must change the variables in caps in these task .json files to suit your environment:*

```bash
aws ecs register-task-definition \
--cli-input-json file://tracegen-java-otel-ecs-ec2.json
```

Note that the task definition will increment each time you try it- from 1 to 2 etc. To check which version is current use:  
```bash
aws ecs list-task-definitions
```

Deploy trace generator task to cluster:

```bash
aws ecs create-service \
--cluster test-cluster \
--launch-type EC2 \
--scheduling-strategy DAEMON \
--service-name tracegen-java-otel-ecs-ec2 \
--task-definition tracegen-java-otel-ecs-ec2:VERSIONHEREi.e.1
```

After a few seconds check Splunk APM to see the trace generator service.

---
### Cleanup  
```bash
aws ecs delete-service --cluster test-cluster --service tracegen-java-otel-ecs-ec2 --force
```
```bash
ecs-cli down \
--cluster test-cluster \
--region us-east-1
```
```bash
aws ecs delete-cluster --cluster test-cluster
```

---
### Extras

The [ecs-cli-commands.md](../../appendix/ecs-cli-commands/) file offers helpful commands for ECS Fargate management for the AWS CLI.