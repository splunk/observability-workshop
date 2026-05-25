---
title: Optimize End User Experiences
linkTitle: Optimize End User Experiences
weight: 4
archetype: chapter
authors: ["Sarah Ware"]
time: 90 minutes
description: Splunk RUM と Synthetics を組み合わせて、実際のユーザーパフォーマンスを測定し、プロアクティブなテストを実行し、重要なフロントエンド KPI にアラートを設定します。
---

Splunk Observability を使用して、エンドユーザーエクスペリエンスに関するインサイトを取得し、エクスペリエンスを改善するためのシナリオをプロアクティブにテストするにはどうすればよいでしょうか？

セクション:

- 可用性とパフォーマンスをすぐに把握するために、基本的な [Synthetic テスト](./1-synthetics/_index.md)を設定する
  - Uptime テスト
  - API テスト
  - Single page Browser テスト
- [RUM](./2-rum/_index.md) を探索して実際のユーザーを理解する
- ユーザーについて学んだことと、ユーザーに行ってほしい操作に基づいて、[高度な Synthetics テスト](./3-advanced-synthetics/_index.md)を作成する
- KPI を把握し、トレンドを表示し、イベントのコンテキストでデータを表示するために、[ダッシュボードチャート](./4-dashboards/_index.md)をカスタマイズする
- KPI にアラートを設定するために [Detectors](./5-detectors/_index.md) を作成する

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}ワークショップ全体を通して以下を念頭に置いてください：エンドユーザーと自分自身/開発者にとって、最速で価値を実現するために、どのように戦略的にアクティビティの優先順位を決めればよいでしょうか？{{% /notice %}}

## コンテキスト

念のため確認ですが、エンドユーザーエクスペリエンスを構成するすべての要素をキャプチャするために、フロントエンドのパフォーマンスモニタリングが必要です。バックエンドのみを監視している場合、ユーザーの成功に不可欠な他のすべてのリソースを見逃していることになります。実際の事例については [What the Fastly Outage Can Teach Us About Observability](https://www.splunk.com/en_us/blog/devops/what-the-fastly-outage-can-teach-us-about-observability.html) をお読みください。下の画像をクリックすると拡大できます。
![What goes into the front end](./images/frontend.png)

## 参考資料

このワークショップでは、エンドユーザーエクスペリエンスをさらに理解し、最適化する方法に関するリソースへの参照が随所に登場します。サポートされている機能については [Splunk Docs](https://docs.splunk.com/observability/en/rum/intro-to-rum.html)、ヒントやコツについては [Lantern](https://lantern.splunk.com/Observability/UCE/Optimized_experiences) に加えて、[Google's web.dev](https://web.dev/) や [Mozilla](https://developer.mozilla.org/en-US/docs/Learn/Performance) も優れたリソースです。

使用している特定のライブラリ、プラットフォーム、CDN には、それぞれ独自のリソースがあることも覚えておいてください。例えば、[React](https://react.dev/reference/react/useCallback#skipping-re-rendering-of-components)、[Wordpress](https://wpengine.com/support/troubleshooting-high-time-first-byte-ttfb/)、[Cloudflare](https://community.cloudflare.com/t/improving-time-to-first-byte-ttfb-with-cloudflare/390367) にはそれぞれパフォーマンスを改善するための独自のヒントがあります。
