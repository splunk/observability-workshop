# Instructions on how to set up EC2 cloud instances for participants

Set the following variables:

- `aws_region`: Which region do you want the instances in?
- `instance_type`: What kind of instance?
- `aws_instance_count`: How many instances?

Sample command:

```
terraform apply \
-auto-approve \
-var="aws_region=eu-central-1" \
-var="instance_type=1" \
-var="aws_instance_count=1"
```

