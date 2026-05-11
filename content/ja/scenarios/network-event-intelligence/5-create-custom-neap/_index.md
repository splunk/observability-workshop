---
title: カスタム NEAP の作成
linkTitle: 5. カスタム NEAP の作成
weight: 5
time: 10 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---

<div style="max-width: 80%; margin: 0 auto; font-size: 18px;">

## ベンダー間のアラート相関

ネットワークイベントが発生すると、運用チームは何が起こったのか、どこから始まったのか、どのサービスやユーザーが影響を受けているのかを把握するために、接続されていない複数のツールを手作業で調査しなければなりません。共通の相関レイヤーがなければ、アラートノイズは高くなり、調査は遅くなり、ネットワーク障害のビジネスへの影響は顧客からの問い合わせが来るまで見えないままです。

ITSI の真の価値は、関連するイベントを **Notable Event Aggregation Policy (NEAP)** を使用して、単一のアクション可能なエピソードに相関させる能力にあります。

NEAP は、ITSI がノータブルイベントをグループ化するルールを定義します。この場合の目標は、同じネットワークサイトに関連する Catalyst Center と SolarWinds の両方のアラートを単一のエピソードにグループ化することです。これにより、運用チームは調査する場所が1つになり、対応するチケットが1つになり、どのサイトが影響を受けているか、そして何件のアラートソースが問題を裏付けているかを明確に把握できます。

ITSI には事前設定された NEAP が多数含まれていますが、このワークショップではロケーションごとのアラートのグループ化に特に焦点を当てます。このセクションでは、Catalyst Center と SolarWinds のアラートをサイトごとに相関させるカスタム NEAP を構築し、サービスヘルスとエピソードの状態を一緒に確認してポリシーが正しく機能していることを検証します。

![Episode Review](../images/episode-review.png?width=40vw)

## このセクションで行うこと

このセクションを完了すると、以下のことが達成されます

- Catalyst Center と SolarWinds の両方のアラートをネットワークサイトごとにグループ化する**カスタム Notable Event Aggregation Policy** の作成
- ネットワークヘルスが正常に戻った際のエピソード自動解決の設定
- Service Analyzer と Episode Review がリアルタイムのサイトヘルスを反映していることの検証

</div>
