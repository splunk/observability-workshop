---
title: まとめと次のステップ
linkTitle: 7. まとめ
weight: 7
---

## ワークショップの概要

おめでとうございます！「Using AI in Splunk Observability Cloud」ワークショップを完了しました。プラットフォームのAIとML機能について学んだことを振り返りましょう。

## 重要なポイント

### 1. Related Content

- AIがコンテキストに関連するダッシュボード、ディテクター、リソースを表示します
- 調査中のナビゲーションと発見を加速します
- 使用パターンとメタデータの関係性から学習します
- **ベストプラクティス**: 一貫したタグ付けと命名規則を使用してください

### 2. AutoDetect と ML 駆動のディテクター

- 機械学習がインテリジェントなディテクターを自動的に作成します
- 環境固有のパターンと季節性に適応します
- 動的しきい値によりアラートノイズを削減します
- **ベストプラクティス**: ベースライン確立のために1〜2週間の期間を確保してください

### 3. Tag Spotlight

- すべてのタグディメンションにわたるAI駆動の根本原因分析
- パフォーマンス問題に寄与するタグを自動的に特定します
- 手動でのフィルタリングと調査の時間を何時間も節約します
- **ベストプラクティス**: すべてのリソースに包括的で一貫したタグを適用してください

### 4. Log Observer AI

- パターン検出により類似のログを自動的にグループ化します
- 異常検出により通常と異なるログエントリをハイライトします
- インテリジェントフィルタリングが関連フィールドを提案します
- **ベストプラクティス**: 一貫したフィールド名で構造化ログを使用してください

### 5. APM AI Assistant

- アプリケーション問題のトラブルシューティングのためのインテリジェントなガイダンス
- トレース内のボトルネックと異常の自動検出
- 自然言語によるインサイトと要約
- **ベストプラクティス**: 包括的なタグと属性でトレースを充実させてください

### 6. Predictive Analytics

- MLモデルが将来のトレンドとキャパシティニーズを予測します
- 潜在的な問題をプロアクティブに特定します
- キャパシティプランニングのためのトラフィック予測
- **ベストプラクティス**: 正確な予測のために一貫した履歴データを維持してください

## AI 駆動の調査ワークフロー

これらすべてのAI機能がどのように連携するかを示します：

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

## AI の効果を最大化する

### データ品質が鍵

AIは提供されるデータの品質に依存します。以下を確認してください：

- **包括的なタグ付け**: すべてのリソースに一貫してタグを付ける
- **豊富なメタデータ**: ビジネスと技術的なコンテキストを含める
- **構造化ログ**: JSONまたはキーバリュー形式のログを使用する
- **完全なトレース**: すべてのサービスと依存関係を計装する
- **一貫した命名**: 標準的な命名規則を使用する

### シンプルに始めて、スケールアップする

1. **1つの AI 機能から始める**: まずAutoDetectまたはTag Spotlightをマスターする
2. **検証と調整**: アラートをレビューして感度を調整する
3. **機能を追加**: 徐々に追加のAI機能を組み込む
4. **ワークフローを統合**: 調査で複数のAI機能を組み合わせる
5. **自動化**: AIのインサイトに基づいてランブックと自動化を構築する

### 継続的な改善

- **AI の提案を定期的にレビュー**: 正確で有用ですか？
- **感度レベルを調整**: アラートの品質に基づいて調整する
- **タグ付けを拡張**: 価値を発見したら新しいディメンションを追加する
- **ベースラインを更新**: MLモデルが現在の正常を反映していることを確認する
- **知識を共有**: AIが発見を助けたパターンを文書化する

## 避けるべき一般的な落とし穴

| 落とし穴 | 影響 | 解決策 |
|---------|--------|----------|
| 履歴データの不足 | ベースラインが不十分、異常検出が不正確 | 効果を判断する前に1〜2週間待つ |
| 一貫性のないタグ付け | Tag Spotlight が適切に相関できない | タグ名と値を標準化する |
| 感度が高すぎる | 誤検知によるアラート疲労 | 中程度から始めて、結果に基づいて調整する |
| AI の提案を無視 | 貴重なインサイトを見逃す | 提案を調査し、フィードバックを提供する |
| 非構造化ログ | パターン検出機能が制限される | 構造化ログ形式に移行する |
| AI への過度な依存 | コンテキスト固有の問題を見逃す | AI のインサイトとドメイン専門知識を組み合わせる |

## AI の効果を測定する

AIの効果を測定するためにこれらのメトリクスを追跡します：

### 検出メトリクス

- **MTTD（平均検出時間）**: 問題をより早く発見していますか？
- **誤検知率**: AutoDetectのアラートは正確ですか？
- **カバレッジ**: インシデントの何パーセントがAIで検出されましたか？

### 調査メトリクス

- **MTTR（平均復旧時間）**: より早く解決していますか？
- **根本原因までの時間**: Tag Spotlightがどれだけ早く問題を特定しますか？
- **調査ステップ数**: 必要な手動ステップが減りましたか？

### 効率メトリクス

- **レビューしたアラート**: シグナルが増え、ノイズが減りましたか？
- **ダッシュボードの使用状況**: 適切なダッシュボードをより早く見つけていますか？
- **チームの速度**: 同じリソースでより多くの問題を解決していますか？

## 追加リソース

### ドキュメント

- [Splunk Observability Cloud Documentation](https://docs.splunk.com/observability)
- [AutoDetect Documentation](https://docs.splunk.com/observability/alerts-detectors-notifications/autodetect.html)
- [Tag Spotlight Guide](https://docs.splunk.com/observability/apm/tag-spotlight.html)
- [Log Observer Documentation](https://docs.splunk.com/observability/logs/intro-logconnect.html)

### トレーニングと認定

- Splunk Observability Cloud Certification
- Advanced APM Training
- ML and AI in Observability webinars

### コミュニティ

- Splunk Community Forums
- Splunk Observability Cloud User Group
- Splunk Answers

### 最新情報を入手

- Splunk製品アップデートを購読する
- Splunk AI/ML機能リリースをフォローする
- 新しいAI機能のプレビュープログラムに参加する

## ハンズオン練習

### 学習の次のステップ

1. **AutoDetect ディテクターを作成**: 重要なサービス用に作成する
2. **Tag Spotlight を構成**: Troubleshooting MetricSetsで構成する
3. **ログパターンを探索**: 実際のログデータで探索する
4. **AI 対応のランブックを構築**: これらの機能を活用したランブックを構築する
5. **チームと共有**: ベストプラクティスを確立して共有する

### チャレンジ演習

さらに挑戦したいですか？これらの上級演習を試してください：

#### チャレンジ 1: AI 駆動のランブックを構築する

複数のAI機能を組み合わせたランブックを作成します：

- AutoDetectディテクターがトリガー
- Tag Spotlightがスコープを特定
- Related Contentが関連ダッシュボードを検索
- Log Observer AIが根本原因を確認

#### チャレンジ 2: タグ付け戦略を最適化する

- サービス全体の現在のタグを監査する
- Tag Spotlightが困難になる箇所のギャップを特定する
- 追加のディメンションを実装する
- 調査速度の改善を測定する

#### チャレンジ 3: ML ディテクターを調整する

- 重要なメトリクス用にAutoDetectをデプロイする
- 2週間モニタリングする
- アラートの品質（真陽性vs偽陽性）を分析する
- 感度を調整して結果を比較する

#### チャレンジ 4: AI 強化ダッシュボードを作成する

- 以下を組み合わせたダッシュボードを構築します：
  - ML予測値
  - 異常インジケーター
  - Tag Spotlightのインサイト
  - Related Contentリンク

## フィードバックの提供

皆様のフィードバックはAI機能の改善に役立ちます：

- 不正確なAIの提案をSplunkサポートを通じて報告する
- Splunkアカウントチームと成功事例を共有する
- 新しいAI機能のプレビュープログラムに参加する
- コミュニティでの議論に貢献する

## ありがとうございました

このワークショップにご参加いただきありがとうございました。AIとMLはオブザーバビリティを変革し、大規模で複雑なシステムの管理を容易にしています。これらのツールをマスターすることで、あなた自身と組織を現代のクラウドネイティブ環境での成功に向けて準備することができます。

### ご質問は？

- Splunkアカウントチームにお問い合わせください
- [Splunk Community](https://community.splunk.com/) にアクセスしてください
- [Splunk Docs](https://docs.splunk.com/) をご確認ください

{{% notice title="次のワークショップ" style="primary" icon="forward" %}}
さらに学びたいですか？他の [Splunk4Ninjas ワークショップ](/ninja-workshops/) をチェックして、Splunk Observability Cloudの特定分野の専門知識を深めてください。
{{% /notice %}}

---

**ワークショップ完了！** このワークショップがお役に立てば幸いです。AIを活用してオブザーバビリティの実践を強化してください！
