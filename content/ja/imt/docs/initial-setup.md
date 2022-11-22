---
title: ワークショップ環境へのアクセス
linkTitle: AWS/EC2 インスタンスにアクセスする
weight: 2
description: > 
  **5 分**
isCJKLanguage: true
---

1. 各自に割り当てられたAWS/EC2インスタンスのIPアドレスを確認します
2. SSH、Putty[^1]、またはWebブラウザを使ってインスタンスに接続します
3. クラウド上にある AWS/EC2 インスタンスへの接続を確認します

---

## 1. AWS/EC2 の IP アドレス

ワークショップの準備として、Splunk は AWS/EC2 に Ubuntu Linux インスタンスを用意しています。

ワークショップで使用するインスタンスにアクセスするには、ワークショップのリーダーが提供する Google Sheets のURLにアクセスしてください。

AWS/EC2 インスタンスの検索には、本ワークショップの登録時にご記入いただいたお名前（姓名）を入力してください。

![参加者のスプレッドシート](../../images/spreadsheet-info.png)

ワークショップのインスタンスに接続するためのIPアドレス、SSHコマンド（Mac OS、Linux、最新のWindowsバージョン用）、パスワードが表示されています。

また、ssh や putty で接続できない場合に使用するブラウザアクセスのURLも記載されています。「[ブラウザ経由でEC2に接続する](./#4-ブラウザ経由でec2に接続する)」を参照してください。

{{% alert title="Important" color="primary" %}}
可能であれば、SSH または Putty を使用してEC2インスタンスにアクセスしてください。
ワークショップで必要になるので、IPアドレスをメモしておいてください。
{{% /alert %}}

## 2. SSH (Mac OS/Linux)

Mac や Linux の端末から SSH を使ってワークショップに接続することができます。

SSH を使用するには、お使いのシステムでターミナルを開き、`ssh ubuntu@x.x.x.x`と入力してください（x.x.x.xをステップ1で見つけたIPアドレスに置き換えてください）。

![ssh を使ったログイン](../../images/ssh-1.png)

**`Are you sure you want to continue connecting (yes/no/[fingerprint])?`** というプロンプトが表示されたら **`yes`** と入力してください。

![ssh パスワードの入力](../../images/ssh-2.png)

ステップ1の Google Sheets に記載されているパスワードを入力してください。

ログインに成功すると、Splunk のロゴと Linux のプロンプトが表示されます。

![ssh 接続完了](../../images/ssh-3.png)

これで [ワークショップを開始する](../../otel/k3s/) に進む準備が整いました。

---

## 3. Putty (Windows)

ssh がプリインストールされていない場合や、Windows システムを使用している場合、putty がおすすめです。Putty は [こちら](https://www.putty.org/) からダウンロードできます。

{{% alert title="Important" color="primary" %}}
Putty がインストールできない場合は、[ブラウザ経由でEC2に接続する](./#4-ブラウザ経由でec2に接続する)で進めてください。
{{% /alert %}}

Putty を開き、**Host Name (or IP address)** の欄に、Google Sheets に記載されているIPアドレスを入力してください。

名前を入力して **Save** を押すと、設定を保存することができます。

![putty-2](../../images/putty-settings.png)

インスタンスにログインするには、**Open** ボタンをクリックします。

初めて AWS/EC2 ワークショップインスタンスに接続する場合は、セキュリティダイアログが表示されますので、**Yes** をクリックしてください。

![putty-3](../../images/putty-security.png)

接続されたら、**ubuntu** としてログインし、パスワードは Google Sheets に記載されているものを使用します。

接続に成功すると、以下のような画面が表示されます。

![putty-4](../../images/putty-loggedin.png)

これで [ワークショップを開始する](../gdi/k3s/) 準備が整いました。

---

## 4. ブラウザ経由でEC2に接続する

SSH（ポート22） の使用が禁止されている場合や、Putty がインストールできない場合は、Webブラウザを使用してワークショップのインスタンスに接続することができます。

{{% alert title="Note" color="primary" %}}
ここでは、6501番ポートへのアクセスが、ご利用のネットワークのファイアウォールによって制限されていないことを前提としています。
{{% /alert %}}

Webブラウザを開き、**http:/x.x.x.x:6501** （X.X.X.Xは Google Sheetsに記載されたIPアドレス）と入力します。

![http-6501](../../images/shellinabox-url.png)

接続されたら、**ubuntu** としてログインし、パスワードは Google Sheets に記載されているものを使用します。

![http-connect](../../images/shellinabox-connect.png)

接続に成功すると、以下のような画面が表示されます。

![web login](../../images/shellinabox-login.png)

通常のSSHを使用しているときとは異なり、ブラウザセッションを使用しているときは、*コピー＆ペースト* を使うための手順が必要です。これは、クロスブラウザの制限によるものです。

ワークショップで指示をターミナルにコピーするように言われたら、以下のようにしてください。

*通常通り指示をコピーし、ウェブターミナルにペーストする準備ができたら、以下のように **Paste from browser** を選択します*。

![webでのペースト](../../images/shellinabox-paste-browser.png)

すると、ウェブターミナルに貼り付けるテキストを入力するダイアログボックスが表示されます。

![webでのペースト3](../../images/shellinabox-example-1.png)

表示されているテキストボックスにテキストを貼り付け、**OK** を押すと、コピー＆ペーストができます。

{{% alert title="Note" color="primary" %}}
通常のSSH接続とは異なり、Webブラウザには60秒のタイムアウトがあり、接続が解除されると、Webターミナルの中央に **Connect** ボタンが表示されます。

この **Connect** ボタンをクリックするだけで、再接続され、次の操作が可能になります。
{{% /alert %}}

 ![webでの再接続](../../images/shellinabox-reconnect.png)

これで [ワークショップを開始する](../gdi/k3s/) 準備が整いました。

---

## 5. Multipass (全員)

AWSへはアクセスできないが、ローカルにソフトウェアをインストールできる場合は、「[Multipassを使用する](https://github.com/signalfx/observability-workshop/tree/main/multipass)」の手順に従ってください。

[^1]: [Putty のダウンロード](https://www.chiark.greenend.org.uk/~sgtatham/putty/)
