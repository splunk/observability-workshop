---
title: OpenTelemetry Collector Processors
linkTitle: 4.2 Resource Detection
weight: 2
---

## Resource Detection Processor

**resourcedetection** プロセッサーは、ホストからリソース情報を検出し、その情報をテレメトリーデータのリソース値として追加または上書きするために使用できます。

デフォルトでは、可能な場合は FQDN がホスト名として設定され、それ以外の場合は OS が提供するホスト名がフォールバックとして使用されます。この動作は `hostname_sources` 設定オプションを使用して変更できます。FQDN の取得を避けて OS が提供するホスト名を使用するために、`hostname_sources` を `os` に設定します。

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

ワークショップのインスタンスが AWS/EC2 インスタンス上で実行されている場合、EC2 メタデータ API から以下のタグを取得できます（これは他のプラットフォームでは利用できません）。

- `cloud.provider ("aws")`
- `cloud.platform ("aws_ec2")`
- `cloud.account.id`
- `cloud.region`
- `cloud.availability_zone`
- `host.id`
- `host.image.id`
- `host.name`
- `host.type`

これらのタグをメトリクスに追加するために、もう1つのプロセッサーを作成します。

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
