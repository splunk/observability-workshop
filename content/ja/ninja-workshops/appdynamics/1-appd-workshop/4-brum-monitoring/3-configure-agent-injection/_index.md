---
title: エージェントインジェクションの設定
time: 3 minutes
weight: 3
description: この演習では、JavaScript Injectionを有効にし、インジェクション対象のBTを選択します。
---

この演習では、以下のタスクを完了します。

* JavaScript Agentインジェクションを有効にする
* インジェクション対象のBusiness Transactionを選択する

## JavaScript Agentインジェクションの有効化

AppDynamicsはJavaScript Agentのインジェクションにさまざまな方法をサポートしていますが、このラボではAuto-Injectionメソッドを使用します。以下の手順に従って、JavaScript AgentのAuto-Injectionを有効にします。

1. 左メニューの **Applications** タブをクリックし、Supercar-Trader-##アプリケーションにドリルインします
2. 左メニュー下部の **Configuration** タブをクリックします
3. **User Experience App Integration** オプションをクリックします

![BRUM Dash 1](images/03-brum-app-integration.png)

1. **JavaScript Agent Injection** タブをクリックします
2. **Enable** をクリックして青色に変えます
3. **Supercar-Trader-Web-##-####** が選択されたブラウザアプリであることを確認します。前のセクションで作成したアプリケーションを選択してください
4. **Enable JavaScript Injection** の下にある **Enable** チェックボックスをオンにします
5. **Save** をクリックします

![BRUM Dash 2](images/03-brum-agent-injection.png)
  
Auto-Injectionが潜在的なBusiness Transactionを検出するまで数分かかります。その間に、以下の手順でBusiness Transaction Correlationを有効にします。新しいAPMエージェントでは、これは自動的に行われます。

1. **Business Transaction Correlation** タブをクリックします
2. **Manually Enable Business Transactions** セクションの下にある **Enable** ボタンをクリックします
3. **Save** をクリックします

![BRUM Dash 3](images/03-brum-bt-manual.png)

## インジェクション対象のBusiness Transactionの選択

以下の手順に従って、Auto-Injection対象のBusiness Transactionを選択します。

1. **JavaScript Agent Injection** タブをクリックします
2. 検索ボックスに **.do** と入力します
3. 9つのBTがすべて表示されるまで、Business Transactionの **Refresh List** リンクをクリックします
4. 右のリストボックスからすべてのBusiness Transactionを選択します
5. 矢印ボタンをクリックして、左のリストボックスに移動します
6. すべてのBusiness Transactionが左のリストボックスに移動されたことを確認します
7. **Save** をクリックします

JavaScript Agentの自動インジェクションの設定について詳しくは [**こちら**](https://help.splunk.com/en/appdynamics-saas/end-user-monitoring/25.7.0/end-user-monitoring/browser-monitoring/browser-real-user-monitoring/inject-the-javascript-agent/automatic-injection-of-the-javascript-agent) を参照してください。

![BRUM Dash 5](images/03-brum-bts-auto-inject.png)

Browserアプリケーションに負荷が表示され始めるまで数分お待ちください。
