---
title: AppD ベースのサービスの作成
linkTitle: 3.2 AppD ベースのサービスの作成
weight: 3
---

# AppDynamics ベースのサービスから始める

1. **Services にアクセス:** ITSI で **Configuration** をクリックし、**Services** をクリックします。

2. **サービスを作成: AD-Ecommerce2:** **Create Service -> Create Service** をクリックします。

3. **サービスの詳細 (AD-Ecommerce2):**
    * **Title:** "AD-Ecommerce2"
    * **Description (Optional):** 例: "Ecommerce Service - version 2"

4. **テンプレートを選択:** **Link service to a service template** を選択し、テンプレートのドロップダウンから "AppDynamics App Performance Monitoring" を検索します。**Create** をクリックして新しいサービスを保存します。

5. **エンティティの割り当て:**
    * ページが読み込まれ、新しいサービスが表示され、Entities ページが表示されます。このデモでは、デフォルトで *AD-Ecommerce:18112:demo1.saas.appdynamics.com* エンティティが選択されます。実際の状況では、entity_name をエンティティ名に手動でマッチさせる必要があります。
    * **Direct Entity Selection (利用可能な場合):** `entity_name="AD-Ecommerce:18112:demo1.saas.appdynamics.com"` を使用してエンティティを検索し、選択します。

7. **Settings:** **Settings** タブをクリックし、*Backfill* を有効にして標準の7日間を維持します。サービスを有効にし、**Save** をクリックします。

## AD-Ecommerce2 の Service Health を AD.Ecommerce の依存関係として設定

1. **Services ページに戻る:** **Configuration -> Services** をクリックします

2. **AD.Ecommerce を見つける:** サービスリストで "AD.Ecommerce" サービスを見つけます。

3. **AD.Ecommerce を編集:** **Edit** をクリックします。

4. **Service Dependencies:** **Service Dependencies** セクションを探します。

5. **依存関係を追加:** 依存サービスを追加するオプションがあるはずです。"AD-Ecommerce2" を検索します。

6. **KPI を選択:** AD-Ecommerce2 の ServiceHealthScore の横にあるチェックボックスをオンにします。

7. **変更を保存:** "AD.Ecommerce" サービスへの変更を保存します。

## 確認

* **Service Analyzer** をクリックし、**Default Analyzer** を選択します
* サービスを "Buttercup Business Health" のみにフィルタリングします
* *AD-Ecommerce2* が *AD.Ecommerce* の下に表示され、グレーのステータスになっていることを確認します。

![show-entry](../images/service_tree_appd.png?classes=inline)