---
title: AI を活用したログ分析
linkTitle: 5. Log Observer AI
weight: 5
---

## Log Observer の AI 機能

Splunk Observability Cloud の Log Observer には、大量のログデータを理解するのに役立つ AI 搭載機能がいくつか含まれています。

- **Pattern Detection**: ログ内の共通パターンを自動的に識別します
- **Anomaly Highlighting**: 異常なログエントリやパターンを浮き彫りにします
- **Log Clustering**: 類似のログメッセージをグループ化します
- **Intelligent Filtering**: コンテキストに基づき AI が提案するフィルター
- **Natural Language Queries**: 平易な言葉でログをクエリできます (利用可能な場合)

## Pattern Detection

### Log Pattern Detection とは

個々のログ行を表示する代わりに、Pattern Detection は構造ごとにログをグループ化し、以下を容易にします。

- 頻出パターンと希少パターンの識別
- 新しいパターンや異常なログパターンの発見
- 異常エントリへの集中
- 反復的なログによるノイズの削減

### 仕組み

AI エンジンは以下を実行します。

1. ログメッセージの構造を分析
2. 可変部分 (ID、タイムスタンプ、値) を識別
3. パターンテンプレートを作成
4. テンプレートごとにログをグループ化
5. パターンの頻度と変化を追跡

## ハンズオン演習: ログパターンの探索

{{% notice title="演習" style="primary" icon="tasks" %}}

### Step 1: Log Observer にアクセス

1. **Log Observer** に移動します
2. アクティブなログデータがある時間範囲を選択します
3. 多様なログを持つサービスまたはインデックスを選びます

### Step 2: Pattern ビューを有効化

1. **Patterns** または **Pattern Analysis** ビューを探します
2. 個別ログビューからパターンビューに切り替えます
3. ログがどのようにクラスタリングされているかを観察します

### Step 3: パターンの分析

パターンリストを確認します。

- **High-frequency patterns**: 通常の想定どおりのログ
- **New patterns**: 最近出現したもの (潜在的な問題)
- **Rare patterns**: 頻度が低く、調査する価値のあるもの
- **Error patterns**: 構造化されたエラーメッセージ

### Step 4: 異常の調査

1. 希少または新しいパターンをクリックします
2. そのパターンに含まれるサンプルログを表示します
3. ベースライン/通常パターンと比較します
4. 問題を示しているか判断します

{{% /notice %}}

## ログ異常検知

### 検知される異常の種類

1. **Frequency Anomalies**: ログ量の急増/急減
2. **Content Anomalies**: 異常なフィールド値やメッセージ内容
3. **Pattern Anomalies**: ベースラインに存在しない新しいパターン
4. **Timing Anomalies**: 通常とは異なる時間に出現するログ

### 異常検知の設定

ML を活用したログベースの Detector をセットアップします。

1. **Alerts & Detectors** に移動します
2. Log Observer から新しい Detector を作成します
3. **Anomaly Detection** モードを選択します
4. 以下を設定します。
   - ベースライン期間
   - 感度レベル
   - アラート条件
   - 通知チャネル

## インテリジェントなログフィルタリング

### AI が提案するフィルター

調査を進める中で、Log Observer は以下を提案することがあります。

- **Related fields**: フィルターに使う価値のあるタグや属性
- **Common values**: 頻繁に出現するフィールド値
- **Anomalous values**: 注目に値する異常なフィールド値
- **Correlated attributes**: 共に出現することが多いフィールド

### 提案フィルターの利用

1. UI 上のフィルター提案を探します
2. クリックして提案フィルターを適用します
3. 結果に基づいて絞り込みます
4. 有用なフィルターの組み合わせを保存します

## APM とインフラストラクチャとのログ相関

### 自動的なコンテキストリンク

AI は以下にログを接続するのに役立ちます。

- **Traces**: ログエントリを分散トレースにリンク
- **Services**: ログを APM サービスに関連付け
- **Infrastructure**: ホスト、コンテナ、Pod に接続
- **Metrics**: ログパターンとメトリクスの変化を相関

### AI のパンくずを辿る

調査中は以下を実行します。

1. ログエントリやパターンから始めます
2. **Related Content** の提案を探します
3. 相関するトレース、メトリクス、インフラストラクチャにジャンプします
4. Tag Spotlight を使用して問題を絞り込みます
5. ログに戻って結果を検証します

## ログの要約とインサイト

### Key Insights パネル

AI が生成するインサイトには以下が含まれる場合があります。

- **Error rate summaries**: エラーの種類別にグループ化
- **Service health**: ログの重大度に基づく
- **Trend analysis**: ログパターンの経時的変化
- **Comparative analysis**: 現在対ベースライン期間

### インサイトの例

```text
⚠️ Error rate increased 340% in the last hour
   → Top error: "Database connection timeout" (1,247 occurrences)
   → Affected services: checkout-service, payment-service
   → Started at: 14:23 UTC

📊 New log pattern detected
   → "WARN: Cache miss for key {key}" appeared 892 times
   → First seen: 14:25 UTC
   → May indicate cache invalidation issue
```

## AI を活用したログ分析のベストプラクティス

### 1. ログを構造化する

構造化ログを使用して AI を支援します。

```json
{
  "timestamp": "2024-01-15T14:23:45Z",
  "level": "ERROR",
  "service": "checkout-service",
  "message": "Payment processing failed",
  "error_code": "PAYMENT_TIMEOUT",
  "transaction_id": "txn_123456",
  "customer_tier": "enterprise"
}
```

### 2. 一貫したフィールド名を使用する

- サービス間でフィールド命名を標準化します
- 共通の分類体系を使用します (例: `serviceName` や `service_id` ではなく `service.name`)
- すべてのログに必須コンテキストを含めます

### 3. 適切なログレベルを設定する

- **DEBUG**: 詳細な診断情報 (開発用)
- **INFO**: 一般的な情報メッセージ
- **WARN**: 潜在的に有害な状況
- **ERROR**: アプリの継続を許す可能性のあるエラーイベント
- **FATAL**: 早期終了を引き起こす重大なエラー

### 4. ログサンプリングを活用する

大量のログに対して以下を実施します。

- AI を使用して代表的なサンプルを特定します
- エラーログと異常に集中します
- インテリジェントサンプリングを適用してコストを削減します

### 5. ログベースの Detector を作成する

以下に対するアラートをセットアップします。

- 重大なエラーパターン
- 異常なログ量
- 新しいエラータイプ
- セキュリティに関連するパターン

## ユースケース

### ユースケース 1: メモリリークの特定

**観察**: パターン分析で「GC pressure」警告の増加が示される

**AI による支援**:

- GC 関連のログパターンをグループ化
- 頻度の増加を強調
- メモリメトリクスと相関
- 影響を受けるサービストレースにリンク

### ユースケース 2: セキュリティ問題の検出

**観察**: 「Authentication failed」という新しいパターンが出現

**AI による支援**:

- 新規/希少パターンとしてフラグ付け
- 送信元 IP ごとにクラスタリング
- 異常なアクセスパターンを強調
- セキュリティ関連のフィルターを提案

### ユースケース 3: データベース性能劣化

**観察**: スロークエリ警告が増加

**AI による支援**:

- パターンごとにクエリをグループ化
- 最も遅いクエリタイプを特定
- データベースメトリクスと相関
- アプリケーショントレースにリンク

## 制限事項と考慮点

- **パターンの品質はログ構造に依存します**: 非構造化ログはパターン化が困難です
- **高カーディナリティフィールド**: UUID や一意の ID はパターンを分割する可能性があります
- **学習期間**: 異常検知には AI がベースラインデータを必要とします
- **コンテキストが鍵**: ログ AI を他のオブザーバビリティシグナルと組み合わせて使用します

{{% notice title="ヒント" style="info" icon="lightbulb" %}}
最も効果的なログ分析は、AI を活用したパターン検出とドメイン知識を組み合わせます。AI でシグナルを浮き彫りにし、専門知識で解釈してください。
{{% /notice %}}

## 次のステップ

Log Observer の AI 機能を理解したところで、アプリケーションのトラブルシューティングのために APM AI Assistant を探索しましょう。
