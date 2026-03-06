# 翻訳ガイドライン詳細

## 目次

1. [用語集](#用語集)
2. [翻訳パターン](#翻訳パターン)
3. [避けるべき表現](#避けるべき表現)
4. [Hugo ショートコード](#hugo-ショートコード)

## 用語集

### 翻訳しない用語(Splunk Observability Cloud)

| 英語                       | 説明                               |
| -------------------------- | ---------------------------------- |
| Splunk                     | 製品名                             |
| Splunk Observability Cloud | 製品名                             |
| Log Observer               | 機能名                             |
| APM                        | Application Performance Monitoring |
| RUM                        | Real User Monitoring               |
| Kubernetes                 | 技術名                             |
| Docker                     | 技術名                             |
| Helm                       | ツール名                           |
| OpenTelemetry              | 技術名                             |
| OTEL                       | OpenTelemetry 略称                 |
| Collector                  | OpenTelemetry Collector            |
| Span                       | トレーシング用語                   |
| Trace                      | トレーシング用語                   |
| Metric                     | メトリクス                         |
| Dashboard                  | ダッシュボード（カタカナ可）       |
| Receiver                   | OpenTelemetry コンポーネント名     |
| Processor                  | OpenTelemetry コンポーネント名     |
| Exporter                   | OpenTelemetry コンポーネント名     |

その他、Splunk Observabitlity Cloudにおける機能名を差す単語

### カタカナ化する用語(Splunk Observability Cloud)

| 英語                 | 日本語                       |
| -------------------- | ---------------------------- |
| Workshop             | ワークショップ               |
| Container            | コンテナ                     |
| Cluster              | クラスター                   |
| Service              | サービス                     |
| Application          | アプリケーション             |
| Monitoring           | モニタリング                 |
| Observability        | オブザーバビリティ           |
| Instrumentation      | 計装                         |
| Auto-instrumentation | 自動計装                     |

### 翻訳する用語

| 英語            | 日本語               |
| --------------- | -------------------- |
| Navigate to     | ～に移動します       |
| Click on        | ～をクリックします   |
| Select          | ～を選択します       |
| Enter           | ～を入力します       |
| Copy            | ～をコピーします     |
| Paste           | ～を貼り付けます     |
| Run the command | コマンドを実行します |
| You should see  | ～が表示されます     |
| Make sure       | ～を確認してください |
| Note that       | 注意:                |

### 決まった訳がある単語(AppDynamics)

AppDynamicsでは、一部の単語には決まった日本語訳が割り当てられているため、その訳を尊重する

| 英語        | 日本語         |
| ----------- | -------------- |
| health rule | 正常性ルール   |

## 翻訳パターン

### 命令形 → です/ます形

```markdown
# 英語

Click the **Save** button.

# 日本語

**Save** ボタンをクリックします。
```

### 箇条書きの翻訳

```markdown
# 英語

- Navigate to the dashboard
- Click on **Metrics**
- Select the time range

# 日本語

- ダッシュボードに移動します
- **Metrics** をクリックします
- 時間範囲を選択します
```

### 見出しの翻訳

```markdown
# 英語

## Getting Started

# 日本語

## はじめに
```

```markdown
# 英語

## Prerequisites

# 日本語

## 前提条件
```

### リンクテキストの翻訳

```markdown
# 英語

See [the documentation](url) for more details.

# 日本語

詳細は[ドキュメント](url)を参照してください。
```

## 避けるべき表現

### 機械翻訳的な表現

| 避ける               | 推奨       |
| -------------------- | ---------- |
| あなたは～できます   | ～できます |
| ～することができます | ～できます |
| それは～です         | ～です     |
| 私たちは～します     | ～します   |

### 不自然な敬語

| 避ける         | 推奨                       |
| -------------- | -------------------------- |
| ～してください | ～します（手順説明の場合） |
| ～いただきます | ～します                   |

## Hugo ショートコード

### 変更しないもの

Hugo のショートコードは翻訳せず、そのまま維持する:

```markdown
{{< tabs >}}
{{% tab title="Linux" %}}
...
{{% /tab %}}
{{< /tabs >}}
```

### タイトル属性の翻訳

ショートコード内の `title` 属性は翻訳する場合がある:

```markdown
# 英語

{{% tab title="Step 1: Install" %}}

# 日本語

{{% tab title="ステップ1: インストール" %}}
```

### notice ショートコード

```markdown
# 英語

{{% notice title="Note" %}}
This is important information.
{{% /notice %}}

# 日本語

{{% notice title="注意" %}}
これは重要な情報です。
{{% /notice %}}
```

## 句読点

- 句点: `。`（全角）
- 読点: `、`（全角）
- コロン: `:` または `：`（文脈による）
- 括弧: `（）`（全角）または `()` （半角、技術用語内）

### 行末コロンの除去

英語では見出しや導入文の行末にコロン「:」を付ける慣行があるが、日本語では不自然なため「:」「：」を除去する。

```markdown
# 英語

The following options are available:

# 日本語
//よい例

以下のオプションが利用可能です。

//悪い例1

以下のオプションが利用可能です：

//悪い例2

以下のオプションが利用可能です:

```

## 数字

- 基本的に半角数字を使用

## スペーシング

半角文字（英数字）と全角文字（日本語）の間のスペースは、textlint-rule-preset-ja-spacingにより自動制御されます。

### ルール

- 半角・全角間にスペースを入れない: `Splunkの設定`（正）、`Splunk の設定`（誤）
- インラインコード前後にスペースを入れる: 値は `true` です（正）
- 全角括弧の前後にスペースを入れない: `設定（デフォルト）`（正）
- 全角文字同士の間にスペースを入れない
- 単位との間にスペースは入れない: `10GB`, `5分`

### 例外

- Markdown太字マークアップ（`**`）前後の意図的なスペースはtextlintの対象外
- コードブロック内はtextlintの対象外
