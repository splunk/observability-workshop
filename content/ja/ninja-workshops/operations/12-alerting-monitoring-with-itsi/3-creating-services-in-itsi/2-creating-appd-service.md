---
title: Creating an AppD Based Service
linkTitle: 3.2 Creating an AppD Based Service
weight: 3
---

# AppDynamics ベースのサービスから始める

1. **Services にアクセス:** ITSI で "Configuration" をクリックし、"Services" をクリックします。

2. **サービスの作成 (AD-Ecommerce2):** "Create Service -> Create Service" をクリックします。

3. **サービスの詳細 (AD-Ecommerce2):**
    * **Title:** "AD-Ecommerce2"
    * **Description (Optional):**  例: "Ecommerce Service - version 2"

4. **テンプレートの選択:** "Link service to a service template" を選択し、テンプレートのドロップダウンから "AppDynamics App Performance Monitoring" を検索します。**Create** をクリックして新しいサービスを保存します。

5. **エンティティの割り当て:**
    * ページが読み込まれると新しいサービスが表示され、Entities ページが開きます。このデモではデフォルトで *AD-Ecommerce:18112:demo1.saas.appdynamics.com* エンティティが選択されています。実際の環境では、entity_name を手動でエンティティ名と一致させる必要があります。
    * **エンティティの直接選択 (利用可能な場合):** `entity_name="AD-Ecommerce:18112:demo1.saas.appdynamics.com"` を使用してエンティティを検索し、選択します。

6. **設定:** "Settings" タブをクリックし、*Backfill* を有効にして標準の 7 日間のままにします。サービスを有効化し、"Save" をクリックします。

## AD-Ecommerce2 のサービスヘルスを AD.Ecommerce の依存関係として設定する

1. **Services ページに戻る:** "Configuration -> Services" をクリックします。

2. **AD.Ecommerce を探す:** サービスリストから "AD.Ecommerce" サービスを見つけます。

3. **AD.Ecommerce を編集:** "Edit" をクリックします。

4. **Service Dependencies:** "Service Dependencies" セクションを探します。

5. **依存関係の追加:** 依存サービスを追加するオプションがあるはずです。"AD-Ecommerce2" を検索します。

6. **KPI の選択:** AD-Ecommerce2 の ServiceHealthScore の横にあるチェックボックスをオンにします。

7. **変更を保存:** "AD.Ecommerce" サービスの変更を保存します。

## 検証

* "Service Analyzer" をクリックし、"Default Analyzer" を選択します
* サービスを "Buttercup Business Health" のみにフィルタリングします
* *AD-Ecommerce2* が *AD.Ecommerce* の下に表示され、グレーのステータスになっていることを確認します。

![show-entry](../images/service_tree_appd.png?classes=inline)
