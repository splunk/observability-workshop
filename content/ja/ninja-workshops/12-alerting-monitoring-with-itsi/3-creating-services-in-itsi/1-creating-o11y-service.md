---
title: O11y ベースのサービスの作成
linkTitle: 3.1 O11y ベースのサービスの作成
weight: 2
---

# Observability Cloud ベースのサービスから始める

1. **Services にアクセス:** ITSIで **Configuration** をクリックし、**Services** をクリックします。

2. **新しいサービスを作成: PaymentService2:** **Create New Service** をクリックします。

3. **サービスの詳細 (PaymentService2):**
    * **Title:** "PaymentService2"
    * **Description (Optional):** 例: "Payment Service for Hipster Shop - version 2"

4. **テンプレートを選択:** **Link service to a service template** を選択し、テンプレートのドロップダウンから "Splunk APM Business Workflow KPIs" を検索します。**Create** をクリックして新しいサービスを保存します。

5. **エンティティの割り当て:**
    * ページが読み込まれ、新しいサービスが表示され、Entitiesページが表示されます。このデモでは、デフォルトで *paymentservice:grpc.hipstershop.PaymentService/Charge* エンティティが選択されます。実際の状況では、ワークフローをエンティティ名に手動でマッチさせる必要があります。
    * **Direct Entity Selection (利用可能な場合):** `sf_workflow="paymentservice:grpc.hipstershop.PaymentService/Charge"` を使用してエンティティを検索し、選択します。

6. **サービスを保存 (PaymentService2):** **Save** をクリックして "PaymentService2" を作成します。

7. **Settings:** **Settings** タブをクリックし、*Backfill* を有効にして標準の7日間を維持します。サービスを有効にし、**Save** をクリックします。

## PaymentService2 の Service Health を Online-Boutique-US の依存関係として設定

1. **Online-Boutique-US を見つける:** サービスリストで "Online-Boutique-US" サービスを見つけます。

2. **Online-Boutique-US を編集:** **Edit** をクリックします。

3. **Service Dependencies:** **Service Dependencies** セクションを探します。

4. **依存関係を追加:** 依存サービスを追加するオプションがあるはずです。"PaymentService2" を検索します。

5. **KPI を選択:** PaymentService2のServiceHealthScoreの横にあるチェックボックスをオンにします。

6. **変更を保存:** "Online-Boutique-US" サービスへの変更を保存します。

## 確認

* **Service Analyzer** をクリックし、**Default Analyzer** を選択します
* サービスを "Buttercup Business Health" のみにフィルタリングします
* *PaymentService2* が *Online-Boutique-US* の下に表示され、グレーのステータスになっていることを確認します。

![show-entry](../images/service_tree_o11y.png?classes=inline)
