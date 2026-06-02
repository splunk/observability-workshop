---
title: API の例
linkTitle: 8. API の例
weight: 8
time: 5 minutes
description: 利用可能な API の例
---

## ThousandEyes API の利用

プログラムによる統合を行う場合は、以下の API コマンドを使用します。

### HTTP プロトコル

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

### gRPC プロトコル

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

`streamEndpointUrl` と `X-SF-Token` の値は、ご利用の Splunk Observability Cloud インスタンスに合わせた正しい値に置き換えてください。

{{% notice title="Note" style="info" %}}
`{REALM}` は使用している Splunk 環境の realm（例: `us1`、`us2`、`eu0`）に、`{TOKEN}` は実際の Splunk アクセストークンに置き換えてください。
{{% /notice %}}
