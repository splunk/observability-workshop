# Instructions on how to set up cloud instances for participants

Set the following variables:

- `aws_region`: Which region do you want the instances in?
- `instance_type`: What kind of instance?
- `aws_instance_count`: How many instances?
- `signalfx_realm`: Which SignalFx realm to send to?
- `signalfx_api_access_token`: A SignalFx user API access token. *Not* an org token. The user needs to be an admin.
- `signalfx_aws_integration_name`: This name shows up in the SignalFx integrations UI. We suggest you use your first name or initials.

Sample command:

```
terraform apply \
-auto-approve \
-var="aws_region=eu-central-1" \
-var="instance_type=1" \
-var="aws_instance_count=1" \
-var="signalfx_realm=eu0" \
-var="signalfx_api_access_token=YOURTOKENHERE" \
-var="signalfx_aws_integration_name=AWS-$USER"
```

To disable rollout of the AWS integration, set `-var="signalfx_aws_integration_enabled=0"`.
