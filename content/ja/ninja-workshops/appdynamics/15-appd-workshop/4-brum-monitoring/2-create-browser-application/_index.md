---
title: Browser Application の作成
time: 2 minutes
weight: 2
description: この演習では、Controller でアプリケーションを作成し設定します。
---

この演習では、以下のタスクを完了します

* Web ブラウザから AppDynamics Controller にアクセスします。
* Controller で Browser Application を作成します。
* Browser Application を設定します。

## Controller にログインする

Cisco の認証情報を使用して [AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) にログインします。

## Controller で Browser Application を作成する

以下の手順に従って、新しい Browser Application を作成します。

{{% notice title="Note" style="primary"  %}}
以下のステップ 5 で、Browser Application に**一意の名前**を作成することが**非常に重要**です。
{{% /notice %}}

1. 上部メニューの **User Experience** タブをクリックします。
2. **User Experience** の下にある **Browser Apps** オプションをクリックします。
3. **Add App** をクリックします。
4. **Create an Application manually** オプションを選択します。
5. Browser Application の一意の名前を _Supercar-Trader-Web-<your\_initials\_or\_name>-<four\_random\_numbers>_ の形式で入力します。
    * 例 1: Supercar-Trader-Web-JFK-3179
    * 例 2: Supercar-Trader-Web-JohnSmith-0953
6. **OK** をクリックします。

![Create App](images/02-brum-create-app.png)

**Supercar-Trader-Web-##-####** アプリケーションの **Browser App Dashboard** が表示されます。

1. 左メニューの **Configuration** タブをクリックします。
2. **Instrumentation** オプションをクリックします。

![Instrumentation](images/02-brum-instrument.png)

以下の手順に従って、ブラウザモニタリングエージェントがキャプチャしたデータとともに IP アドレスが保存されるようにデフォルト設定を変更します。

3. **Settings** タブをクリックします。
4. 右側のスクロールバーを使用して画面の一番下までスクロールします。
5. **Store IP Address** チェックボックスにチェックを入れます。
6. **Save** をクリックします。

Browser RUM の Controller UI の設定について詳しくは[こちら](https://help.splunk.com/en/appdynamics-saas/end-user-monitoring/25.7.0/end-user-monitoring/browser-monitoring/browser-real-user-monitoring/overview-of-the-controller-ui-for-browser-rum/configure-the-controller-ui-for-browser-rum)をご覧ください。

![IPAddress Config](images/02-brum-ipaddress.png)
