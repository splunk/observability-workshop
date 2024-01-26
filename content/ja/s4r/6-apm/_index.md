---
title: Splunk APM
linkTitle: 6. Splunk APM
weight: 6
archetype: chapter
---

{{% badge icon="clock" color="#ed0090" %}}20 minutes{{% /badge %}}

{{% notice icon="user" style="orange" title="Persona" %}}

あなたは**バックエンドの開発者**で、SREによって発見された問題の調査を支援するように呼ばれました。SREはユーザーエクスペリエンスが悪いと特定し、その問題の調査をお願いしています。

{{% /notice %}}

RUMトレース（フロントエンド）からAPMトレース（バックエンド）に移動することで、フルエンドツーエンドの可視性の力を発見します。すべてのサービスは、Splunk Observability Cloudが視覚化、分析、異常およびエラーの検出に使用できるトレースとスパンのテレメトリを送信しています。

RUMとAPMは同じコインの二つの側面です。RUMはアプリケーションのクライアント側のビューであり、APMはサーバー側のビューです。このセクションでは、APMを使用して問題を特定するためにドリルダウンします。
