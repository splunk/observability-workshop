# Instructions on how to set up cloud instances for participants

Set the following variables:

- `gcp_project`: Your existing GCP project.
- `gcp_region`: Which region do you want the instances in?
- `gcp_instance_count`: How many instances?
- `signalfx_realm`: Which SignalFx realm to send to?
- `signalfx_api_access_token`: A SignalFx user API access token. *Not* an org token. The user needs to be an admin.
- `signalfx_gcp_integration_name`: This name shows up in the SignalFx integrations UI. We suggest you use your first name or initials.

Sample command:

```
terraform apply \
-auto-approve \
-var="gcp_project=o11y-goes-gcp" \
-var="gcp_region=europe-west3-a" \
-var="gcp_instance_count=1" \
-var="signalfx_realm=eu0" \
-var="signalfx_api_access_token=YOURTOKENHERE" \
-var="signalfx_gcp_integration_name=GCP-$USER"
```

To disable rollout of the GCP integration, set `-var="signalfx_gcp_integration_enabled=0"`.
