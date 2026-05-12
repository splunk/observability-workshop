---
title: API Examples
linkTitle: 9. API Examples
weight: 9
time: 5 minutes
description: API Examples you can use
---

### Using the ThousandEyes API

For a programmatic integration, use the following API commands:

#### HTTP Protocol

```bash
curl -v -XPOST https://api.thousandeyes.com/v7/stream \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BEARER_TOKEN" \
  -d '{
    "type": "opentelemetry",
    "testMatch": [{
      "id": "281474976717575",
      "domain": "cea"
    }],
    "endpointType": "http",
    "streamEndpointUrl": "https://ingest.{REALM}.signalfx.com:443/v2/datapoint/otlp",
    "customHeaders": {
      "X-SF-Token": "{TOKEN}",
      "Content-Type": "application/x-protobuf"
    }
  }'
```

#### gRPC Protocol

```bash
curl -v -XPOST https://api.thousandeyes.com/v7/stream \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BEARER_TOKEN" \
  -d '{
    "type": "opentelemetry",
    "testMatch": [{
      "id": "281474976717575",
      "domain": "cea"
    }],
    "endpointType": "grpc",
    "streamEndpointUrl": "https://ingest.{REALM}.signalfx.com:443",
    "customHeaders": {
      "X-SF-Token": "{TOKEN}",
      "Content-Type": "application/x-protobuf"
    }
  }'
```

Replace `streamEndpointUrl` and `X-SF-Token` values with the correct values for your Splunk Observability Cloud instance.

{{% notice title="Note" style="info" %}}
Make sure to replace `{REALM}` with your Splunk environment realm (e.g., `us1`, `us2`, `eu0`) and `{TOKEN}` with your actual Splunk access token.
{{% /notice %}}