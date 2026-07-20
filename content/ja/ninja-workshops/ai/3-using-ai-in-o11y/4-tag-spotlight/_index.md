---
title: Tag Spotlight - AIによる根本原因分析
linkTitle: 4. Tag Spotlight
weight: 4
---

## Tag Spotlightとは

Tag SpotlightはAIを活用した分析機能で、タグやメタデータ全体のパターンを自動的に分析することで、パフォーマンス問題の根本原因を迅速に特定できます。数百のタグの組み合わせを手動でフィルタリングする代わりに、Tag Spotlightは機械学習を使用して、パフォーマンス低下と最も強く相関するタグ値を強調表示します。

## Tag Spotlightが解決する問題

以下のようなサービスがあると想像してください

- 10の異なるリージョン
- リージョンごとに5つのアベイラビリティゾーン
- 20の異なるサービスエンドポイント
- 3つのデプロイバージョン

手動で確認するには最大3,000の組み合わせがあります。Tag Spotlightはすべての組み合わせを自動的に分析し、問題のあるものを表面化させます。

## Tag Spotlightの仕組み

Tag Spotlightはいくつかの分析手法を使用します

1. **Statistical Analysis**: すべてのタグ値間でパフォーマンスを比較します
2. **Pattern Recognition**: 多次元データの異常なパターンを特定します
3. **Contribution Analysis**: どのタグが問題に最も寄与しているかを計算します
4. **Correlation Scoring**: 問題との関連性でタグをランク付けします

## Tag Spotlightへのアクセス

Tag Spotlightは主に2つの場所で利用できます

### APM Service Mapsから

1. **APM** → **Services** に移動します
2. 問題が発生しているサービスを選択します
3. トラブルシューティングパネルで **Tag Spotlight** をクリックします

### Troubleshooting MetricSetsから

1. Troubleshooting MetricSet（TMS）を作成またはアクセスします
2. Tag SpotlightはTMS分析ビューに組み込まれています

## ハンズオン演習: Tag Spotlightの使用

{{% notice title="演習" style="primary" icon="tasks" %}}

### ステップ1: APMでTag Spotlightにアクセス

1. **APM** → **Services** に移動します
2. 複数のタグを持つサービスを選択します（例: 異なるリージョン、バージョン、エンドポイント）
3. **Tag Spotlight** または **Troubleshooting** セクションを探します

### ステップ2: 結果を分析

Tag Spotlightは以下を表示します

- **寄与度順にランク付けされたタグ**: パフォーマンス問題への寄与度
- **比較チャート**: タグ値ごとのパフォーマンス
- **寄与率**: 各タグの寄与率
- **統計的有意性**: 有意性の指標

### ステップ3: 結果の解釈

以下を確認します

- **寄与度の高いタグ**: 上位のタグが最も影響が大きい
- **外れ値**: 他と異なるパフォーマンスを示す特定のタグ値
- **時間の相関**: 乖離はいつ始まったか

### ステップ4: ドリルダウン

1. ハイライトされたタグ値をクリックしてビューをフィルタリングします
2. そのタグの特定のトレースやメトリクスを調査します
3. パフォーマンスが良好なタグ値と比較します
4. 根本原因を特定します（コード、インフラストラクチャ、設定）

{{% /notice %}}

## Tag Spotlightの結果を理解する

### Contribution Score

各タグに関連するパフォーマンス問題の割合を示します

```text
Region: us-west-2    → 78% contribution
Version: v2.3.1      → 45% contribution
Endpoint: /checkout  → 23% contribution
```

高い割合は問題との相関が強いことを示します。

### Statistical Significance

Tag Spotlightは以下も考慮します

- **Sample size**: 十分なデータポイントがあるか
- **Variance**: パターンはどの程度一貫しているか
- **Baseline comparison**: 通常時と比較してどうか

## 実際のユースケース

### ユースケース1: リージョンのパフォーマンス低下

**症状**: 全体のレイテンシーが300ms増加

**Tag Spotlightの結果**:

- `aws_region: eu-central-1` → 92% contribution
- 他のリージョンは正常に動作

**根本原因**: EUリージョンでのデータベースレプリケーション遅延

### ユースケース2: バージョンロールアウトの問題

**症状**: デプロイ後にエラー率が急上昇

**Tag Spotlightの結果**:

- `version: v3.0.1` → 85% contribution
- `endpoint: /api/search` → 67% contribution

**根本原因**: 新しい検索エンドポイントがメモリリークを引き起こした

### ユースケース3: 顧客セグメントへの影響

**症状**: チェックアウトのレイテンシーが増加

**Tag Spotlightの結果**:

- `tenant: enterprise-tier` → 71% contribution
- `payment_method: invoice` → 58% contribution

**根本原因**: 新しい請求バリデーションがエンタープライズの請求処理を遅延させている

## Tag Spotlightのベストプラクティス

### 1. 豊富なタグ付けを確保する

Tag Spotlightはタグの品質に依存します。以下を含めてください

- **インフラストラクチャタグ**: リージョン、AZ、クラスター、ノード
- **アプリケーションタグ**: バージョン、環境、フィーチャーフラグ
- **ビジネスタグ**: テナント、顧客ティア、プロダクトライン
- **カスタムディメンション**: ドメインに関連するすべてのもの

### 2. 一貫したタグ名を使用する

- サービス間で標準的な命名規則を使用します
- 同義語を避けます（例: `region` と `aws_region` を混在させない）
- タグ付け戦略を文書化します

### 3. 他のツールと組み合わせる

Tag Spotlightを以下と併用します

- **APM traces**: 実際のトレースデータで発見を検証
- **Metrics**: 時系列データでパターンを確認
- **Logs**: 特定されたタグのエラーメッセージを検索

### 4. Troubleshooting MetricSetsを作成する

重要なサービスには、以下を含むTroubleshooting MetricSetsを事前設定します

- 主要パフォーマンス指標（レイテンシー、エラー率、スループット）
- 重要なディメンション（リージョン、バージョン、エンドポイント）
- 適切なベースライン比較期間

## Troubleshooting MetricSets（TMS）

TMSはTag Spotlight向けに設計されたカスタムメトリクス集約です

### TMSの作成

1. **APM** → **Troubleshooting MetricSets** に移動します
2. **Create Troubleshooting MetricSet** をクリックします
3. サービスとメトリクスを選択します
4. 分析するディメンションを選択します
5. 保存して有効化します

### TMSを作成すべきタイミング

- **重要なサービス**: 厳格なSLAがあるサービス
- **複雑なアーキテクチャ**: 多くのディメンションを持つサービス
- **繰り返し発生する問題**: パフォーマンス変動が頻繁なサービス
- **マルチテナントシステム**: 顧客への影響が異なる場合

## 制限事項と考慮点

- **十分なデータが必要**: タグ値ごとに十分なサンプルが必要です
- **相関 ≠ 因果関係**: Tag Spotlightは相関を示します。根本原因は検証してください
- **タグのカーディナリティ**: 非常に高いカーディナリティのタグ（例: ユーザーID）は有用でない場合があります
- **時間ウィンドウが重要**: 適切な比較期間を選択してください

{{% notice title="ヒント" style="info" icon="lightbulb" %}}
Tag Spotlightは、分析対象の明確なパフォーマンス低下期間がある場合に最も効果的です。正確な結果を得るために、ベースラインと比較ウィンドウを慎重に定義してください。
{{% /notice %}}

## 次のステップ

Tag Spotlightを理解したところで、次はLog ObserverのAI機能を探索しましょう。
