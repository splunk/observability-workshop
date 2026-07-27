---
title: EC2 インスタンスへの接続
linkTitle: 1. EC2 インスタンスへの接続
weight: 1
time: 5 minutes
---

## EC2 インスタンスに接続する

各参加者用にAWS/EC2でUbuntu Linuxインスタンスを準備しています。インストラクターから提供されたIPアドレスとパスワードを使用して、以下のいずれかの方法でEC2インスタンスに接続してください：

* macOS / Linux
  * `ssh splunk@IP address`
* Windows 10+
  * OpenSSHクライアントを使用
* Windowsの以前のバージョン
  * Puttyを使用

## ファイルの編集

ワークショップでは `vi` を使用してファイルを編集します。簡単な使い方を説明します。

ファイルを編集用に開くには：

```bash
vi <filename>
```

* ファイルを編集するには、`i` を押して **Insert mode** に切り替え、通常通りテキストを入力します。`Esc` を押すと **Command mode** に戻ります。
* エディタを終了せずに変更を保存するには、`Esc` を押してコマンドモードに戻り、`:w` と入力します。
* 変更を保存せずにエディタを終了するには、`Esc` を押してコマンドモードに戻り、`:q!` と入力します。
* 変更を保存してエディタを終了するには、`Esc` を押してコマンドモードに戻り、`:wq` と入力します。

`vi` の包括的な説明については [**An introduction to the vi editor**](https://www.redhat.com/en/blog/introduction-vi-editor) を参照してください。

別のエディタを使用したい場合は、代わりに `nano` を使用できます：

```bash
nano <filename>
```
