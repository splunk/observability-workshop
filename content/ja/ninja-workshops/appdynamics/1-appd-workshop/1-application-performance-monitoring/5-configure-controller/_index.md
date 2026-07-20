---
title: 5. Controllerの設定
weight: 5
description: このセクションでは、Controller内のさまざまなAPM設定を構成する方法を学びます
---


この演習では、以下のタスクを完了します。

- Business Transactionの設定を調整する
- Call Graphの設定を調整する
- Business Transactionの変更を確認する

## Business Transactionの設定を調整する  

前の演習では、Business Transactionが自動検出されていることを確認しました。Business Transactionの自動検出ルールを最適な状態に調整したい場合があります。今回のサンプルアプリケーションは古いApache Strutsフレームワーク上に構築されているため、このケースに該当します。  

以下の画像で強調表示されているBusiness Transactionは、各ペアにStruts Action（.execute）とServletタイプ（.jsp）があることを示しています。トランザクション検出ルールの設定を調整して、これら2種類のトランザクションを1つに統合します。  

AppDynamics UIで時間枠セレクターが表示されている場合、表示されるビューは選択された時間枠のコンテキストを表します。事前定義された時間枠から選択するか、表示したい特定の日付と時間範囲でカスタム時間枠を作成できます。

1. 過去1時間の時間枠を選択します。
2. マウスを青いアイコンの上にホバーして、トランザクションのEntry Point Typeを確認します。

![List of Business Transactions](images/business-transactions-list.png)

以下の手順に従ってトランザクション検出を最適化します。  

1. 左下メニューの **Configuration** オプションをクリックします。
2. **Instrumentation** リンクをクリックします。

    ![Configure Instrumentation](images/configure-instrumentation.png)

3. Instrumentationメニューから **Transaction Detection** を選択します。
4. **Java Auto Discovery Rule** を選択します。
5. **Edit** をクリックします。

    ![Edit Java Rules](images/edit-java-rule.png)  

6. Rule Editorの **Rule Configuration** タブを選択します。
7. **Struts Action** セクションのすべてのチェックボックスをオフにします。
8. **Web Service** セクションのすべてのチェックボックスをオフにします。
9. 下にスクロールしてServletの設定を見つけます。
10. **Enable Servlet Filter Detection** のチェックボックスをオンにします（Servlet設定では3つすべてのチェックボックスがオンになっている必要があります）。
11. **Save** をクリックして変更を保存します。

Transaction Detection Rulesの詳細については[こちら](https://help.splunk.com/en/appdynamics-saas/application-performance-monitoring/25.7.0/configure-instrumentation/transaction-detection-rules)を参照してください。

![Rule Configuration](images/rule-configuration1.png)  
![Rule Configuration Cont](images/rule-configuration2.png)  

## Call Graphの設定を調整する

以下に表示されるCall Graph Settingsウィンドウで、トランザクションスナップショット内のCall Graphでキャプチャされるデータを制御できます。このステップでは、SQL Captureの設定を変更して、各SQLクエリのパラメータが完全なクエリとともにキャプチャされるようにします。以下の手順でSQL Captureの設定を変更できます。

1. Instrumentationウィンドウから **Call Graph Settings** タブを選択します。これは前の演習で移動した **Instrumentation** 設定内にあります。
2. 設定内で **Java** タブが選択されていることを確認します。
3. **SQL Capture Settings** が表示されるまで下にスクロールします。
4. **Capture Raw SQL** オプションをクリックします。
5. **Save** をクリックします。

Call Graph設定の詳細については[こちら](https://help.splunk.com/en/appdynamics-saas/application-performance-monitoring/25.7.0/configure-instrumentation/call-graph-settings)を参照してください。  

![Call Graph Configuration](images/call-graph-config.png)  

## Business Transactionの変更を確認する

新しいBusiness Transactionが以前のトランザクションに置き換わるまで最大30分かかる場合があります。新しいトランザクションが検出されると、Business Transactionのリストは以下の例のように表示されます。

1. 左メニューの **Business Transactions** をクリックします。
2. 時間範囲ピッカーを **last 15 minutes** に調整します。

![Updated BTs](images/updated_business_transactions.png)
