---
title: Synthetic Scripting
description: ユーザーフロー、ビジネストランザクション、APIのパフォーマンス問題をプロアクティブに発見・修正し、より良いデジタルエクスペリエンスを提供します。
weight: 1
authors: ["Robert Castley"]
time: 45 minutes
aliases:
  - /ninja-workshops/4-synthetics-scripting/
---

Webアプリのパフォーマンスを、問題がユーザーに影響を与える前にプロアクティブにモニタリングします。**Splunk Synthetic Monitoring** を使用すると、技術チームとビジネスチームは詳細なテストを作成し、開発サイクルのあらゆる段階で、Webサイト、Webアプリ、リソースの速度と信頼性を継続的にモニタリングできます。

**Splunk Synthetic Monitoring** は、唯一の完全なオブザーバビリティスイートであるSplunk Observability Cloudの一部として、稼働時間とWebパフォーマンス最適化のための最も包括的で詳細な機能を提供します。

API、サービスエンドポイント、エンドユーザーエクスペリエンスのモニタリングを簡単にセットアップできます。**Splunk Synthetic Monitoring** を使用すると、基本的な稼働時間とパフォーマンスのモニタリングを超えて、問題のプロアクティブな発見と修正、Webパフォーマンスの最適化、顧客への最高のユーザーエクスペリエンスの確保に集中できます。

**Splunk Synthetic Monitoring** では以下が可能です。

- 重要なユーザーフロー、ビジネストランザクション、APIエンドポイント全体で問題を迅速に検出・解決
- インテリジェントなWeb最適化エンジンにより、Webパフォーマンスの問題が顧客に影響する前に防止
- すべてのページリソースとサードパーティ依存関係のパフォーマンスを改善

## このワークショップで構築するもの

このワークショップは、チームが実際にSplunk Synthetic Monitoringを本番環境で採用する方法を反映した、2つの補完的なパートに分かれています。

- **パート1 — Real Browser Test。** [**Chrome DevTools Recorder**](https://developer.chrome.com/docs/devtools/recorder/) を使用して、デモのOnline Boutiqueストアフロントでの実際のユーザージャーニー（商品の閲覧、カートへの追加、注文の確定）をキャプチャします。そのジャーニーをJSONとしてエクスポートし、Splunk Synthetic Monitoringにインポートし、複数のグローバルロケーションから実行するようスケジュールし、結果のパフォーマンスデータの読み方を学びます。
- **パート2 — API Test。** Spotify Web APIに対するマルチステップAPIチェックを構築します。OAuth 2クライアントクレデンシャルを使用して認証し、結果のベアラートークンを検索リクエストにチェーンし、レスポンスを検証します。これは、独自のバックエンドSLOをエンドツーエンドでモニタリングする際に使用するのと同じパターンです。

45分のワークショップが終わる頃には、両方のチェックタイプの作成、設定、解釈に慣れているはずです。そして、どのような場合にどちらを使うべきかがわかるようになります。

## 前提条件

- Google Chromeがローカルにインストールされていること（レコーダー部分で使用）
- **Synthetics** タブが有効なSplunk Observability Cloud組織へのアクセス
- 約45分。テストはワークショップ終了後もバックグラウンドで実行され続けるため、トレンドの蓄積を観察したい場合はそのまま残しておいてください

> Synthetic Monitoringには、軽量なポートおよびHTTP可用性チェック用の3番目のチェックタイプ **Uptime Tests** もあります。このワークショップでは構築しませんが、UI上で参照されているのを確認できます。[Uptime testドキュメント](https://docs.splunk.com/Observability/synthetics/uptime-test/uptime-test.html)は、フォローアップとして読むのに適しています。
