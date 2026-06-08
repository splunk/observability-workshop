---
title: The Astronomy Shop
linkTitle: The Astronomy Shop
weight: 2
archetype: chapter
time: 10 minutes
description: OpenTelemetry Demo アプリケーションを操作し、ワークショップモジュールで使用するテレメトリーデータを生成します。
---

{{% notice icon="user" style="orange" title="Persona" %}}

あなたは**好奇心旺盛な天文学者**です。Astronomy Shop で望遠鏡、星図、アクセサリーを閲覧しています。

{{% /notice %}}

> >[!IMPORTANT]
> **Astronomy Shop** は OpenTelemetry Demo の Splunk バージョンです。OpenTelemetry で完全に計装されたマイクロサービスベースの EC サイトアプリケーションです。異なる言語で書かれた複数のサービスにわたって、メトリクス、トレース、ログを生成します。ここで生成したテレメトリーデータは、トレーナーが選択するモジュールで使用されます。

{{% notice title="Exercise" style="green" icon="running" %}}

* インストラクターが Astronomy Shop の URL を提供します。
* カタログを閲覧し、商品の詳細を確認し、説明を読んでください。
* カートに複数の商品を追加してください。
* チェックアウトに進み、購入を完了してください。
* 十分なテレメトリーデータを生成するために、**3〜5回繰り返して**ください。

![ui](images/1-shop.png)

{{< tabs >}}
{{% tab title="Question" %}}
**すべてスムーズに動作しましたか？チェックアウト中に何か異常に気づきましたか？**
{{% /tab %}}
{{% tab title="Answer" %}}
Astronomy Shop の一部のサービスには、意図的に問題が注入されています。チェックアウト中にレスポンスが遅かったり、エラーが発生したりしたかもしれません。これは意図的なもので、ワークショップモジュールで調査します。
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}
