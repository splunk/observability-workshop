---
title: EC2インスタンスへの接続
linkTitle: 1. EC2インスタンスへの接続
weight: 1
time: 5 minutes
---

## EC2インスタンスに接続する

各参加者用にAWS/EC2上にUbuntu Linuxインスタンスを用意しています。

* お住まいのリージョンのリンクをクリックして **Splunk Show** イベントにアクセスします
* 右上の **Enroll** をクリックします
* ページ下部付近でEC2インスタンスの詳細を確認します

以下のような接続情報が表示されます。

![Connection Information](../images/ConnectionInformation.png)

**Connection Information** に含まれるIPアドレス（**SSH Command** の一部）と **SSH Password** を使用して、以下のいずれかの方法でEC2インスタンスに接続します。

* Mac OS / Linux
  * ssh splunk@IPアドレス
* Windows 10+
  * OpenSSHクライアントを使用します
* それ以前のバージョンのWindows
  * Puttyを使用します

{{% notice title="注意: 接続を続行するか聞かれたら「yes」と入力してください" style="primary" icon="running" %}}

![SSH Connection](../images/ssh-connection.png)

{{% / notice %}}

{{% notice title="VPN接続" style="green" icon="running" %}}

オフィスから作業していて接続に問題がある場合は、まず企業VPNに接続してみてください。

{{% /notice %}}

## インスタンス名の取得

SSHでEC2インスタンスにログインしたら、以下のコマンドを使用してインスタンス名を取得します。

```bash
echo $INSTANCE
```

このインスタンス名はあなた固有のもので、後のワークショップでSplunk Observability Cloudからデータを見つける際に使用するため、メモしておいてください。

## Visual Studio Codeの接続（オプション）

このワークショップでは複数のファイルを編集します。ワークショップの手順には `vi` エディタを使用するヒントが含まれていますが、参加者は `nano` エディタも使用できます。

本格的なIDEを使用したい場合は、ラップトップで実行しているVisual Studio CodeをEC2インスタンスに接続してリモートファイルを編集できます。

手順の概要は以下のとおりです。

1. [こちらのリンク](https://code.visualstudio.com/download)からVS Codeをダウンロードしてインストールします。
2. VS Codeで **Settings** に移動し、**Extensions** を開きます。
3. **Remote – SSH extension**（Microsoft製）を検索してインストールします。

    ![Install Remote SSH Extension](../images/InstallRemoteSSH.png)

4. F1キー（WindowsではCtrl+Shift+P / Mac OSではCmd+Shift+P）を押します。
5. **Remote-SSH: Connect to Host** を実行します。
6. Splunk ShowからSSHコマンドをコピーします: `ssh -p 2222 splunk@EC2_PUBLIC_IP`
7. プロンプトが表示されたら、デフォルトのSSH設定ファイルを選択します。
8. 再度F1キー（WindowsではCtrl+Shift+P / Mac OSではCmd+Shift+P）を押します。
9. **Remote-SSH: Connect to Host** を実行します。
10. 追加したホストを選択します。VS Codeが新しいウィンドウを開き、接続を開始します。
11. VS Codeの上部に **SSH password** の入力を求めるプロンプトが表示されます。Splunk Showからパスワードをコピーして入力します。
12. **Open Folder** をクリックし、フォルダ名として `/home/splunk` を入力します。

![Open Remote Folder](../images/OpenRemoteFolder.png)

これでVS Codeを使用してリモートファイルを編集できます。
