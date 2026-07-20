---
title: まとめと次のステップ
linkTitle: 7. まとめ
weight: 7
---

## ワークショップのまとめ

おめでとうございます！「Using AI in Splunk Observability Cloud」ワークショップを完了しました。プラットフォームにおけるAIとMLの機能について学んだ内容を振り返りましょう。

## 主なポイント

### 1. Related Content

- AIがコンテキストに関連するダッシュボード、ディテクター、リソースを表示します
- 調査中のナビゲーションと発見を加速します
- 使用パターンとメタデータの関係性から学習します
- **ベストプラクティス** : 一貫したタグ付けと命名規則を使用します

### 2. AutoDetectとMLドリブンディテクター

- 機械学習がインテリジェントなディテクターを自動的に作成します
- 環境固有のパターンと季節性に適応します
- 動的しきい値によりアラートノイズを削減します
- **ベストプラクティス** : ベースライン確立のために1〜2週間を確保します

### 3. Tag Spotlight

- すべてのタグディメンションにわたるAI駆動の根本原因分析
- パフォーマンス問題に寄与するタグを自動的に特定します
- 手動のフィルタリングと調査の時間を大幅に節約します
- **ベストプラクティス** : すべてのリソースに包括的で一貫したタグを適用します

### 4. Log Observer AI

- パターン検出により類似のログを自動的にグループ化します
- 異常検出により通常と異なるログエントリをハイライトします
- インテリジェントなフィルタリングが関連フィールドを提案します
- **ベストプラクティス** : 一貫したフィールド名で構造化ログを使用します

### 5. APM AI Assistant

- アプリケーション問題のトラブルシューティングに対するインテリジェントなガイダンス
- トレースにおけるボトルネックと異常の自動検出
- 自然言語によるインサイトとサマリー
- **ベストプラクティス** : 包括的なタグと属性でトレースを充実させます

### 6. 予測分析

- MLモデルが将来のトレンドとキャパシティニーズを予測します
- 潜在的な問題のプロアクティブな特定
- キャパシティプランニングのためのトラフィック予測
- **ベストプラクティス** : 正確な予測のために一貫した履歴データを維持します

## AI駆動の調査ワークフロー

すべてのAI機能がどのように連携するかを示します

```text
1. Issue Detected
   ├─→ AutoDetect ML Detector triggers alert
   └─→ Anomaly clearly identified with dynamic baseline

2. Context Gathering
   ├─→ Related Content surfaces relevant dashboards
   ├─→ APM AI Assistant provides service health summary
   └─→ Log Observer AI shows correlated log patterns

3. Root Cause Analysis
   ├─→ Tag Spotlight identifies problematic tag values
   ├─→ APM AI analyzes traces and highlights bottlenecks
   └─→ Log patterns confirm findings

4. Impact Assessment
   ├─→ AI estimates scope (which customers/regions affected)
   ├─→ Historical comparison shows severity
   └─→ Dependency analysis shows downstream impact

5. Resolution
   ├─→ AI suggests potential fixes based on similar past issues
   ├─→ Monitor AI metrics to confirm resolution
   └─→ AI learns from the incident for future detection
```

## AIの効果を最大化する

### データ品質が鍵

AIは提供されるデータの品質に依存します。以下を確認してください

- **包括的なタグ付け** : すべてのリソースに一貫したタグを付けます
- **豊富なメタデータ** : ビジネスおよび技術的コンテキストを含めます
- **構造化ログ** : JSONまたはキーバリュー形式のログを使用します
- **完全なトレース** : すべてのサービスと依存関係を計装します
- **一貫した命名** : 標準的な命名規則を使用します

### シンプルに始めてスケールアップ

1. **1つのAI機能から始める** : まずAutoDetectまたはTag Spotlightをマスターします
2. **検証とチューニング** : アラートをレビューし感度を調整します
3. **機能を追加する** : 段階的に追加のAI機能を組み込みます
4. **ワークフローを統合する** : 調査で複数のAI機能を組み合わせます
5. **自動化する** : AIのインサイトに基づいてランブックと自動化を構築します

### 継続的な改善

- **AIの提案を定期的にレビューする** : 正確で役立っていますか？
- **感度レベルをチューニングする** : アラート品質に基づいて調整します
- **タグ付けを拡張する** : 価値を発見したら新しいディメンションを追加します
- **ベースラインを更新する** : MLモデルが現在の正常状態を反映していることを確認します
- **知識を共有する** : AIが発見を助けたパターンをドキュメント化します

## 避けるべき一般的な落とし穴

| 落とし穴 | 影響 | 解決策 |
|---------|--------|----------|
| 履歴データの不足 | ベースラインの品質低下、不正確な異常検出 | 効果を判断する前に1〜2週間待ちます |
| 一貫性のないタグ付け | Tag Spotlightが適切に相関できない | タグ名と値を標準化します |
| 感度が高すぎる | 誤検知によるアラート疲れ | 中程度から始め、結果に基づいてチューニングします |
| AIの提案を無視する | 貴重なインサイトを見逃す | 提案を調査し、フィードバックを提供します |
| 非構造化ログ | パターン検出機能の制限 | 構造化ログ形式に移行します |
| AIへの過度な依存 | コンテキスト固有の問題を見逃す | AIのインサイトとドメイン専門知識を組み合わせます |

## AIの効果を測定する

AI の効果を測定するために以下のメトリクスを追跡します

### 検出メトリクス

- **MTTD（平均検出時間）** : 問題をより速く発見できていますか？
- **誤検知率** : AutoDetectアラートは正確ですか？
- **カバレッジ** : インシデントの何パーセントがAIで検出されましたか？

### 調査メトリクス

- **MTTR（平均復旧時間）** : より速く解決できていますか？
- **根本原因到達時間** : Tag Spotlightがどのくらい速く問題を特定しますか？
- **調査ステップ** : 手動ステップが減りましたか？

### 効率メトリクス

- **レビューしたアラート** : シグナルが増え、ノイズが減りましたか？
- **ダッシュボード使用状況** : 適切なダッシュボードをより速く見つけられますか？
- **チームベロシティ** : 同じリソースでより多くの問題を解決できていますか？

## 追加リソース

### ドキュメント

- [Splunk Observability Cloudドキュメント](https://docs.splunk.com/observability)
- [AutoDetectドキュメント](https://docs.splunk.com/observability/alerts-detectors-notifications/autodetect.html)
- [Tag Spotlightガイド](https://docs.splunk.com/observability/apm/tag-spotlight.html)
- [Log Observerドキュメント](https://docs.splunk.com/observability/logs/intro-logconnect.html)

### トレーニングと認定

- Splunk Observability Cloud認定
- 上級APMトレーニング
- オブザーバビリティにおけるMLとAIのウェビナー

### コミュニティ

- Splunk Communityフォーラム
- Splunk Observability Cloudユーザーグループ
- Splunk Answers

### 最新情報の入手

- Splunk製品アップデートを購読します
- Splunk AI/ML機能リリースをフォローします
- 新しいAI機能のプレビュープログラムに参加します

## ハンズオン演習

### 学習の次のステップ

1. **AutoDetectディテクターを作成する** : 重要なサービスに対して設定します
2. **Tag Spotlightを設定する** : Troubleshooting MetricSetsを使用します
3. **ログパターンを探索する** : 実際のログデータで確認します
4. **AI対応のランブックを構築する** : これらの機能を活用します
5. **チームと共有する** : ベストプラクティスを確立します

### チャレンジ演習

さらに挑戦したい方は、以下の上級演習を試してください

#### チャレンジ1: AI駆動のランブックを構築する

複数のAI機能を組み合わせたランブックを作成します

- AutoDetectディテクターがトリガー
- Tag Spotlightがスコープを特定
- Related Contentが関連ダッシュボードを検索
- Log Observer AIが根本原因を確認

#### チャレンジ2: タグ付け戦略を最適化する

- サービス全体の現在のタグを監査します
- Tag Spotlightが困難になる箇所のギャップを特定します
- 追加のディメンションを実装します
- 調査速度の改善を測定します

#### チャレンジ3: MLディテクターをチューニングする

- 重要なメトリクスにAutoDetectをデプロイします
- 2週間モニタリングします
- アラート品質を分析します（真陽性 vs. 誤検知）
- 感度を調整し結果を比較します

#### チャレンジ4: AI強化ダッシュボードを作成する

- 以下を組み合わせたダッシュボードを構築します
  - ML予測値
  - 異常インジケーター
  - Tag Spotlightのインサイト
  - Related Contentリンク

## フィードバックの提供

フィードバックはAI機能の改善に役立ちます

- Splunk Supportを通じて不正確なAI提案を報告します
- Splunkアカウントチームに成功事例を共有します
- 新しいAI機能のプレビュープログラムに参加します
- コミュニティディスカッションに貢献します

## ありがとうございました

このワークショップにご参加いただきありがとうございます。AIとMLはオブザーバビリティを変革し、大規模な複雑なシステムの管理を容易にしています。これらのツールをマスターすることで、モダンなクラウドネイティブ環境での成功に向けて、ご自身と組織を位置づけることができます。

### ご質問は？

- Splunkアカウントチームにお問い合わせください
- [Splunk Community](https://community.splunk.com/)をご覧ください
- [Splunk Docs](https://docs.splunk.com/)をご確認ください

{{% notice title="次のワークショップ" style="primary" icon="forward" %}}
さらに学びたい方は、Splunk Observability Cloudの特定の分野の専門知識を深めるために、他の [Splunk4Ninjasワークショップ](/ninja-workshops/) をご覧ください。
{{% /notice %}}

---

**ワークショップ完了！** このワークショップがお役に立てれば幸いです。AIを活用してオブザーバビリティの実践を向上させましょう！
