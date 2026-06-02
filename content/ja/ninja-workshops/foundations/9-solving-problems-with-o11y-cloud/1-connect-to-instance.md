---
title: EC2 インスタンスへの接続
linkTitle: 1. EC2 インスタンスへの接続
weight: 1
time: 5 minutes
---

## EC2 インスタンスへの接続

参加者ごとに AWS/EC2 上に Ubuntu Linux インスタンスを用意しています。講師から提供される IP アドレスとパスワードを使用して、以下のいずれかの方法で EC2 インスタンスに接続してください。

* macOS / Linux
  * `ssh splunk@IP address`
* Windows 10 以降
  * OpenSSH クライアントを使用してください
* それ以前のバージョンの Windows
  * Putty を使用してください

## ファイルの編集

ワークショップでは `vi` を使用してファイルを編集します。簡単な使い方を以下に示します。

ファイルを編集用に開くには：

```bash
vi <filename> 
```

* ファイルを編集するには、`i` を押して **Insert モード** に切り替え、通常通りテキストを入力します。`Esc` で **Command モード** に戻ります。
* エディタを終了せずに変更を保存するには、`Esc` を押してコマンドモードに戻り、`:w` を入力します。
* 変更を保存せずにエディタを終了するには、`Esc` を押してコマンドモードに戻り、`:q!` を入力します。
* 変更を保存してエディタを終了するには、`Esc` を押してコマンドモードに戻り、`:wq` を入力します。

`vi` の詳しい使い方については [**An introduction to the vi editor**](https://www.redhat.com/en/blog/introduction-vi-editor) を参照してください。

別のエディタを使用したい場合は、代わりに `nano` を使用することもできます：

```bash
nano <filename> 
```
