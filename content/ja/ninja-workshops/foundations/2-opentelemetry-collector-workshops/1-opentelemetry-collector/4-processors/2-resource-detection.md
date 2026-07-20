---
title: OpenTelemetry Collector Processors
linkTitle: 4.2 Resource Detection
weight: 2
---

## Resource Detection Processor

**resourcedetection** Processorは、ホストからリソース情報を検出し、テレメトリデータのリソース値にその情報を追加または上書きするために使用できます。

デフォルトでは、ホスト名は可能であればFQDNに設定され、それ以外の場合はOSが提供するホスト名がフォールバックとして使用されます。このロジックは `hostname_sources` 設定オプションを使用して変更できます。FQDNを取得せずにOSが提供するホスト名を使用するために、`hostname_sources` を `os` に設定します。

{{% tab title="System Resource Detection Processor設定" %}}

``` yaml {hl_lines="3-7"}
processors:
  batch:
  resourcedetection/system:
    detectors: [system]
    system:
      hostname_sources: [os]
```

{{% /tab %}}

ワークショップインスタンスがAWS/EC2インスタンスで実行されている場合、EC2メタデータAPIから以下のタグを取得できます（他のプラットフォームでは利用できません）。

- `cloud.provider ("aws")`
- `cloud.platform ("aws_ec2")`
- `cloud.account.id`
- `cloud.region`
- `cloud.availability_zone`
- `host.id`
- `host.image.id`
- `host.name`
- `host.type`

これらのタグをメトリクスに追加するために、別のProcessorを作成します。

{{% tab title="EC2 Resource Detection Processor設定" %}}

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
