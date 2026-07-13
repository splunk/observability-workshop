---
title: Astronomy Shop
linkTitle: 2. Astronomy Shop
weight: 2
archetype: chapter
time: 10 minutes
description: OpenTelemetryデモアプリケーションを探索し、ワークショップモジュールで使用するテレメトリデータを生成します。
---

{{% notice icon="user" style="orange" title="ペルソナ" %}}

あなたは **好奇心旺盛な天文学者** です。Astronomy Shopで望遠鏡、星図、アクセサリーを探しています。

{{% /notice %}}

> >[!IMPORTANT]
> **Astronomy Shop** は、OpenTelemetryデモのSplunkバージョンです。OpenTelemetryで完全に計装されたマイクロサービスベースのEコマースアプリケーションで、異なる言語で書かれた複数のサービスにわたってメトリクス、トレース、ログを生成します。ここで生成したテレメトリデータは、トレーナーが選択するモジュールで使用されます。

{{% notice title="演習" style="green" icon="running" %}}

* インストラクターがAstronomy ShopのURLを提供します。
* カタログを閲覧します — 商品の詳細を確認し、説明を読みます。
* カートにいくつかのアイテムを追加します。
* チェックアウトに進み、購入を完了します。
* 十分なテレメトリデータを生成するために **3〜5回繰り返します** 。
* 可能であれば、モバイルデバイスやタブレットからもAstronomy Shopを試します。

![ui](images/1-shop.png)

{{< tabs >}}
{{% tab title="質問" %}}
**すべてスムーズに動作しましたか？チェックアウト中に何か異常に気づきましたか？**
{{% /tab %}}
{{% tab title="回答" %}}
Astronomy Shopの一部のサービスには、意図的に問題が注入されています。チェックアウト中にレスポンスが遅かったり、エラーが発生したりしたかもしれません。これは意図的なもので、ワークショップモジュールで調査します。
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}
