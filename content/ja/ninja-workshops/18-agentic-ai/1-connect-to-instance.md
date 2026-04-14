---
title: EC2 インスタンスへの接続
linkTitle: 1. EC2 インスタンスへの接続
weight: 1
time: 5 minutes
---

## EC2 インスタンスへの接続

各参加者用に AWS/EC2 に Ubuntu Linux インスタンスを用意しています。

インストラクターから提供された IP アドレスとパスワードを使用して、以下のいずれかの方法で EC2 インスタンスに接続してください

* Mac OS / Linux
  * ssh splunk@IP address
* Windows 10+
  * OpenSSH クライアントを使用してください
* 以前のバージョンの Windows
  * Putty を使用してください

## インスタンス名の取得

ssh で EC2 インスタンスにログインしたら、以下のコマンドを使用してインスタンス名を取得してください

```bash
echo $INSTANCE
```

このインスタンス名はあなた固有のものであり、ワークショップの後半で Splunk Observability Cloud でデータを検索する際に使用するため、メモしておいてください。
