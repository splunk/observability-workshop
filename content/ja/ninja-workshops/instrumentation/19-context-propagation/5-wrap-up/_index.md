---
title: まとめ
linkTitle: 6. まとめ
weight: 6
time: 5 minutes
description: 主要なポイントとクリーンアップ手順。
---

## サマリー

このワークショップでは、以下の内容をハンズオンで体験しました

- **ヘッダーを除去するリバースプロキシ**が W3C Trace Context の伝播をどのように破壊するか
- アプリケーションサービスを最初にデプロイし、エンドツーエンドのリクエストフローが正しく動作することを検証する
- 次に **Splunk Distribution of the OpenTelemetry Collector** をデプロイし、Python マイクロサービスを計装して **Splunk Observability Cloud** にテレメトリをエクスポートする
- フェーズ 1 で**分断されたトレース**を観察し、Infrastructure メトリクスを検証する
- フェーズ 2 で手動の inject/extract により**接続されたトレース**を復元する

## リファレンスコマンド一覧

| アクション | コマンド |
| ------ | ------- |
| Step 1 — サービスのデプロイ | `start-lab.sh` |
| Step 2 — Collector のデプロイ | `deploy-collector.sh` |
| Step 3 - 継続的な負荷 | `start-load.sh` |
| Step 4 - 手動プロパゲーション（コードガイド） | manual-propagation.md |
| Step 5 - スタックの停止とクリーンアップ | `teardown.sh` |

## クリーンアップ

```bash
./scripts/teardown.sh
```
