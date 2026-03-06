---
title: Splunk APM
linkTitle: 6. Splunk APM
weight: 6
archetype: chapter
time: 20 minutes
description: このセクションでは、APMを使用して掘り下げ、問題がどこにあるかを特定します。
---

{{% notice icon="user" style="orange" title="ペルソナ" %}}

あなたは**バックエンド開発者**で、SREが発見した問題の調査を手伝うよう依頼されました。SREはユーザーエクスペリエンスの低下を特定し、あなたにその問題を調査するよう依頼しました。

{{% /notice %}}

RUMトレース（フロントエンド）からAPMトレース（バックエンド）にジャンプすることで、完全なエンドツーエンドの可視性の力を発見します。すべてのサービスはテレメトリ（トレースとスパン）を送信しており、Splunk Observability Cloudはこれを視覚化、分析し、異常やエラーを検出するために使用できます。

RUMとAPMは同じコインの表と裏です。RUMはアプリケーションのクライアント側からの視点であり、APMはサーバー側からの視点です。このセクションでは、APMを使用して掘り下げ、問題がどこにあるかを特定します。
