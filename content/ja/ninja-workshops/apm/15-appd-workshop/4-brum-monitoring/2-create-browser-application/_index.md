---
title: ブラウザアプリケーションの作成
time: 2 minutes
weight: 2
description: この演習では、Controller でアプリケーションを作成および構成します。
---

この演習では、以下のタスクを完了します。

* Web ブラウザから AppDynamics Controller にアクセスします。
* Controller でブラウザアプリケーションを作成します。
* ブラウザアプリケーションを構成します。

## Controller へのログイン

[AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) に Cisco の認証情報を使用してログインします。

## Controller でのブラウザアプリケーションの作成

以下の手順で新しいブラウザアプリケーションを作成します。

{{% notice title="Note" style="primary"  %}}
下記のステップ 5 でブラウザアプリケーションに一意の名前を付けることが**非常に重要**です。
{{% /notice %}}

1. トップメニューの **User Experience** タブをクリックします。
2. **User Experience** の下にある **Browser Apps** オプションをクリックします。
3. **Add App** をクリックします。
4. **Create an Application manually** オプションを選択します。
5. ブラウザアプリケーションの一意の名前を _Supercar-Trader-Web-<your\_initials\_or\_name>-<four\_random\_numbers>_ の形式で入力します。
    * 例 1: Supercar-Trader-Web-JFK-3179
    * 例 2: Supercar-Trader-Web-JohnSmith-0953
6. **OK** をクリックします。

![Create App](images/02-brum-create-app.png)

これで **Supercar-Trader-Web-##-####** アプリケーションの **Browser App Dashboard** が表示されるはずです。

1. 左メニューの **Configuration** タブをクリックします。
2. **Instrumentation** オプションをクリックします。

![Instrumentation](images/02-brum-instrument.png)

以下の手順に従って、ブラウザモニタリングエージェントが取得したデータと一緒に IP アドレスを保存するようにデフォルトの構成を変更します。

1. **Settings** タブをクリックします。
2. 右側のスクロールバーを使用して画面の一番下までスクロールします。
3. **Store IP Address** チェックボックスをオンにします。
4. **Save** をクリックします。

Browser RUM 用の Controller UI の構成について詳しくは、[こちら](https://help.splunk.com/en/appdynamics-saas/end-user-monitoring/25.7.0/end-user-monitoring/browser-monitoring/browser-real-user-monitoring/overview-of-the-controller-ui-for-browser-rum/configure-the-controller-ui-for-browser-rum) を参照してください。

![IPAddress Config](images/02-brum-ipaddress.png)
