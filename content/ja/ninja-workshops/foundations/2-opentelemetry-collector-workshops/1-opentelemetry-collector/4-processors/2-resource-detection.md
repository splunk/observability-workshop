---
title: OpenTelemetry Collector Processors
linkTitle: 4.2 Resource Detection
weight: 2
---

## Resource Detection Processor

**resourcedetection** processor は、ホストからリソース情報を検出し、テレメトリデータのリソース値にこの情報を追加または上書きするために使用できます。

デフォルトでは、ホスト名は可能であれば FQDN に設定され、それ以外の場合は OS が提供するホスト名がフォールバックとして使用されます。このロジックは `hostname_sources` 設定オプションを使用して変更できます。FQDN を取得せずに OS が提供するホスト名を使用するには、`hostname_sources` を `os` に設定します。

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

ワークショップインスタンスが AWS/EC2 インスタンスで実行されている場合、EC2 メタデータ API から以下のタグを収集できます（これは他のプラットフォームでは利用できません）。

- `cloud.provider ("aws")`
- `cloud.platform ("aws_ec2")`
- `cloud.account.id`
- `cloud.region`
- `cloud.availability_zone`
- `host.id`
- `host.image.id`
- `host.name`
- `host.type`

これらのタグをメトリクスに追加するために、別の processor を作成します。

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
