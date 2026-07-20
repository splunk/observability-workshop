---
title: "Phase 0: Python ウォームアップ"
linkTitle: 2. Python ウォームアップ
weight: 2
archetype: chapter
time: 15 minutes
description: ホスト上で素のPythonアプリを実行し、カスタムメトリクスでSplunkへの接続を確認した後、OBIバイナリを使用してAPMトレーシングを追加します。すべてDockerなしで行います。
---

このフェーズでは、OBIが生のLinuxプロセスに対して **カーネルレベル** で動作することを示します。コンテナなし、サイドカーなし、SDKなし — eBPFバイナリがカーネルからアプリを監視するだけです。

このセクションを完了すると、以下が得られます。

1. オブザーバビリティコードがゼロの状態で動作するPython Flaskアプリ
2. Splunk組織がデータを受信していることの証明（カスタムメトリクス経由）
3. コード変更なしにカーネルからアプリに追加された完全なAPMトレース
