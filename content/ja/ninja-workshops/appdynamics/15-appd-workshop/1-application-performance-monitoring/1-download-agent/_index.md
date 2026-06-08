---
title: 1. Download Java Agent
weight: 1
description: この演習では、Web ブラウザから AppDynamics Controller にアクセスし、Java APM エージェントをダウンロードします。
---
この演習では、Web ブラウザから AppDynamics Controller にアクセスし、Java APM エージェントをダウンロードします。

## Controller へのログイン

Cisco の認証情報を使用して [AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) にログインします。

## アプリケーションの設定

1. 左側のナビゲーションパネルで **Overview** を選択します
2. **Getting Started** タブをクリックします
3. **Getting Started Wizard** ボタンをクリックします

![Getting Started Wizard](images/agent-wizard-rz.png)

Java アプリケーションタイプを選択します
  
![Java Application](images/select-java-rz.png)

## Java エージェントのダウンロード

1. JVM タイプとして **Sun/JRockit - Legacy** を選択します
2. Controller 接続のデフォルト設定をそのまま使用します
3. **Set Application and Tier** の下で、**Create a new Application:** を選択します
4. アプリケーション名として **Supercar-Trader-YOURINITIALS** を入力します
5. 新しい Tier に **Web Portal** を入力します
6. Node Name に **Web-Portal_Node-01** を入力します
7. **Continue** をクリックします
8. **Click Here to Download** をクリックします

{{% notice title="Warning" style="primary"  icon="lightbulb" %}}
アプリケーション名は一意である必要があります。アプリケーション名にイニシャルまたは一意の識別子を追加してください。
{{% /notice %}}

![Agent Configuration1](images/java-agent-config1-rz.png)

![Agent Configuration2](images/java-agent-config2-rz.png)

ブラウザにエージェントがローカルファイルシステムにダウンロードされていることを示すプロンプトが表示されます。ファイルがダウンロードされた場所とファイルの完全な名前を必ずメモしてください。

![Agent Bundle](images/agent-bundle-rz.png)
