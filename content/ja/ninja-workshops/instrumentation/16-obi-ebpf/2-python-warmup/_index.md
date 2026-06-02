---
title: "Phase 0: Python ウォームアップ"
linkTitle: 2. Python ウォームアップ
weight: 2
archetype: chapter
time: 15 minutes
description: ホスト上で素の Python アプリを実行し、カスタムメトリクスで Splunk への接続性を確認した後、Docker を使わずに OBI バイナリで APM トレーシングを追加します。
---

このフェーズでは、OBI が素の Linux プロセスに対して**カーネルレベル**で動作することを確認します。コンテナもサイドカーも SDK も不要で、カーネルからアプリを監視する eBPF バイナリだけで動きます。

このセクションの終わりまでに、以下が完成します。

1. observability コードがゼロの状態で動作する Python Flask アプリ
2. Splunk org がデータを受信していることの証明（カスタムメトリクス経由）
3. コード変更ゼロでカーネルから追加された、アプリの完全な APM トレース
