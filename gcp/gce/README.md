# Instructions on how to set up GCE cloud instances for participants

Set the following variables:

- `gcp_project`: Your existing GCP project.
- `gcp_zone`: Which zone do you want the instances in?
- `gcp_instance_count`: How many instances?

Sample command:

```
terraform apply \
-auto-approve \
-var="gcp_project=o11y-goes-gcp" \
-var="gcp_zone=europe-west3-a" \
-var="gcp_instance_count=1"
```

