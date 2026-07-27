---
title: "Phase 0: Python ウォームアップ"
linkTitle: 2. Python Warm-up
weight: 2
archetype: chapter
time: 15 minutes
description: ホスト上で素の Python アプリを実行し、カスタムメトリクスを使用して Splunk への接続を確認した後、OBI バイナリを使用して APM トレースを追加します。すべて Docker なしで行います。
---

このフェーズでは、OBI が生の Linux プロセス上で**カーネルレベル**で動作することを示します。コンテナなし、サイドカーなし、SDK なし、ただ eBPF バイナリがカーネルからアプリを監視するだけです。

このセクションの終了時には、以下が完了します

1. オブザーバビリティコードがゼロの Python Flask アプリの実行
2. Splunk 組織がデータを受信していることの確認（カスタムメトリクス経由）
3. コード変更なしでカーネルからアプリに追加された完全な APM トレース
