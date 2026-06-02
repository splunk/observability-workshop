---
title: Creating an O11y Based Service
linkTitle: 3.1 Creating an O11y Based Service
weight: 2
---

# Observability Cloud ベースのサービスから始める

1. **サービスへのアクセス:** ITSI で "Configuration" をクリックし、"Services" をクリックします。

2. **新しいサービス PaymentService2 を作成:** "Create New Service" をクリックします。

3. **サービスの詳細 (PaymentService2):**
    * **Title:** "PaymentService2"
    * **Description (Optional):**  例: "Payment Service for Hipster Shop - version 2"

4. **テンプレートを選択:** "Link service to a service template" を選択し、テンプレートのドロップダウンから "Splunk APM Business Workflow KPIs" を検索します。**Create** をクリックして新しいサービスを保存します。

5. **エンティティの割り当て:**
    * ページが読み込まれて新しいサービスが表示され、Entities ページが開きます。このデモではデフォルトで *paymentservice:grpc.hipstershop.PaymentService/Charge* エンティティが選択されます。実際の運用では、ワークフローをエンティティ名と手動で一致させる必要があります。
    * **エンティティの直接選択 (利用可能な場合):** `sf_workflow="paymentservice:grpc.hipstershop.PaymentService/Charge"` を使用してエンティティを検索し、選択します。

6. **サービスを保存 (PaymentService2):** "Save" をクリックして "PaymentService2" を作成します。

7. **設定:** "Settings" タブをクリックし、*Backfill* を有効にして標準の 7 日間のままにしておきます。サービスを有効にして、"Save" をクリックします。

## PaymentService2 のサービス正常性を Online-Boutique-US の依存関係として設定する

1. **Online-Boutique-US を見つける:** サービス一覧で "Online-Boutique-US" サービスを探します。

2. **Online-Boutique-US を編集:** "Edit" をクリックします。

3. **サービスの依存関係:** "Service Dependencies" セクションを探します。

4. **依存関係を追加:** 依存サービスを追加するオプションがあるはずです。"PaymentService2" を検索します。

5. **KPI を選択:** PaymentService2 の ServiceHealthScore の横のチェックボックスをオンにします。

6. **変更を保存:** "Online-Boutique-US" サービスへの変更を保存します。

## 検証

* "Service Analyzer" をクリックし、"Default Analyzer" を選択します。
* サービスを "Buttercup Business Health" のみにフィルタします。
* *PaymentService2* が *Online-Boutique-US* の下に表示され、グレーステータスになっていることを確認します。

![show-entry](../images/service_tree_o11y.png?classes=inline)
