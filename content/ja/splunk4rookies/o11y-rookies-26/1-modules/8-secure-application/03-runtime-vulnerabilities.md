---
title: Runtime Vulnerabilities
linkTitle: 03-Runtime-Vulnerabilities
weight: 3
---

## 単一のインベントリビューが重要な理由

スタンドアロンの脆弱性スキャナーは、コードリポジトリやコンテナイメージに対する理論的な検出結果を報告することが多く、実際に稼働中の JVM やサービスにロードされているものを反映していません。チームはスプレッドシートをエクスポートし、CMDB エントリとクロスリファレンスしても、本番環境での露出に対する確信が得られません。

Splunk Secure Application は、デプロイされたアプリケーションおよびチームがパフォーマンストラブルシューティングに使用するのと同じ APM コンテキストに関連付けて、**ランタイムで**脆弱性を検出します。統合されたインベントリは、経営層の質問に答えます*現在のアプリケーションセキュリティリスクの露出状況はどうなっているか？*

### 脆弱性へのアクセス

{{% notice title="Exercise" style="green" icon="running" %}}

1. **Sevice-Map** → **Vulnerabilities Widget** に移動します
2. **Runtime Vulnerabilities** ラベルをクリックして脆弱性リストを開きます

![apm](../images/03a-runtime-vuln-lbl.png)

{{% /notice %}}

### ステークホルダービュー

インストルメント済みアプリケーション全体の脆弱性リストが以下の詳細とともに表示されます。

    - **CVE ID** - 標準的な脆弱性識別子
    - **CVSS Score** - 理論的な脆弱性深刻度スコア
    - **EPSS Score** - 脅威情報に基づくスコア
    - **Library** - 脆弱なライブラリの識別子
    - **Status** - トリアージ状態（例：Detected、Fixed、Ignored）
    - **Recommended action** - 特定された脆弱性を解決するための修復オプション
![apm](../images/03a-runtime-vuln-lst.png)

> [!NOTE]
> 詳細がわかっている場合は、特定の CVE を検索できます。また、脆弱性リストを **CVSS Score** でソートして、深刻度別（**Critical、Medium、Low**）に CVE を確認することもできます。

---

### 学んだこと

- サービスレベルおよび組織全体のランタイム脆弱性インベントリへのアクセス方法。
- CVE、CVSS、ステータス、Threat Risk Score が1つのビューにどのように表示されるか。
- コンテキスト化されたランタイムインベントリが、スタンドアロンのスキャンツールと比較してコンテキストスイッチングをどのように削減するか。
