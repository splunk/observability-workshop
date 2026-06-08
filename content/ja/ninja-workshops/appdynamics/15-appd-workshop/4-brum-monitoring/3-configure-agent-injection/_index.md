---
title: Configure Agent Injection
time: 3 minutes
weight: 3
description: この演習では、JavaScript Injection を有効にし、インジェクション対象の BT を選択します。
---

この演習では、以下のタスクを完了します

* JavaScript Agent インジェクションを有効にします。
* インジェクション対象の Business Transactions を選択します。

## JavaScript Agent インジェクションの有効化

AppDynamics は JavaScript Agent をインジェクトするさまざまな方法をサポートしていますが、このラボでは Auto-Injection 方式を使用します。以下の手順に従って、JavaScript Agent の Auto-Injection を有効にしてください。

1. 左メニューの **Applications** タブをクリックし、Supercar-Trader-## アプリケーションにドリルインします。
2. 左メニュー下部の **Configuration** タブをクリックします。
3. **User Experience App Integration** オプションをクリックします。

![BRUM Dash 1](images/03-brum-app-integration.png)

4. **JavaScript Agent Injection** タブをクリックします。
5. **Enable** をクリックして青色に変えます。
6. **Supercar-Trader-Web-##-####** が選択されたブラウザアプリであることを確認します。前のセクションで作成したアプリケーションを選択してください。
7. **Enable JavaScript Injection** の下にある **Enable** チェックボックスにチェックを入れます。
8. **Save** をクリックします。

![BRUM Dash 2](images/03-brum-agent-injection.png)
  
Auto-Injection が潜在的な Business Transactions を検出するまで数分かかります。この間に、以下の手順で Business Transaction Correlation を有効にしてください。新しい APM エージェントでは、これは自動的に行われます。

9. **Business Transaction Correlation** タブをクリックします。
10. **Manually Enable Business Transactions** セクションの下にある **Enable** ボタンをクリックします。
11. **Save** をクリックします。

![BRUM Dash 3](images/03-brum-bt-manual.png)

## インジェクション対象の Business Transactions の選択

以下の手順に従って、Auto-Injection 対象の Business Transactions を選択します。

1. **JavaScript Agent Injection** タブをクリックします。
2. 検索ボックスに **.do** と入力します。
3. すべての 9 つの BT が表示されるまで、Business Transactions の **Refresh List** リンクをクリックします。
4. 右側のリストボックスからすべての Business Transactions を選択します。
5. 矢印ボタンをクリックして、左側のリストボックスに移動します。
6. すべての Business Transactions が左側のリストボックスに移動されたことを確認します。
7. **Save** をクリックします。

JavaScript Agent の Automatic Injection の設定について詳しくは、[**こちら**](https://help.splunk.com/en/appdynamics-saas/end-user-monitoring/25.7.0/end-user-monitoring/browser-monitoring/browser-real-user-monitoring/inject-the-javascript-agent/automatic-injection-of-the-javascript-agent)をご覧ください。

![BRUM Dash 5](images/03-brum-bts-auto-inject.png)

Browser Application にロードが表示され始めるまで数分お待ちください。
