---
title: EC2 インスタンスへの接続
linkTitle: 1. EC2 インスタンスへの接続
weight: 1
time: 5 minutes
---

## EC2 インスタンスに接続する

各参加者用に AWS/EC2 に Ubuntu Linux インスタンスを用意しています:

* お住まいのリージョンのリンクをクリックして **Splunk Show** イベントにアクセスします
* 右上の **Enroll** をクリックします
* ページの下部付近で EC2 インスタンスの詳細を確認します

以下のような接続情報が表示されます:

![Connection Information](../images/ConnectionInformation.png)

**Connection Information** に含まれる IP アドレス（**SSH Command** の一部）と **SSH Password** を使用して、以下のいずれかの方法で EC2 インスタンスに接続します:

* Mac OS / Linux
  * ssh splunk@IP address
* Windows 10+
  * OpenSSH クライアントを使用します
* それ以前のバージョンの Windows
  * Putty を使用します

{{% notice title="注意: 接続を続行するか聞かれたら「yes」と回答してください" style="primary" icon="running" %}}

![SSH Connection](../images/ssh-connection.png)

{{% / notice %}}

{{% notice title="VPN 接続" style="green" icon="running" %}}

オフィスから作業していて接続に問題がある場合は、まず企業 VPN に接続してみてください。

{{% /notice %}}

## インスタンス名の取得

SSH で EC2 インスタンスにログインしたら、以下のコマンドでインスタンス名を取得します:

```bash
echo $INSTANCE
```

このインスタンス名はあなた固有のもので、ワークショップの後半で Splunk Observability Cloud にてデータを検索する際に使用しますので、メモしておいてください。

## Visual Studio Code の接続（オプション）

このワークショップでは複数のファイルを編集します。ワークショップの手順には `vi` エディターを使用するヒントが含まれていますが、参加者は `nano` エディターも使用できます。

本格的な IDE を使用したい場合は、ラップトップで実行している Visual Studio Code を接続して、EC2 インスタンス上のリモートファイルを編集できます。

手順の概要は以下のとおりです:

1. [このリンク](https://code.visualstudio.com/download)を使用して、マシンに VS Code をダウンロードしてインストールします。
2. VS Code で **Settings**、次に **Extensions** に移動します。
3. **Remote – SSH extension**（Microsoft 製）を検索してインストールします。

![Install Remote SSH Extension](../images/InstallRemoteSSH.png)

4. F1 キー（Windows では Ctrl+Shift+P / Mac OS では Cmd+Shift+P）を押します。
5. **Remote-SSH: Connect to Host** を実行します。
6. Splunk Show から SSH コマンドをコピーします: `ssh -p 2222 splunk@EC2_PUBLIC_IP`
7. プロンプトが表示されたら、デフォルトの SSH 設定ファイルを選択します。
8. もう一度 F1 キー（Windows では Ctrl+Shift+P / Mac OS では Cmd+Shift+P）を押します。
9. **Remote-SSH: Connect to Host** を実行します。
10. 先ほど追加したホストを選択します。VS Code が新しいウィンドウを開き、接続を開始します。
11. VS Code の上部に **SSH password** を求めるプロンプトが表示されます。Splunk Show からパスワードをコピーして入力します。
12. **Open Folder** をクリックし、フォルダー名として `/home/splunk` を入力します:

![Open Remote Folder](../images/OpenRemoteFolder.png)

これで VS Code を使用してリモートファイルを編集できます！
