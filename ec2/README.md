# Instructions on how to set up cloud instances for participants

Set the following variables:

- `aws_instance_count`: How many instances?
- `aws_instance_type`: What kind of instance?
- `aws_region`: Which region do you want the instances in?
- `signalFxRealm`: Which SignalFx realm to send to?
- `signalFxApiAccessToken`: A SignalFx user API access token. *Not* an org token. The user needs to be an admin.
- `signalFxAWSIntegrationName`: This name shows up in the SignalFx integrations UI. We suggest you use your first name or initials.

Sample command:

```
terraform apply \
-auto-approve \
-var="aws_instance_count=1" \
-var="instance_type=1" \
-var="aws_region=eu-central-1" \
-var="signalFxRealm=eu0" \
-var="signalFxApiAccessToken=YOURTOKENHERE" \
-var="signalFxAWSIntegrationName=AWS-$USER"
```

To disable rollout of the AWS integration, set `-var="signalFxAWSIntegrationEnabled=0"`.
