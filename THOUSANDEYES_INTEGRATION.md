# ThousandEyes Integration Added

This document describes the ThousandEyes integration scenario that has been added to the Splunk Observability Workshop.

## Location

The new scenario is located at:
- **Content**: `content/en/scenarios/thousandeyes-integration/`
- **Workshop Files**: `workshop/synthetics/`

## Structure

The scenario includes:

1. **Overview** (`1-overview/`) - ThousandEyes agent types and architecture
2. **Deployment** (`2-deployment/`) - Kubernetes deployment instructions
3. **Splunk Integration** (`3-splunk-integration/`) - OpenTelemetry integration setup
4. **Kubernetes Testing** (`4-kubernetes-testing/`) - Internal service monitoring
5. **Troubleshooting** (`5-troubleshooting/`) - Common issues and solutions

## Workshop Files

The following configuration files are available in `workshop/synthetics/`:
- `credentialsSecret.yaml` - Kubernetes secret template for ThousandEyes token
- `thousandEyesDeploy.yaml` - ThousandEyes agent deployment manifest

## Media

All images and GIFs from the original guide have been copied to:
`content/en/scenarios/thousandeyes-integration/images/`

## Accessing the Workshop

Once the Hugo site is built, the workshop will be accessible at:
`/scenarios/thousandeyes-integration/`

## Testing Locally

To test the new scenario locally:

```bash
cd observability-workshop
hugo server -D
```

Then navigate to: http://localhost:1313/scenarios/thousandeyes-integration/
