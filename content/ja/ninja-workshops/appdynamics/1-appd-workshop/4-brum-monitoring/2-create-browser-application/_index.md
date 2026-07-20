---
title: Browser Applicationの作成
time: 2 minutes
weight: 2
description: この演習では、Controllerでアプリケーションを作成し設定します。
---

この演習では、以下のタスクを実施します。

* WebブラウザからAppDynamics Controllerにアクセスします。
* ControllerでBrowser Applicationを作成します。
* Browser Applicationを設定します。

## Controllerにログイン

Ciscoの資格情報を使用して [AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) にログインします。

## ControllerでBrowser Applicationを作成

以下の手順に従って、新しいBrowser Applicationを作成します。

{{% notice title="注意" style="primary"  %}}
以下のステップ5で、Browser Applicationに一意の名前を作成することが **非常に重要** です。
{{% /notice %}}

1. トップメニューの **User Experience** タブをクリックします。
2. **User Experience** の下にある **Browser Apps** オプションをクリックします。
3. **Add App** をクリックします。
4. **Create an Application manually** オプションを選択します。
5. _Supercar-Trader-Web-<your\_initials\_or\_name>-<four\_random\_numbers>_ の形式でBrowser Applicationの一意の名前を入力します。
    * 例1: Supercar-Trader-Web-JFK-3179
    * 例2: Supercar-Trader-Web-JohnSmith-0953
6. **OK** をクリックします。

![Create App](images/02-brum-create-app.png)

**Supercar-Trader-Web-##-####** アプリケーションの **Browser App Dashboard** が表示されます。

1. 左メニューの **Configuration** タブをクリックします。
2. **Instrumentation** オプションをクリックします。

![Instrumentation](images/02-brum-instrument.png)

以下の手順に従って、ブラウザモニタリングエージェントがキャプチャしたデータとともにIPアドレスが保存されるようにデフォルト設定を変更します。

1. **Settings** タブをクリックします。
2. 右側のスクロールバーを使用して画面の一番下までスクロールします。
3. **Store IP Address** チェックボックスをオンにします。
4. **Save** をクリックします。

Browser RUM用のController UIの設定について詳しくは[こちら](https://help.splunk.com/en/appdynamics-saas/end-user-monitoring/25.7.0/end-user-monitoring/browser-monitoring/browser-real-user-monitoring/overview-of-the-controller-ui-for-browser-rum/configure-the-controller-ui-for-browser-rum)を参照してください。

![IPAddress Config](images/02-brum-ipaddress.png)
