---
title: Application Performance Monitoring Home page
linkTitle: 3.1 APM Home Page 
weight: 2
---
 
メインメニューから **APM** をクリックし、**Overview** を選択します。APM ホームページは 3 つの異なるセクションで構成されています。

![APM page](../images/apm-main.png)

1. **Onboarding Pane:** Splunk APM を始めるためのトレーニング動画とドキュメントへのリンクです。
2. **APM Overview Pane:** トップサービスとトップビジネスワークフローのリアルタイムメトリクスです。
3. **Functions Pane:** サービス、タグ、トレース、データベースクエリパフォーマンス、コードプロファイリングの詳細分析へのリンクです。

**APM Overview** ペインでは、アプリケーションの健全性をハイレベルで把握できます。アプリケーション内のサービス、レイテンシー、エラーのサマリーが含まれます。また、エラー率順のトップサービスと、エラー率順のトップビジネスワークフローのリストも含まれます（ビジネスワークフローとは、特定のアクティビティまたはトランザクションに関連するトレースの集合の最初から最後までの一連の流れであり、エンドツーエンドの KPI のモニタリングと、根本原因やボトルネックの特定を可能にします）。

{{% notice title=" About Environments" style="info" %}}

複数のアプリケーションを簡単に区別できるようにするため、Splunk では **environments**（環境）を使用します。ワークショップ環境の命名規則は **[NAME OF WORKSHOP]-workshop** です。インストラクターから選択すべき正しい環境名が伝えられます。

{{% /notice %}}

{{% exercise title="Filter APM to your workshop" %}}

* 操作対象の時間枠が直近 15 分（**-15m**）に設定されていることを確認します。
* ドロップダウンボックスから名前を選択して環境をワークショップ用のものに変更し、それだけが選択されていることを確認します。
{{< tabs >}}
{{% tab title="Question" %}}
***Top Services by Error Rate*** チャートから何が読み取れますか？**
{{% /tab %}}
{{% tab title="Answer" %}}
***paymentservice*** のエラー率が高いです**
{{% /tab %}}
{{< /tabs >}}
<!--
* Click on the Explore Tile in the Function Pane. This will bring us to the automatically generated map of our services. This map shows how the services interact together based on the trace data being sent to Splunk Observability Cloud.
-->
{{% /exercise %}}

Overview ページを下にスクロールしていくと、一部のサービスの隣に **Inferred Service** と表示されているのに気づくでしょう。

Splunk APM は、リモートサービスを呼び出すスパンに必要な情報があれば、リモートサービス、つまり推論サービス（inferred service）の存在を推論できます。推論サービスの例としては、データベース、HTTP エンドポイント、メッセージキューなどがあります。推論サービスはインスツルメンテーションされていませんが、サービスマップとサービスリストに表示されます。

次に、**Splunk Log Observer (LO)** を見てみましょう。
