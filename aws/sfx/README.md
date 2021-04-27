# Instructions on how to set up AWS cloud integration

Set the following variables:

- `aws_region`: Which region do you want the instances in?
- `signalfx_realm`: Which Observability Cloud realm to send to?
- `signalfx_api_access_token`: A Observability Cloud user API access token. *Not* an org token. The user needs to be an admin.
- `signalfx_aws_integration_name`: This name shows up in the Observability Cloud integrations UI. We suggest you use your first name or initials.

Sample command:

```
terraform apply \
-auto-approve \
-var="aws_region=eu-central-1" \
-var="signalfx_realm=eu0" \
-var="signalfx_api_access_token=YOURTOKENHERE" \
-var="signalfx_aws_integration_name=AWS-$USER"
```

