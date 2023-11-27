---
title: OpenTelemetry Collector プロセッサー
linkTitle: 4.2 Resource Detection
weight: 2
---

## Resource Detection プロセッサー

**resourcedetection** プロセッサーは、ホストからリソース情報を検出して、テレメトリーデータ内のリソース値をこの情報で追加または上書きすることができます。

デフォルトでは、可能であればホスト名を FQDN に設定し、そうでなければ OS が提供するホスト名になります。このロジックは `hostname_sources` オプションを使って変更できます。FQDN を取得せず、OSが提供するホスト名を使用するには、`hostname_sources`を`os`に設定します。

{{% tab title="System Resource Detection Processor Configuration" %}}

``` yaml {hl_lines="3-7"}
processors:
  batch:
  resourcedetection/system:
    detectors: [system]
    system:
      hostname_sources: [os]
```

{{% /tab %}}

If the workshop instance is running on an AWS/EC2 instance we can gather the following tags from the EC2 metadata API (this is not available on other platforms).
ワークショップのインスタンスが AWS/EC2 インスタンスで実行されている場合、EC2 のメタデータ API から以下のタグを収集します（これは他のプラットフォームでは利用できないものもあります）。

- `cloud.provider ("aws")`
- `cloud.platform ("aws_ec2")`
- `cloud.account.id`
- `cloud.region`
- `cloud.availability_zone`
- `host.id`
- `host.image.id`
- `host.name`
- `host.type`

これらのタグをメトリクスに追加するために、別のプロセッサーとして定義してみましょう。

{{% tab title="EC2 Resource Detection Processor Configuration" %}}

``` yaml {hl_lines="7-8"}
processors:
  batch:
  resourcedetection/system:
    detectors: [system]
    system:
      hostname_sources: [os]
  resourcedetection/ec2:
    detectors: [ec2]
```

{{% /tab %}}
