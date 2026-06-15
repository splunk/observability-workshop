---
title: まとめと次のステップ
linkTitle: 7. まとめ
weight: 7
---

## ワークショップのまとめ

おめでとうございます！「Using AI in Splunk Observability Cloud」ワークショップを完了しました。プラットフォームにおける AI と ML の機能について学んだことを振り返りましょう。

## 主なポイント

### 1. Related Content

- AI がコンテキストに関連するダッシュボード、ディテクター、リソースを表示します
- 調査中のナビゲーションと発見を加速します
- 使用パターンとメタデータの関係性から学習します
- **ベストプラクティス**: 一貫したタグ付けと命名規則を使用してください

### 2. AutoDetect と ML 駆動のディテクター

- 機械学習がインテリジェントなディテクターを自動的に作成します
- 環境固有のパターンや季節性に適応します
- 動的なしきい値によりアラートノイズを削減します
- **ベストプラクティス**: ベースライン確立のために1〜2週間の期間を確保してください

### 3. Tag Spotlight

- すべてのタグディメンションにわたる AI を活用した根本原因分析
- パフォーマンスの問題に寄与するタグを自動的に特定します
- 手動のフィルタリングや調査にかかる時間を数時間節約します
- **ベストプラクティス**: すべてのリソースに包括的で一貫したタグを適用してください

### 4. Log Observer AI

- パターン検出が類似のログを自動的にグループ化します
- 異常検出が通常と異なるログエントリをハイライトします
- インテリジェントなフィルタリングが関連フィールドを提案します
- **ベストプラクティス**: 一貫したフィールド名で構造化ログを使用してください

### 5. APM AI Assistant

- アプリケーションの問題をトラブルシューティングするためのインテリジェントなガイダンス
- トレースにおけるボトルネックと異常の自動検出
- 自然言語によるインサイトとサマリー
- **ベストプラクティス**: 包括的なタグと属性でトレースを充実させてください

### 6. Predictive Analytics

- ML モデルが将来のトレンドとキャパシティのニーズを予測します
- 潜在的な問題のプロアクティブな特定
- キャパシティプランニングのためのトラフィック予測
- **ベストプラクティス**: 正確な予測のために一貫した履歴データを維持してください

## AI を活用した調査ワークフロー

これらの AI 機能がどのように連携して動作するかを示します

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

AI は提供されるデータの品質に依存します。以下を確認してください

- **包括的なタグ付け**: すべてのリソースに一貫してタグを付ける
- **豊富なメタデータ**: ビジネスと技術のコンテキストを含める
- **構造化ログ**: JSON またはキーバリュー形式のログを使用する
- **完全なトレース**: すべてのサービスと依存関係を計装する
- **一貫した命名**: 標準的な命名規則を使用する

### シンプルに始めて、スケールアップする

1. **1つの AI 機能から始める**: まず AutoDetect または Tag Spotlight を習得する
2. **検証とチューニング**: アラートを確認し、感度を調整する
3. **機能を追加する**: 段階的に追加の AI 機能を組み込む
4. **ワークフローを統合する**: 調査で複数の AI 機能を組み合わせる
5. **自動化する**: AI のインサイトに基づいてランブックと自動化を構築する

### 継続的な改善

- **AI の提案を定期的に確認する**: 正確で役立つものですか？
- **感度レベルを調整する**: アラートの品質に基づいて調整する
- **タグ付けを拡大する**: 価値を発見したら新しいディメンションを追加する
- **ベースラインを更新する**: ML モデルが現在の正常状態を反映していることを確認する
- **知識を共有する**: AI が発見を助けるパターンを文書化する

## 避けるべき一般的な落とし穴

| 落とし穴 | 影響 | 解決策 |
|---------|--------|----------|
| 履歴データの不足 | ベースラインが不十分で、異常検出が不正確 | 効果を判断する前に1〜2週間待つ |
| 一貫性のないタグ付け | Tag Spotlight が適切に相関できない | タグの名前と値を標準化する |
| 感度が高すぎる | 誤検知によるアラート疲労 | 中程度から始め、結果に基づいて調整する |
| AI の提案を無視する | 貴重なインサイトを見逃す | 提案を調査し、フィードバックを提供する |
| 非構造化ログ | パターン検出能力が限定的 | 構造化ログ形式に移行する |
| AI への過度な依存 | コンテキスト固有の問題を見逃す | AI のインサイトとドメインの専門知識を組み合わせる |

## AI の効果を測定する

AI の効果を測定するために、以下のメトリクスを追跡してください

### 検出メトリクス

- **MTTD (Mean Time to Detect)**: 問題をより早く発見できていますか？
- **誤検知率**: AutoDetect のアラートは正確ですか？
- **カバレッジ**: インシデントの何パーセントが AI によって検出されましたか？

### 調査メトリクス

- **MTTR (Mean Time to Resolve)**: より早く解決できていますか？
- **根本原因到達時間**: Tag Spotlight がどれくらい早く問題を特定しますか？
- **調査ステップ数**: 手動ステップの削減はありますか？

### 効率メトリクス

- **確認したアラート**: シグナルが増え、ノイズが減りましたか？
- **ダッシュボードの使用**: 適切なダッシュボードをより早く見つけられていますか？
- **チームの生産性**: 同じリソースでより多くの問題を解決していますか？

## 追加リソース

### ドキュメント

- [Splunk Observability Cloud Documentation](https://docs.splunk.com/observability)
- [AutoDetect Documentation](https://docs.splunk.com/observability/alerts-detectors-notifications/autodetect.html)
- [Tag Spotlight Guide](https://docs.splunk.com/observability/apm/tag-spotlight.html)
- [Log Observer Documentation](https://docs.splunk.com/observability/logs/intro-logconnect.html)

### トレーニングと認定

- Splunk Observability Cloud Certification
- Advanced APM Training
- ML and AI in Observability ウェビナー

### コミュニティ

- Splunk Community Forums
- Splunk Observability Cloud User Group
- Splunk Answers

### 最新情報

- Splunk の製品アップデートを購読する
- Splunk AI/ML の機能リリースをフォローする
- 新しい AI 機能のプレビュープログラムに参加する

## ハンズオン演習

### 学習の次のステップ

1. **AutoDetect ディテクターを作成する** - 重要なサービスに対して
2. **Tag Spotlight を設定する** - Troubleshooting MetricSets を使用して
3. **ログパターンを探索する** - 実際のログデータで
4. **AI 対応のランブックを構築する** - これらの機能を活用して
5. **チームと共有する** - ベストプラクティスを確立する

### チャレンジ演習

さらに挑戦したいですか？以下の上級演習に取り組んでみましょう

#### チャレンジ 1: AI を活用したランブックの構築

複数の AI 機能を組み合わせたランブックを作成します

- AutoDetect ディテクターのトリガー
- Tag Spotlight によるスコープの特定
- Related Content による関連ダッシュボードの検索
- Log Observer AI による根本原因の確認

#### チャレンジ 2: タグ付け戦略の最適化

- サービス全体の現在のタグを監査する
- Tag Spotlight が困難になる箇所のギャップを特定する
- 追加のディメンションを実装する
- 調査速度の改善を測定する

#### チャレンジ 3: ML ディテクターのチューニング

- 重要なメトリクスに AutoDetect をデプロイする
- 2週間監視する
- アラートの品質を分析する（真陽性 vs 偽陽性）
- 感度を調整し、結果を比較する

#### チャレンジ 4: AI を活用したダッシュボードの作成

- 以下を組み合わせたダッシュボードを構築する
  - ML による予測値
  - 異常インジケーター
  - Tag Spotlight のインサイト
  - Related Content のリンク

## フィードバックの提供

皆さまのフィードバックは AI 機能の改善に役立ちます

- 不正確な AI の提案を Splunk Support を通じて報告する
- 成功事例を Splunk アカウントチームと共有する
- 新しい AI 機能のプレビュープログラムに参加する
- コミュニティのディスカッションに貢献する

## ありがとうございました

このワークショップにご参加いただきありがとうございます。AI と ML はオブザーバビリティを変革し、大規模な複雑なシステムの管理をより容易にしています。これらのツールを習得することで、皆さま自身と組織をモダンなクラウドネイティブ環境で成功するためのポジションに置くことができます。

### ご質問がありますか？

- Splunk アカウントチームにお問い合わせください
- [Splunk Community](https://community.splunk.com/) をご覧ください
- [Splunk Docs](https://docs.splunk.com/) をご確認ください

{{% notice title="Next Workshop" style="primary" icon="forward" %}}
さらに学びたいですか？Splunk Observability Cloud の特定の分野の専門知識を深めるために、他の [Splunk4Ninjas ワークショップ](/ninja-workshops/) をご覧ください。
{{% /notice %}}

---

**ワークショップ完了！** このワークショップが皆さまのお役に立てたことを願っています。AI を活用してオブザーバビリティの実践を強化していきましょう！
