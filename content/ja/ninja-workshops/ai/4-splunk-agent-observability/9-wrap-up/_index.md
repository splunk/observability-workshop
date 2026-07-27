---
title: まとめ
linkTitle: 9. まとめ
weight: 9
archetype: chapter
time: 5 minutes
description: Splunk Agent Observabilityワークショップを完了しました。おめでとうございます。
---

おめでとうございます、**Splunk Agent Observability** ワークショップを完了しました！

Careful Health Providerのエージェント型ヘルスケアアシスタントを、患者に薬の倍量服用を静かに指示してしまうブラックボックスから、可視化、測定、ガバナンスが可能なシステムへと変革しました。

## 達成したこと

* すべてのエージェントインタラクションをトレースするためにアプリケーションを **計装** しました。
* エラーの根本原因を迅速に特定するためにエージェントの動作を **トレースおよび調査** しました。
* ハルシネーションやツール選択エラーを自動的に検出するために **品質メトリクスを有効化** しました。
* 測定しようと思わなかった繰り返し発生する障害パターン、つまり未知の未知を表面化するために **Signals を使用** しました。
* 危険なアクションをブロックし、安全でない回答を実行時に安全な方向へ導くために **ガードレールを追加** しました。

## なぜSplunk Agent Observabilityなのか

Splunk Agent Observabilityは、従来のインフラストラクチャおよびAPMモニタリングでは見えないAIの信頼性ギャップを埋めます。

* **正確で低コストな評価**: 専用のLuna SLMがハルシネーション、バイアスなどを検出し、*すべての* トラフィックをスコアリングできる手頃なコストで実現します。
* **AIスタック全体のエンドツーエンドの可視性**: エージェント、モデル、ベクターデータベース、プロキシなどを一箇所で観測できます。
* **組み込みのランタイムセキュリティとプライバシーのガードレール**: 不正確で有害な動作を顧客に届く前にブロックします。

また、Splunk Observabilityの一部であるため、エージェントのテレメトリはインフラストラクチャ、APM、ログデータと同じ場所に存在します。スタック全体を1つのプラットフォームで管理できます。

## 次のステップ

* 独自の障害モードに合わせたカスタムメトリクスと **Signals** を追加します。
* 推測をエビデンスに置き換え、リリース前のリグレッションを防止するために **experiments** を実行します。
* 自動リリースゲートとしてexperimentsをCI/CDに組み込みます。
* プロンプトインジェクション、PII漏洩、スコープ制御など、より多くのステップにガードレールを拡大します。
* よりクリーンな分離のために、異なるワークロードを専用のログストリームにルーティングします。

## 参考資料

* [Galileo documentation](https://docs.galileo.ai/)
* [Galileo Quickstart](https://docs.galileo.ai/getting-started/quickstart)
* [Galileo LangChain integration](https://docs.galileo.ai/sdk-api/third-party-integrations/langchain/langchain)

<!-- TODO screenshot: celebratory image (trophy, fireworks, etc.) sized for the wrap-up page -->
![ワークショップ完了おめでとうございます](../images/congratulations.png?width=20vw)

{{< checkpoint title="ワークショップ完了 -- **お疲れ様でした！**" >}}
