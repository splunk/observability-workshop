---
title: The Astronomy Shop
linkTitle: The Astronomy Shop
weight: 12
archetype: chapter
time: 10 minutes
description: OpenTelemetry Demo アプリケーションを操作し、ワークショップモジュールで使用するテレメトリーデータを生成します。
---

{{% notice icon="user" style="orange" title="Persona" %}}

あなたは **好奇心旺盛な天文学者** です。Astronomy Shop で望遠鏡、星図、アクセサリーを物色しています。

> [!splunk] **Astronomy Shop** は Splunk が配布する OpenTelemetry Demo であり、OpenTelemetry で全面的に計装されたマイクロサービス構成の EC アプリケーションです。さまざまな言語で書かれた複数のサービスにまたがって、メトリクス・トレース・ログを生成します。ここで生成されるテレメトリーデータは、トレーナーが選択したモジュールで活用されます。

{{% /notice %}}

{{% notice title="Exercise" style="green" icon="running" %}}

* インストラクターから Astronomy Shop の URL が共有されます。
* カタログを閲覧し、製品の詳細や説明を確認してください。
* いくつかの商品をカートに追加します。
* チェックアウトに進み、購入を完了させます。
* 十分なテレメトリーデータを生成するため、 **3〜5 回繰り返してください** 。

![ui](images/1-shop.png)

{{< tabs >}}
{{% tab title="Question" %}}
**すべてスムーズに動作しましたか？それとも、チェックアウト中に何か違和感はありませんでしたか？**
{{% /tab %}}
{{% tab title="Answer" %}}
Astronomy Shop の一部のサービスには、意図的に問題が仕込まれています。チェックアウト中に応答の遅延やエラーが発生したかもしれませんが、これは意図的なものであり、ワークショップのモジュールで詳しく調査します。
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}
