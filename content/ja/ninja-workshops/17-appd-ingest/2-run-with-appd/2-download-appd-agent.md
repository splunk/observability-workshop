---
title: 2. AppD Agent のダウンロード
weight: 2
---

デュアルシグナルモードを使用するには、AppDynamics Java Agent（バージョン25.6.0以上）が必要です。AppDynamics ControllerのGetting Started Wizardからダウンロードします。

## AppDynamics Controller へのログイン

ブラウザで [AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) を開き、Ciscoの認証情報でログインします。

## Getting Started Wizard の起動

1. 左側のナビゲーションパネルで **Overview** を選択します
2. **Getting Started** タブをクリックします
3. [**Getting Started Wizard**](https://se-lab.saas.appdynamics.com/controller/#/location=GETTING_STARTED_JAVA&timeRange=last_15_minutes.BEFORE_NOW.-1.-1.15) ボタンをクリックします

## アプリケーションの設定

1. Application Typeとして **Java** を選択します
2. JVM typeとして **JDK8+** を選択します
3. Controller connectionはデフォルト値のままにします
4. **Set Application and Tier** で以下を設定します:
   - **Application Name**: `Dual-Ingest-<YOURINITIALS>`（一意である必要があります -- あなたのイニシャルを追加してください）
   - **Tier Name**: `OrderService`
   - **Node Name**: `OrderService-Node`
5. **Continue** をクリックします
6. **Click Here to Download** をクリックします

![AppDynamics Agent](../../_images/appd-agent.png?width=30vw)

## Agent を EC2 インスタンスに転送する

AgentのZIPファイルはローカルマシンにダウンロードされます。EC2インスタンスにアップロードします:

{{% notice title="ヒント" style="primary" icon="lightbulb" %}}
ファイル名はダウンロードした正確なバージョンに置き換え、インスタンスのホスト名を使用してください。
{{% /notice %}}

```bash
scp -P 2222 ~/Downloads/AppServerAgent-<your-downloaded-version>.zip splunk@<your-instance>.splunk.show:~/workshop/appd/
```

**例:** `scp -P 2222 ~/Downloads/AppServerAgent-1.8-26.1.0.37621.zip splunk@i-0e279f0be5347a79e.splunk.show:~/workshop/appd/`

## Agent の解凍

インスタンスにSSH接続し、Agentを解凍します:

```bash
cd ~/workshop/appd
mkdir -p agent
unzip AppServerAgent-*.zip -d agent/
```

これでAgent JARが `~/workshop/appd/agent/javaagent.jar` に配置されているはずです。

## Account Access Key をメモする

アプリを実行する際に [**Account Access Key**](https://se-lab.saas.appdynamics.com/controller/#/licensing/license-management-account?timeRange=last_15_minutes.BEFORE_NOW.-1.-1.15) が必要になります。AppDynamics Controllerで確認できます:

1. **Settings**（歯車アイコン）→ **License** に移動します
2. 左側のサイドバーで **Account** をクリックします
2. **Account** の下で、**Name**（`se-lab`）と **Access Key** をメモします

{{% notice title="手元に控えておきましょう" style="primary" icon="lightbulb" %}}
次のステップでAccount NameとAccess KeyをJVMプロパティとして使用します。これらはAgentをControllerに認証するために使用されます。
{{% /notice %}}
