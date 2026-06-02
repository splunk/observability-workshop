---
title: EC2 インスタンスへの接続
linkTitle: 1. EC2 インスタンスへの接続
weight: 1
time: 5 minutes
---

## EC2 インスタンスへの接続

参加者ごとに AWS/EC2 上に Ubuntu Linux インスタンスを用意しています。

* お住まいのリージョンのリンクをクリックして **Splunk Show** イベントにアクセスします
* 右上の **Enroll** をクリックします
* ページ下部付近にある EC2 インスタンスの詳細を確認します

以下のような接続情報が表示されます。

![Connection Information](../images/ConnectionInformation.png)

**Connection Information** に記載されている **SSH Command** に含まれる IP アドレスと **SSH Password** を使用して、以下のいずれかの方法で EC2 インスタンスに接続します。

* Mac OS / Linux
  * ssh splunk@IP address
* Windows 10+
  * OpenSSH クライアントを使用します
* それ以前のバージョンの Windows
  * Putty を使用します

{{% notice title="注意: 接続を続行するか尋ねられたら 'yes' と答えてください" style="primary" icon="running" %}}

![SSH Connection](../images/ssh-connection.png)

{{% / notice %}}

{{% notice title="VPN 接続について" style="green" icon="running" %}}

オフィスから作業していて接続に問題がある場合は、まず社内 VPN に接続してみてください。

{{% /notice %}}

## インスタンス名の取得

ssh で EC2 インスタンスにログインしたら、以下のコマンドを使用してインスタンス名を取得します。

```bash
echo $INSTANCE
```

このインスタンス名はあなた専用のもので、ワークショップの後半で Splunk Observability Cloud 内のデータを検索する際に使用するため、メモしておいてください。

## Visual Studio Code への接続（オプション）

ワークショップを通じていくつかのファイルを編集します。ワークショップの手順では `vi` エディタを使用するためのヒントが記載されており、`nano` エディタも使用できます。

本格的な IDE を使いたい場合は、ローカルマシンで動作している Visual Studio Code を EC2 インスタンス上のリモートファイル編集に使用できます。

その大まかな手順は以下のとおりです。

1. [このリンク](https://code.visualstudio.com/download) からマシンに VS Code をダウンロードしてインストールします。
2. VS Code で **Settings** を開き、**Extensions** に移動します。
3. **Remote – SSH extension**（Microsoft 製）を検索してインストールします。

![Install Remote SSH Extension](../images/InstallRemoteSSH.png)

1. F1 キー（Windows では Ctrl+Shift+P、Mac OS では Cmd+Shift+P）を押します。
2. **Remote-SSH: Connect to Host** を実行します。
3. Splunk Show から SSH コマンドをコピーします: `ssh -p 2222 splunk@EC2_PUBLIC_IP`。
4. プロンプトが表示されたら、デフォルトの SSH 設定ファイルを選択します。
5. もう一度 F1 キー（Windows では Ctrl+Shift+P、Mac OS では Cmd+Shift+P）を押します。
6. **Remote-SSH: Connect to Host** を実行します。
7. 先ほど追加したホストを選択します。VS Code が新しいウィンドウを開き、接続を開始します。
8. VS Code の上部に **SSH password** を求めるプロンプトが表示されます。Splunk Show からパスワードをコピーしてここに入力します。
9. **Open Folder** をクリックし、フォルダ名として `/home/splunk` を入力します。

![Open Remote Folder](../images/OpenRemoteFolder.png)

これで VS Code を使ってリモートでファイルを編集できるようになりました。
