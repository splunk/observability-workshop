---
title: ITSI でのエピソード作成
linkTitle: 5. ITSI でのエピソード作成
weight: 1
---

# Splunk ITSI での集約ポリシーの作成

このセクションでは、先ほど設定したアラートに一致する集約ポリシーを Splunk ITSI で作成する手順を説明します。このポリシーにより関連するアラートをグループ化し、ノイズを削減してインシデント管理を改善できます。

**作成したアラートに応じて、このアラートで使用するタイトルが変わります。以下の手順では、AlertName を使用したサービス名に置き換えてください。**

* **PaymentService2** または
* **AD-Ecommerce2**

## 手順

1. **Notable Event Aggregation Policies に移動:** Splunk で "Configuration" -> "Notable Event Aggregation Policies" に移動します。

2. **新しいポリシーの作成:** 右上にある緑色の "Create Notable Event Aggregation Policy" ボタンをクリックします。

3. **フィルタリング条件:** これが最も重要な部分です。このポリシーでグループ化するアラートの条件を定義します。"Add Rule (OR)" をクリックします。

    * **Field:** ドロップダウンメニューから "title" を選択します。
    * **Operator:** "matches" を選択します。
    * **Value:** 文字列 "*Service Name**" を入力します。（* を含めることを忘れないでください）

4. **イベントの分割:** デフォルトで提供されている "hosts" フィールドを削除し、"service" フィールドを使用するように更新します。これにより、見つかった各サービスごとに新しいエピソードが生成されます。今回の例では、1 つのみとなります。

5. **ブレーク条件:** エピソードがどのようにブレーク（終了）されるかを設定します。デフォルトの *"If an event occurs for which severity = Normal"* のままにします。右側の Preview をクリックして、アラートが取り込まれていることを確認します。

6. **Next をクリック**

7. **アクション（任意）:** 集約されたアラートに対して実行するアクションを定義します。たとえば、ServiceNow で自動的にチケットを作成したり、メール通知を送信したりできます。ここではこの部分をスキップします。

8. **Next をクリック**

9. **ポリシーのタイトルと説明:**
    * **Policy Title:** *Service Name* Alert Grouping
    * **Description:** Grouping *Service Name* alerts together.

10. **ポリシーの保存:** "Next" ボタンをクリックして集約ポリシーを作成します。

## 確認

ポリシーを保存した後、"Go to Episode Review" ページに移動し、過去 15 分間のアラートをフィルタリングして、status=New のフィルタを追加し、検索ボックスでサービス名を検索します。

すでに特定のアラート名のエピソードが存在する場合があります。その場合は、それをクローズして、新しいタイトルで新しいエピソードが生成されるのを待ちます。

![show-entry](../images/episode.png?classes=inline)
