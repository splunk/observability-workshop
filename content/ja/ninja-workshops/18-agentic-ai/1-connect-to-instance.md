---
title: EC2 インスタンスへの接続
linkTitle: 1. EC2 インスタンスへの接続
weight: 1
time: 5 minutes
---

## EC2 インスタンスに接続する

各参加者用に AWS/EC2 上に Ubuntu Linux インスタンスを用意しています:

* お住まいのリージョンのリンクをクリックして **Splunk Show** イベントにアクセスします
* 右上の **Enroll** をクリックします
* ページ下部付近で EC2 インスタンスの詳細を確認します

以下のような接続情報が表示されます:

![Connection Information](../images/ConnectionInformation.png)

**Connection Information** に記載されている IP アドレス（**SSH Command** の一部）と **SSH Password** を使用して、以下のいずれかの方法で EC2 インスタンスに接続します:

* Mac OS / Linux
  * ssh splunk@IP address
* Windows 10+
  * OpenSSH クライアントを使用します
* それ以前のバージョンの Windows
  * Putty を使用します

{{% notice title="VPN 接続" style="green" icon="running" %}}

オフィスから作業していて接続に問題がある場合は、まず企業 VPN に接続してみてください。

{{% /notice %}}

## インスタンス名の取得

SSH で EC2 インスタンスにログインしたら、以下のコマンドでインスタンス名を取得します:

```bash
echo $INSTANCE
```

この名前をメモしておいてください。インスタンス名はあなた固有のもので、ワークショップの後半で Splunk Observability Cloud 上のデータを検索する際に使用します。

## Visual Studio Code の接続（オプション）

このワークショップでは複数のファイルを編集します。ワークショップの手順には `vi` エディタを使用するためのヒントが含まれており、参加者は `nano` エディタも使用できます。

本格的な IDE を使用したい場合は、ノート PC 上の Visual Studio Code から EC2 インスタンス上のリモートファイルを編集できます。

手順の概要は以下のとおりです:

1. [このリンク](https://code.visualstudio.com/download)から VS Code をダウンロードしてインストールします。
2. VS Code で **Settings** に移動し、**Extensions** を開きます。
3. **Remote – SSH extension**（Microsoft 製）を検索してインストールします。

![Install Remote SSH Extension](../images/InstallRemoteSSH.png)

4. F1 キー（Windows では Ctrl+Shift+P / Mac OS では Cmd+Shift+P）を押します。
5. **Remote-SSH: Connect to Host** を実行します。
6. Splunk Show から SSH コマンドをコピーします: `ssh -p 2222 splunk@EC2_PUBLIC_IP`
7. プロンプトが表示されたら、デフォルトの SSH 設定ファイルを選択します。
8. 再度 F1 キー（Windows では Ctrl+Shift+P / Mac OS では Cmd+Shift+P）を押します。
9. **Remote-SSH: Connect to Host** を実行します。
10. 先ほど追加したホストを選択します。VS Code が新しいウィンドウを開き、接続を開始します。
11. VS Code の上部に **SSH password** の入力を求めるプロンプトが表示されます。Splunk Show からパスワードをコピーして入力します。
12. **Open Folder** をクリックし、フォルダ名として `/home/splunk` を入力します:

![Open Remote Folder](../images/OpenRemoteFolder.png)

これで VS Code を使用してリモートでファイルを編集できます！
