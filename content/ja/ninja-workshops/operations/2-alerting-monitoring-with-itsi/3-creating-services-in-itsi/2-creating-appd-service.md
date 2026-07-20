---
title: AppDベースのサービスの作成
linkTitle: 3.2 AppDベースのサービスの作成
weight: 3
---

# AppDynamicsベースのサービスの作成

1. **サービスへのアクセス:** ITSIで「Configuration」をクリックし、「Services」をクリックします。

2. **サービスの作成: AD-Ecommerce2:** 「Create Service -> Create Service」をクリックします。

3. **サービスの詳細（AD-Ecommerce2）:**
    * **Title:** 「AD-Ecommerce2」
    * **Description（任意）:** 例: 「Ecommerce Service - version 2」

4. **テンプレートの選択:** 「Link service to a service template」を選択し、テンプレートのドロップダウンから「AppDynamics App Performance Monitoring」を検索します。 **Create** をクリックして新しいサービスを保存します。

5. **エンティティの割り当て:**
    * ページが読み込まれ、新しいサービスが表示され、Entitiesページが表示されます。このデモではデフォルトで *AD-Ecommerce:18112:demo1.saas.appdynamics.com* エンティティが選択されます。実際の環境では、entity_nameをエンティティ名に手動でマッチさせる必要があります。
    * **直接エンティティ選択（利用可能な場合）:** `entity_name="AD-Ecommerce:18112:demo1.saas.appdynamics.com"` を使用してエンティティを検索し、選択します。

6. **Settings:** 「Settings」タブをクリックし、 *Backfill* を有効にして標準の7日間のままにします。サービスを有効にし、「Save」をクリックします。

## AD-Ecommerce2のサービス正常性をAD.Ecommerceの依存関係として設定する

1. **サービスページに戻る:** 「Configuration -> Services」をクリックします。

2. **AD.Ecommerceを見つける:** サービスリストで「AD.Ecommerce」サービスを見つけます。

3. **AD.Ecommerceを編集する:** 「Edit」をクリックします。

4. **Service Dependencies:** 「Service Dependencies」セクションを探します。

5. **依存関係の追加:** 依存サービスを追加するオプションがあります。「AD-Ecommerce2」を検索します。

6. **KPIの選択:** AD-Ecommerce2のServiceHealthScoreの横にあるチェックボックスをオンにします。

7. **変更の保存:** 「AD.Ecommerce」サービスへの変更を保存します。

## 確認

* 「Service Analyzer」をクリックし、「Default Analyzer」を選択します
* サービスを「Buttercup Business Health」のみにフィルタリングします
* *AD-Ecommerce2* が *AD.Ecommerce* の下に表示され、グレーのステータスになっていることを確認します

![show-entry](../images/service_tree_appd.png?classes=inline)
