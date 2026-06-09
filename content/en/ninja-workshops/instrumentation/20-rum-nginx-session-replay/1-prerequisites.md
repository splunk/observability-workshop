---
title: 1. Prerequisites
linkTitle: 1. Prerequisites
weight: 1
---

Before you enable Digital Experience Analytics (DXA), make sure the browser application is ready to send Splunk RUM data with enough session context for behavior analysis.

## Required Splunk values

- **Realm**: your Splunk Observability Cloud realm, such as `us1`, `eu0`, or `au0`.
- **RUM access token**: the browser RUM token used by the front-end application.
- **Application name**: the RUM application name that will be added to a DXA project.
- **Deployment environment**: for example `workshop`, `staging`, or `production`.
- **Application version**: a release number, build SHA, or deploy identifier.
- **DXA access**: Digital Experience Analytics must be available in your Splunk Observability Cloud organization.

{{% notice title="DXA data source" style="info" %}}
DXA does not require a separate browser SDK. It uses events collected by Splunk RUM. For browser applications, use Splunk RUM browser agent version 2.0.0 or later and keep anonymous user tracking enabled so DXA can correlate behavior across sessions.
{{% /notice %}}

## Required tools

For the local lab you need:

- Docker or a compatible container runtime.
- `curl`.
- A browser with developer tools.
- Access to Splunk Observability Cloud if you want to verify live RUM and DXA data.

The local Docker lab runs over HTTP so you can inspect the nginx injection quickly. Production RUM collection should run from pages, scripts, and API requests served over HTTPS.

## Create the local environment file

Copy the example environment file:

```bash
cd workshop/rum-nginx-session-replay
cp .env.example .env
```

Edit `.env` and replace the placeholder values:

```bash
SPLUNK_RUM_REALM=us1
SPLUNK_RUM_ACCESS_TOKEN=replace-with-your-rum-token
SPLUNK_RUM_APPLICATION_NAME=dxa-rum-workshop
SPLUNK_RUM_APP_VERSION=1.0.0
SPLUNK_RUM_ENVIRONMENT=workshop
SPLUNK_RUM_AGENT_VERSION=v3
DEMO_PORT=8088
```

The sample uses `v3`, which tracks the current v3 release line from the Splunk CDN. In tightly controlled production environments, pin an exact version and add Subresource Integrity after testing that version.

{{% notice title="Element picker note" style="tip" %}}
DXA's element picker works best against a page that your browser can open while you are signed in to Splunk Observability Cloud. For purely local demos, use the manual event-definition steps in this workshop if the picker cannot reach `localhost`.
{{% /notice %}}
