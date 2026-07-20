---
title: ITSIでのエピソード作成
linkTitle: 5. ITSIでのエピソード作成
weight: 1
---

# Splunk ITSIでの集約ポリシーの作成

このセクションでは、先ほど設定したアラートに一致する集約ポリシーをSplunk ITSIで作成する手順を説明します。このポリシーは関連するアラートをグループ化し、ノイズを削減してインシデント管理を改善します。

**作成したアラートに応じて、このアラートに使用するタイトルが変わります。以下の手順では、AlertNameを使用したサービス名に置き換えてください**

* **PaymentService2** または
* **AD-Ecommerce2**

## 手順

1. **Notable Event Aggregation Policiesに移動します:** Splunkで「Configuration」→「Notable Event Aggregation Policies」に移動します。

2. **新しいポリシーを作成します:** 右上隅の緑色の「Create Notable Event Aggregation Policy」ボタンをクリックします。

3. **フィルタリング条件:** これが最も重要な部分です。このポリシーでグループ化するアラートの条件を定義します。「Add Rule (OR)」をクリックします。

    * **Field:** ドロップダウンメニューから「title」を選択します。
    * **Operator:** 「matches」を選択します。
    * **Value:** 「*Service Name**」という文字列を入力します（*を含めることを確認してください）。

4. **イベントの分割:** デフォルトで設定されている「hosts」フィールドを削除し、「service」フィールドに更新します。検出された各サービスごとに新しいエピソードを生成するようにします。この例では、1つだけになるはずです。

5. **ブレーク条件:** エピソードがブレークまたは終了する方法を設定します。デフォルトの *「If an event occurs for which severity = Normal」* のままにします。右側のPreviewをクリックして、アラートが検出されていることを確認します。

6. **Nextをクリックします**

7. **アクション（オプション）:** 集約されたアラートに対して実行するアクションを定義します。例えば、ServiceNowでチケットを自動作成したり、メール通知を送信したりできます。この部分はスキップします。

8. **Nextをクリックします**

9. **ポリシーのタイトルと説明:**
    * **Policy Title:** *Service Name* Alert Grouping
    * **Description:** Grouping *Service Name* alerts together.

10. **ポリシーを保存します:** 「Next」ボタンをクリックして集約ポリシーを作成します。

## 検証

ポリシーを保存した後、「Go to Episode Review」ページに移動し、過去15分間のアラートをフィルタリングし、status=Newのフィルタを追加して、検索ボックスでサービス名を検索します。

特定のアラートにちなんだ名前のエピソードが既に存在する場合は、それをクローズして、新しいタイトルで新しいエピソードが生成されるのを待ちます。

![show-entry](../images/episode.png?classes=inline)
