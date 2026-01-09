---
title: ブラウザアプリケーションの作成
time: 2 minutes
weight: 2
description: この演習では、Controllerでアプリケーションを作成および設定します。
---

この演習では、以下のタスクを完了します：

*   WebブラウザからAppDynamics Controllerにアクセスする。
*   ControllerでBrowser Applicationを作成する。
*   Browser Applicationを設定する。

## Controllerへのログイン

Ciscoの認証情報を使用して[AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/)にログインします。

## ControllerでのBrowser Applicationの作成

以下の手順に従って、新しいブラウザアプリケーションを作成します。

{{% notice title="Note" style="primary"  %}}
下記のステップ5で、ブラウザアプリケーションに一意の名前を作成することが**非常に重要**です。
{{% /notice %}}

1. トップメニューの **User Experience** タブをクリックします。
2. **User Experience** の下にある **Browser Apps** オプションをクリックします。
3. **Add App** をクリックします。
4. **Create an Application manually** オプションを選択します。
5. _Supercar-Trader-Web-<your\_initials\_or\_name>-<four\_random\_numbers>_ の形式でブラウザアプリケーションの一意の名前を入力します。
    * 例1: Supercar-Trader-Web-JFK-3179
    * 例2: Supercar-Trader-Web-JohnSmith-0953
6. **OK** をクリックします。

![Create App](images/02-brum-create-app.png)

これで **Supercar-Trader-Web-##-####** アプリケーションの **Browser App Dashboard** が表示されるはずです。

1. 左メニューの **Configuration** タブをクリックします。
2. **Instrumentation** オプションをクリックします。

![Instrumentation](images/02-brum-instrument.png)

以下の手順に従って、ブラウザ監視エージェントによってキャプチャされるデータと一緒にIPアドレスが保存されるようにデフォルト設定を変更します。

3. **Settings** タブをクリックします。
4. 右側のスクロールバーを使用して画面の下部までスクロールします。
5. **Store IP Address** チェックボックスをオンにします。
6. **Save** をクリックします。

Browser RUM用のController UIの設定について詳しくは、[こちら](https://help.splunk.com/en/appdynamics-saas/end-user-monitoring/25.7.0/end-user-monitoring/browser-monitoring/browser-real-user-monitoring/overview-of-the-controller-ui-for-browser-rum/configure-the-controller-ui-for-browser-rum)をご覧ください。

![IPAddress Config](images/02-brum-ipaddress.png)
