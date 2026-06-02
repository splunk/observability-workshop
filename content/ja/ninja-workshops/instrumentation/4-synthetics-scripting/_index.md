---
title: Splunk Synthetic Scripting
description: ユーザーフロー、ビジネストランザクション、API全体のパフォーマンス問題をプロアクティブに発見・修正し、より優れたデジタル体験を提供します。
weight: 4
authors: ["Robert Castley"]
time: 45 minutes
aliases:
  - /ninja-workshops/4-synthetics-scripting/
---

問題がユーザーに影響する前に、Webアプリのパフォーマンスをプロアクティブに監視しましょう。**Splunk Synthetic Monitoring** を活用することで、技術チームとビジネスチームは詳細なテストを作成し、Webサイト、Webアプリ、リソースの速度と信頼性を、開発サイクルのあらゆる段階で長期的にプロアクティブに監視できます。

**Splunk Synthetic Monitoring** は、唯一の完全なオブザーバビリティスイートである Splunk Observability Cloud の一部として、稼働時間とWebパフォーマンス最適化に関する最も包括的かつ詳細な機能を提供します。

API、サービスエンドポイント、エンドユーザー体験の監視を簡単にセットアップできます。**Splunk Synthetic Monitoring** を使えば、基本的な稼働時間とパフォーマンスの監視を超えて、問題のプロアクティブな発見と修正、Webパフォーマンスの最適化、そして顧客に最高のユーザー体験を提供することに注力できます。

**Splunk Synthetic Monitoring** では以下のことが可能です。

- 重要なユーザーフロー、ビジネストランザクション、APIエンドポイント全体で問題を高速に検出・解決
- インテリジェントなWeb最適化エンジンにより、Webパフォーマンスの問題が顧客に影響することを未然に防止
- すべてのページリソースおよびサードパーティ依存関係のパフォーマンスを向上

## このワークショップで構築するもの

このワークショップは、本番環境でチームが実際に Splunk Synthetic Monitoring を採用する流れを反映した、相互補完的な2つのパートに分かれています。

- **Part 1 — Real Browser Test。** [**Chrome DevTools Recorder**](https://developer.chrome.com/docs/devtools/recorder/) を使用して、デモ用 Online Boutique ストアフロント上の実際のユーザージャーニー（商品の閲覧、カートへの追加、注文の発注）をキャプチャします。そのジャーニーを JSON としてエクスポートし、Splunk Synthetic Monitoring にインポートし、複数のグローバルロケーションから実行するようスケジュールし、得られたパフォーマンスデータの読み方を学びます。
- **Part 2 — API Test。** Spotify Web API に対するマルチステップ API チェックを構築します。OAuth 2 クライアントクレデンシャルを使用して認証し、得られたベアラートークンを検索リクエストにチェーンし、レスポンスを検証します。これは自社のバックエンド SLO をエンドツーエンドで監視する場合に使用するのと同じパターンです。

45分間が終わる頃には、両方のチェックタイプを快適に作成、設定、解釈できるようになり、どちらをいつ使うべきかも分かるようになっているはずです。

## 前提条件

- ローカルに Google Chrome がインストールされていること（recorder 部分で使用）。
- **Synthetics** タブが有効化された Splunk Observability Cloud オーガニゼーションへのアクセス。
- 所要時間は約45分です。テストはワークショップ終了後もバックグラウンドで実行され続けるため、トレンドの蓄積を確認したい場合はそのままにしておいてください。

> Synthetic Monitoring には、軽量なポートおよび HTTP 可用性チェック向けの第3のチェックタイプである **Uptime Tests** もあります。本ワークショップでは構築しませんが、UI 上で参照される場面に出会うはずです。続けて読むのに適した資料として [Uptime test documentation](https://docs.splunk.com/Observability/synthetics/uptime-test/uptime-test.html) があります。
