---
title: 1. Java Agentのダウンロード
weight: 1
description: この演習では、WebブラウザからAppDynamics Controllerにアクセスし、Java APM Agentをダウンロードします。
---
この演習では、WebブラウザからAppDynamics Controllerにアクセスし、Java APM Agentをダウンロードします。

## Controllerへのログイン

Ciscoの認証情報を使用して [AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) にログインします。

## アプリケーションの設定

1. 左側のナビゲーションパネルで **Overview** を選択します
2. **Getting Started** タブをクリックします
3. **Getting Started Wizard** ボタンをクリックします

![Getting Started Wizard](images/agent-wizard-rz.png)

Java Application Typeを選択します
  
![Java Application](images/select-java-rz.png)

## Java Agentのダウンロード

1. JVMタイプとして **Sun/JRockit - Legacy** を選択します
2. Controller接続のデフォルト値をそのまま使用します
3. **Set Application and Tier** で **Create a new Application:** を選択します
4. アプリケーション名として **Supercar-Trader-YOURINITIALS** を入力します
5. 新しいTierとして **Web Portal** を入力します
6. Node Nameとして **Web-Portal_Node-01** を入力します
7. **Continue** をクリックします
8. **Click Here to Download** をクリックします

{{% notice title="注意" style="primary"  icon="lightbulb" %}}
アプリケーション名は一意である必要があります。アプリケーション名にイニシャルまたは一意の識別子を追加してください。
{{% /notice %}}

![Agent Configuration1](images/java-agent-config1-rz.png)

![Agent Configuration2](images/java-agent-config2-rz.png)

ブラウザにAgentがローカルファイルシステムにダウンロードされていることを示すプロンプトが表示されます。ファイルのダウンロード先とファイル名を確認してください。

![Agent Bundle](images/agent-bundle-rz.png)
