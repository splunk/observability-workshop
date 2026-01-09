---
title: 5. Controller 設定の構成
weight: 5
description: このセクションでは、Controller 内のさまざまな APM 設定を構成する方法を学びます
---


この演習では、以下のタスクを完了します：

- Business Transaction 設定を調整する
- Call Graph 設定を調整する
- Business Transaction の変更を確認する

## Business Transaction 設定の調整

前の演習で、Business Transactions が自動検出されていることを確認しました。Business Transaction の自動検出ルールを最適な状態に調整したい場合があります。これは、古い Apache Struts フレームワーク上に構築されたサンプルアプリケーションの場合に当てはまります。

以下の画像で強調表示されている Business Transactions は、各ペアに Struts Action（.execute）と Servlet タイプ（.jsp）があることを示しています。これら2種類のトランザクションが1つに統合されるように、トランザクション検出ルールの設定を調整します。

AppDynamics UI に時間枠セレクターが表示されている場合、表示されるビューは選択した時間枠のコンテキストを表します。事前定義された時間枠の1つを選択するか、表示したい特定の日付と時間範囲でカスタム時間枠を作成できます。

1. 過去1時間の時間枠を選択します。
2. マウスを青いアイコンの上に移動して、トランザクションの Entry Point Type を確認します。

![List of Business Transactions](images/business-transactions-list.png)

以下の手順に従ってトランザクション検出を最適化します：

1. 左下のメニューで **Configuration** オプションをクリックします。
2. **Instrumentation** リンクをクリックします。

    ![Configure Instrumentation](images/configure-instrumentation.png)

3. Instrumentation メニューから **Transaction Detection** を選択します。
4. **Java Auto Discovery Rule** を選択します。
5. **Edit** をクリックします。

    ![Edit Java Rules](images/edit-java-rule.png)  

6. Rule Editor で **Rule Configuration** タブを選択します。
7. **Struts Action** セクションのすべてのボックスのチェックを外します。
8. **Web Service** セクションのすべてのボックスのチェックを外します。
9. 下にスクロールして Servlet 設定を見つけます。
10. **Enable Servlet Filter Detection** ボックスにチェックを入れます（Servlet 設定では3つのボックスすべてにチェックが入っている必要があります）。
11. **Save** をクリックして変更を保存します。

Transaction Detection Rules の詳細については[こちら](https://help.splunk.com/en/appdynamics-saas/application-performance-monitoring/25.7.0/configure-instrumentation/transaction-detection-rules)をご覧ください。

![Rule Configuration](images/rule-configuration1.png)
![Rule Configuration Cont](images/rule-configuration2.png)

## Call Graph 設定の調整

以下に示す Call Graph Settings ウィンドウで、トランザクションスナップショット内の call graphs でキャプチャされるデータを制御できます。このステップでは、各 SQL クエリのパラメータが完全なクエリと共にキャプチャされるように SQL Capture 設定を変更します。以下の手順に従って SQL Capture 設定を変更できます。

1. Instrumentation ウィンドウから **Call Graph Settings** タブを選択します。これは、前の演習で移動した **Instrumentation** 設定内にあります。
2. 設定内で **Java** タブが選択されていることを確認します。
3. **SQL Capture Settings** が表示されるまで下にスクロールします。
4. **Capture Raw SQL** オプションをクリックします。
5. **Save** をクリックします。

Call Graph 設定の詳細については[こちら](https://help.splunk.com/en/appdynamics-saas/application-performance-monitoring/25.7.0/configure-instrumentation/call-graph-settings)をご覧ください。

![Call Graph Configuration](images/call-graph-config.png)

## Business Transaction の変更の確認

新しい Business Transactions が以前のトランザクションを置き換えるまでに最大30分かかる場合があります。新しいトランザクションが検出されると、Business Transactions のリストは以下の例のようになります。

1. 左側のメニューで **Business Transactions** をクリックします。
2. 時間範囲ピッカーを調整して **last 15 minutes** を確認します

![Updated BTs](images/updated_business_transactions.png)
