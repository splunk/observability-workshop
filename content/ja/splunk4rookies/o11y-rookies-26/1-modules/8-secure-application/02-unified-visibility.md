---
title: Unified Visibility
linkTitle: 02-Unified-Visibility
weight: 2
---

## 統合的な可視性が重要な理由

信頼性とセキュリティが別々のツールに存在する場合、優先順位付けの議論が停滞します。SRE は*何が壊れたのか？*と問い、AppSec は*何が悪用可能か？*と問いますが、どちらのビューも同時に不健全かつ高リスクなサービスを表示しません。

Splunk Secure Application は、**APM Overview**、**Service Map**、および**サービスごとの Application Security** ワークスペース上で、ゴールデンシグナルと並べて脆弱性と攻撃のサマリーを表示します。エンジニアリング、アプリケーションセキュリティ、SecOps は、重複するエージェントやワークフローなしで1つのランタイムビューを共有できます。

### APM Overview でのセキュリティ態勢

セキュリティと信頼性を統合し、チームがアプリケーションのパフォーマンスと動作を理解するのと同じ場所で Application Security のリスクを確認できるようにします。

{{% notice title="Exercise" style="green" icon="running" %}}

1. **APM → Overview** に移動します。
2. **environment** フィルターを 'astronomy-shop-*' に設定します。
3. **Services** タブまでスクロールします。

各サービス行を確認してください。標準的なヘルスメトリクスに加えて、インストルメント済みサービスのランタイム脆弱性と脅威プロファイルのサマリー（Critical および High の CVE と攻撃の件数）が表示されます。

![apm](../images/02-overview.png)
{{% /notice %}}

### Service Map のランタイムセキュリティウィジェット

上位の脆弱性（CVE タイトル、ID、CVSS スコア、ライブラリ）と攻撃アクティビティ（タイプと結果）を、サービスの集約的かつ相関されたビューで確認できます。

{{% notice title="Exercise" style="green" icon="running" %}}

1. **APM → Service Map** に移動します。
2. **Services** フィルターを開き、**'ad'** を選択します。
3. Service Map 内の **`ad`** ノードをクリックします。
4. **Runtime Vulnerabilities** と **Attacks** ウィジェット（画面右側）までスクロールします。

![apm](../images/02-servicemap.png)
{{% /notice %}}

（オプション）- 脆弱性または攻撃の詳細（関連するウィジェットから）にドリルインして、ナビゲーションパスを確認します。

{{% notice title="Note" style="info" %}}
このビューは、すべての関連する依存関係、アプリケーショントラフィック、パフォーマンスパターンと並べて問題を表示する Blast-radius 思考を強調します。
{{% /notice %}}

### 学んだこと

- APM Overview でサービスの健全性と脆弱性・脅威プロファイルを相関させる方法。
- Service Map ウィジェットがトポロジーコンテキストでセキュリティの問題をどのように表示するか。
- サービスごとの Application Security が APM ワークスペース内でトリアージを維持する方法。
