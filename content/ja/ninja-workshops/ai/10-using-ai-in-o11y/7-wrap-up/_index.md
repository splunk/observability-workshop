---
title: まとめと次のステップ
linkTitle: 7. まとめ
weight: 7
---

## ワークショップのまとめ

おめでとうございます！「Using AI in Splunk Observability Cloud」ワークショップを完了しました。プラットフォームの AI および ML 機能について学んだ内容を振り返りましょう。

## 重要なポイント

### 1. Related Content

- AI が文脈に応じた関連ダッシュボード、ディテクター、リソースを提示します
- 調査時のナビゲーションと発見を加速します
- 利用パターンとメタデータの関係性から学習します
- **ベストプラクティス**: 一貫したタグ付けと命名規則を使用してください

### 2. AutoDetect と ML 駆動のディテクター

- 機械学習によりインテリジェントなディテクターを自動的に作成します
- 環境固有のパターンと季節性に適応します
- 動的なしきい値によりアラートノイズを削減します
- **ベストプラクティス**: ベースラインの確立に 1〜2 週間の時間を確保してください

### 3. Tag Spotlight

- すべてのタグディメンションにわたる AI 駆動の根本原因分析
- パフォーマンス問題に寄与するタグを自動的に特定します
- 手動でのフィルタリングと調査の時間を大幅に節約します
- **ベストプラクティス**: すべてのリソースに包括的かつ一貫したタグを適用してください

### 4. Log Observer AI

- パターン検出により類似ログを自動的にグループ化します
- 異常検出により通常と異なるログエントリを強調表示します
- インテリジェントなフィルタリングが関連フィールドを提案します
- **ベストプラクティス**: 一貫したフィールド名で構造化ログを使用してください

### 5. APM AI Assistant

- アプリケーション問題のトラブルシューティングのためのインテリジェントなガイダンス
- トレース内のボトルネックと異常の自動検出
- 自然言語によるインサイトとサマリー
- **ベストプラクティス**: 包括的なタグと属性でトレースを充実させてください

### 6. 予測分析

- ML モデルが将来のトレンドとキャパシティニーズを予測します
- 潜在的な問題のプロアクティブな特定
- キャパシティプランニングのためのトラフィック予測
- **ベストプラクティス**: 正確な予測のために一貫した履歴データを維持してください

## AI 駆動の調査ワークフロー

これらすべての AI 機能がどのように連携するかを以下に示します。

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

AI は提供されるデータの品質に左右されます。以下を確認してください。

- **包括的なタグ付け**: すべてのリソースに一貫してタグを付ける
- **豊富なメタデータ**: ビジネスおよび技術的なコンテキストを含める
- **構造化ログ**: JSON またはキーバリュー形式のログを使用する
- **完全なトレース**: すべてのサービスと依存関係を計装する
- **一貫した命名**: 標準的な命名規則を使用する

### シンプルに始めて、段階的に拡大

1. **1 つの AI 機能から始める**: AutoDetect または Tag Spotlight をまずマスターします
2. **検証とチューニング**: アラートを確認し、感度を調整します
3. **機能を追加する**: 追加の AI 機能を段階的に取り入れます
4. **ワークフローを統合する**: 調査において複数の AI 機能を組み合わせます
5. **自動化する**: AI のインサイトに基づいてランブックと自動化を構築します

### 継続的な改善

- **AI の提案を定期的に確認する**: 正確で有用ですか？
- **感度レベルをチューニングする**: アラートの品質に基づいて調整します
- **タグ付けを拡大する**: その価値を発見するにつれて新しいディメンションを追加します
- **ベースラインを更新する**: ML モデルが現在の通常状態を反映していることを確認します
- **知識を共有する**: AI が発見に役立ったパターンを文書化します

## 避けるべき一般的な落とし穴

| 落とし穴 | 影響 | 解決策 |
|---------|--------|----------|
| 履歴データが不十分 | ベースラインが不正確で、異常検出も不正確になります | 効果を判断する前に 1〜2 週間待ちます |
| タグ付けの不整合 | Tag Spotlight が適切に相関分析できません | タグ名と値を標準化します |
| 感度が高すぎる | 誤検知によるアラート疲労 | medium から始めて、結果に基づいてチューニングします |
| AI の提案を無視する | 価値のあるインサイトを逃します | 提案を調査し、フィードバックを提供します |
| 構造化されていないログ | パターン検出能力が制限されます | 構造化ログ形式に移行します |
| AI への過度な依存 | コンテキスト固有の問題を見逃します | AI のインサイトをドメインの専門知識と組み合わせます |

## AI のインパクトを測定する

AI の効果を測定するために、以下のメトリクスを追跡してください。

### 検出メトリクス

- **MTTD (Mean Time to Detect)**: 問題をより速く発見できていますか？
- **誤検知率**: AutoDetect のアラートは正確ですか？
- **カバレッジ**: インシデントの何パーセントが AI によって検出されましたか？

### 調査メトリクス

- **MTTR (Mean Time to Resolve)**: より速く解決できていますか？
- **根本原因までの時間**: Tag Spotlight はどれくらい早く問題を特定しますか？
- **調査ステップ**: 必要な手動ステップは少なくなりましたか？

### 効率メトリクス

- **確認したアラート**: シグナルが多く、ノイズが少なくなりましたか？
- **ダッシュボード利用**: 適切なダッシュボードをより速く見つけられますか？
- **チームのベロシティ**: 同じリソースでより多くの問題を解決できていますか？

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

### 最新情報の入手

- Splunk 製品アップデートを購読する
- Splunk AI/ML 機能のリリースをフォローする
- 新しい AI 機能のプレビュープログラムに参加する

## ハンズオン演習

### 学習の次のステップ

1. クリティカルなサービスに対して **AutoDetect ディテクターを作成する**
2. Troubleshooting MetricSets を使用して **Tag Spotlight を構成する**
3. 実際のログデータで **ログパターンを探索する**
4. これらの機能を活用する **AI を意識したランブックを構築する**
5. **チームと共有し**、ベストプラクティスを確立する

### チャレンジ演習

さらなる学習をご希望の方は、以下の高度な演習を試してみてください。

#### Challenge 1: AI 駆動のランブックを構築する

複数の AI 機能を組み合わせたランブックを作成します。

- AutoDetect ディテクターのトリガー
- Tag Spotlight が範囲を特定
- Related Content が関連ダッシュボードを発見
- Log Observer AI が根本原因を確認

#### Challenge 2: タグ付け戦略を最適化する

- サービス全体の現在のタグを監査する
- Tag Spotlight が苦戦するであろうギャップを特定する
- 追加のディメンションを実装する
- 調査速度の改善を測定する

#### Challenge 3: ML ディテクターをチューニングする

- クリティカルなメトリクスに対して AutoDetect をデプロイする
- 2 週間モニタリングする
- アラート品質 (真陽性 vs 偽陽性) を分析する
- 感度を調整して結果を比較する

#### Challenge 4: AI 強化されたダッシュボードを作成する

- 以下を組み合わせたダッシュボードを構築します。
  - ML が予測する値
  - 異常インジケーター
  - Tag Spotlight のインサイト
  - Related Content のリンク

## フィードバックの提供

皆さまのフィードバックは AI 機能の改善に役立ちます。

- 不正確な AI の提案は Splunk Support を通じて報告してください
- 成功事例を Splunk アカウントチームと共有してください
- 新しい AI 機能のプレビュープログラムに参加してください
- コミュニティでのディスカッションに貢献してください

## 謝辞

このワークショップにご参加いただきありがとうございました。AI と ML はオブザーバビリティを変革しており、複雑なシステムを大規模に管理することがより容易になっています。これらのツールをマスターすることで、現代のクラウドネイティブ環境において、ご自身と組織の成功に向けた基盤を築くことができます。

### ご質問は？

- Splunk アカウントチームにお問い合わせください
- [Splunk Community](https://community.splunk.com/) を訪問してください
- [Splunk Docs](https://docs.splunk.com/) をご確認ください

{{% notice title="次のワークショップ" style="primary" icon="forward" %}}
さらに学習をご希望ですか？他の [Splunk4Ninjas workshops](/ninja-workshops/) もチェックして、Splunk Observability Cloud の特定の領域に関する専門知識を深めてください。
{{% /notice %}}

---

**ワークショップ完了！** お役に立てたなら幸いです。さあ、AI を活用してオブザーバビリティの実践を強化していきましょう！
