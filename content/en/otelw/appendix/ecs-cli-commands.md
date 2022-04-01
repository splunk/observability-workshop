---
title: 'ECS-CLI Commands'
type: docs
weight: 3
---
#### Create

`aws ecs create-cluster --cluster-name YOURCLUSTERNAMEHERE`   
`aws ecs register-task-definition --cli-input-json file://YOURTASKDEFINITIONHERE.json`   

`aws ecs create-service --cluster test-cluster --service-name signalfx-demo --task-definition signalfx-demo:1 \`   
`--desired-count 1 --launch-type "FARGATE" \`   
`--network-configuration "awsvpcConfiguration={subnets=[subnet-YOURSUBNETIDHERE],securityGroups=[sg-YOURSECURITYGROUPIDHERE],assignPublicIp=ENABLED}"`

#### Monitor   
    
`aws ecs list-task-definitions`   
`aws ecs list-clusters`  
`aws ecs list-services --cluster YOURCLUSTERNAMEHERE`   
`aws ecs describe-services --cluster YOURCLUSTERNAMEHERE --services YOURSERVICENAMEHERE`   

#### Cleanup   
    
`aws ecs deregister-task-definition --task-definition FAMILYNAMEHERE:VERSIONHERE`   
`aws ecs delete-service --cluster YOURCLUSTERNAMEHERE --service YOURSERVICENAMEHERE --force`   
`aws ecs delete-cluster --cluster YOURCLUSTERNAMEHERE`  
`ecs-cli down --cluster YOURCLUSTERNAMEHERE --region YOURREGIONHERE`
