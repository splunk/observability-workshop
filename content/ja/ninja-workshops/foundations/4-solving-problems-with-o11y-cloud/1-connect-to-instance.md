---
title: EC2インスタンスへの接続
linkTitle: 1. EC2インスタンスへの接続
weight: 1
time: 5 minutes
---

## EC2インスタンスに接続する

各参加者用にAWS/EC2でUbuntu Linuxインスタンスを用意しています。インストラクターから提供されたIPアドレスとパスワードを使用して、以下のいずれかの方法でEC2インスタンスに接続します。

* macOS / Linux
  * `ssh splunk@IP address`
* Windows 10+
  * OpenSSHクライアントを使用します
* それ以前のバージョンのWindows
  * Puttyを使用します

## ファイルの編集

ワークショップではファイルの編集に `vi` を使用します。以下に簡単な使い方を紹介します。

ファイルを開いて編集するには次のコマンドを実行します。

```bash
vi <filename> 
```

* ファイルを編集するには、`i` を押して **Insert mode** に切り替え、通常どおりテキストを入力します。`Esc` を押すと **Command mode** に戻ります。
* エディタを終了せずに変更を保存するには、`Esc` を押してコマンドモードに戻り、`:w` を入力します。
* 変更を保存せずにエディタを終了するには、`Esc` を押してコマンドモードに戻り、`:q!` を入力します。
* 変更を保存してエディタを終了するには、`Esc` を押してコマンドモードに戻り、`:wq` を入力します。

`vi` の包括的な入門については [**An introduction to the vi editor**](https://www.redhat.com/en/blog/introduction-vi-editor) を参照してください。

別のエディタを使用したい場合は、代わりに `nano` を使用できます。

```bash
nano <filename> 
```
