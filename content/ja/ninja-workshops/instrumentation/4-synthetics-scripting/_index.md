---
title: Synthetic Scripting
description: ユーザーフロー、ビジネストランザクション、API全体のパフォーマンス問題をプロアクティブに発見・修正し、より優れたデジタルエクスペリエンスを提供します。
weight: 4
authors: ["Robert Castley"]
time: 45 minutes
aliases:
  - /ninja-workshops/4-synthetics-scripting/
---

問題がユーザーに影響を与える前に、Web アプリのパフォーマンスをプロアクティブに監視します。**Splunk Synthetic Monitoring** を使用すると、技術チームとビジネスチームは、開発サイクルのあらゆる段階で、Web サイト、Web アプリ、リソースの速度と信頼性を継続的に監視するための詳細なテストを作成できます。

**Splunk Synthetic Monitoring** は、唯一の完全なオブザーバビリティスイートである Splunk Observability Cloud の一部として、稼働時間と Web パフォーマンスの最適化に関する最も包括的で詳細な機能を提供します。

API、サービスエンドポイント、エンドユーザーエクスペリエンスの監視を簡単にセットアップできます。**Splunk Synthetic Monitoring** を使用すると、基本的な稼働時間とパフォーマンスの監視を超えて、問題のプロアクティブな発見と修正、Web パフォーマンスの最適化、顧客への最高のユーザーエクスペリエンスの提供に集中できます。

**Splunk Synthetic Monitoring** では、以下のことが可能です

- 重要なユーザーフロー、ビジネストランザクション、API エンドポイント全体で問題を迅速に検出・解決する
- インテリジェントな Web 最適化エンジンにより、Web パフォーマンスの問題が顧客に影響を与えることを防止する
- すべてのページリソースとサードパーティの依存関係のパフォーマンスを改善する

## このワークショップで構築するもの

このワークショップは、チームが実際に本番環境で Splunk Synthetic Monitoring を導入する方法を反映した、2つの補完的なパートに分かれています

- **パート 1 — Real Browser Test。** [**Chrome DevTools Recorder**](https://developer.chrome.com/docs/devtools/recorder/) を使用して、デモ用の Online Boutique ストアフロントでの実際のユーザージャーニー（商品の閲覧、カートへの追加、注文の確定）をキャプチャします。そのジャーニーを JSON としてエクスポートし、Splunk Synthetic Monitoring にインポートして、複数のグローバルロケーションから実行するようにスケジュールし、結果のパフォーマンスデータの読み方を学びます。
- **パート 2 — API Test。** Spotify Web API に対するマルチステップの API チェックを構築します：OAuth 2 クライアントクレデンシャルを使用して認証し、取得したベアラートークンを検索リクエストにチェーンし、レスポンスを検証します。これは、自身のバックエンド SLO をエンドツーエンドで監視する場合と同じパターンです。

45分のワークショップが終わる頃には、両方のチェックタイプの作成、設定、解釈に慣れ、どのような場合にどちらを使うべきかが分かるようになります。

## 前提条件

- Google Chrome がローカルにインストールされていること（レコーダー部分で使用します）。
- **Synthetics** タブが有効になっている Splunk Observability Cloud 組織へのアクセス。
- 約45分の時間。テストはワークショップ終了後もバックグラウンドで実行され続けるため、トレンドの蓄積を観察したい場合はそのまま残しておいてください。

> Synthetic Monitoring には、軽量なポートおよび HTTP 可用性チェック用の3番目のチェックタイプ — **Uptime Tests** — もあります。このワークショップでは構築しませんが、UI で参照されているのを目にするでしょう。[Uptime test documentation](https://docs.splunk.com/Observability/synthetics/uptime-test/uptime-test.html) は良いフォローアップ資料です。
