---
title: ITSI でのエピソードの作成
linkTitle: 5. ITSI でのエピソードの作成
weight: 1
---

# Splunk ITSI での Aggregation Policy の作成

このセクションでは、先ほど設定したアラートに一致する Splunk ITSI での Aggregation Policy を作成する手順について説明します。このポリシーは関連するアラートをグループ化し、ノイズを減らしてインシデント管理を改善します。

**作成したアラートに応じて、このアラートに使用するタイトルが変わります。以下の手順では、AlertName を使用した Service Name に置き換えてください**

* **PaymentService2** または
* **AD-Ecommerce2**

## 手順

1. **Notable Event Aggregation Policies に移動:** Splunk で **Configuration** -> **Notable Event Aggregation Policies** に移動します。

2. **新しいポリシーを作成:** 右上隅にある緑色の **Create Notable Event Aggregation Policy** ボタンをクリックします。

3. **フィルタリング条件:** これが最も重要な部分です。このポリシーによってグループ化されるアラートの条件を定義します。**Add Rule (OR)** をクリックします

    * **Field:** ドロップダウンメニューから **title** を選択します。
    * **Operator:** **matches** を選択します。
    * **Value:** "*Service Name**" という文字列を入力します（* を含めることを忘れないでください）。

4. **イベントの分割:** デフォルトで提供されている "hosts" フィールドを削除し、"service" フィールドを使用するように更新します。これにより、見つかった各サービスごとに新しいエピソードが生成されます。この例では、1つだけになるはずです。

5. **終了条件:** エピソードがどのように終了するかを設定します。デフォルトの *"If an event occurs for which severity = Normal"* のままにします。右側の Preview をクリックして、アラートが正しく検出されていることを確認します

6. **Next をクリック**

7. **アクション（オプション）:** 集約されたアラートに対して実行するアクションを定義します。例えば、ServiceNow でチケットを自動作成したり、メール通知を送信したりできます。この部分はスキップします。

8. **Next をクリック**

9. **ポリシーのタイトルと説明:**
    * **Policy Title:** *Service Name* Alert Grouping
    * **Description:** Grouping *Service Name* alerts together.

8. **ポリシーを保存:** **Next** ボタンをクリックして Aggregation Policy を作成します。

## 確認

ポリシーを保存した後、**Go to Episode Review** ページに移動し、過去15分間のアラートをフィルタリングし、status=New のフィルターを追加して、検索ボックスで Service Name を検索します。

特定のアラートの名前が付いたエピソードがすでに存在する場合は、それを閉じて、新しいタイトルで新しいエピソードが生成されるのを待ちます。

![show-entry](../images/episode.png?classes=inline)

