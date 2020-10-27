# Instructions on how to set up cloud instances for participants

Set the following variables:

- `aws_instance_count`: how many instances?
- `aws_instance_type`: what kind of instance?
- `aws_region`: which region do you want the instances in?
- `signalFxApiAccessToken`: a SignalFx user API access token. *Not* an org token. The user needs to be an admin.
- `signalFxAWSIntegrationName`: this name shows up in the SignalFx integrations UI. We suggest you use your first name or initials.
- `signalFxRealm`: Which SignalFx realm to send to.

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
