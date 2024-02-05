---
title: Splunk APM
linkTitle: 6. Splunk APM
weight: 6
archetype: chapter
---

{{% badge icon="clock" color="#ed0090" %}}20 minutes{{% /badge %}}

{{% notice icon="user" style="orange" title="Persona" %}}

あなたは**バックエンドの開発者**で、SRE によって発見された問題の調査を支援するように呼ばれました。SRE はユーザーエクスペリエンスが悪いと特定し、その問題の調査をお願いしています。

{{% /notice %}}

RUM トレース（フロントエンド）から APM トレース（バックエンド）にジャンプすることで、完全な End to End の可視性の力を理解できるでしょう。すべてのサービスが Splunk Observability Cloud によって視覚化、分析、異常およびエラーの検出が可能となるテレメトリ（トレースやスパン）を送信しています。

RUM と APM は同じコインの二つの側面です。RUM はアプリケーションのクライアント側のビューであり、APM はサーバー側のビューです。このセクションでは、APM を使用してどこに問題が潜んでいるかドリルダウンし、特定します。
