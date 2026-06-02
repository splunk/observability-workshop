---
title: Demo-in-a-Box の実行
weight: 3
description: Demo-in-a-Box を使用して、単一の Web UI からデモと OpenTelemetry Collector を管理できます。
draft: true
---

**Demo-in-a-box** は、Web インターフェースを使用してデモアプリを簡単に実行する方法です。

以下の機能を提供します。

* デモアプリと状態を素早くデプロイする方法
* OpenTelemetry Collector の構成を簡単に変更し、ログを確認する方法
* Pod のステータスや Pod のログなどを取得する機能

multipass を使用してローカルで利用するには、以下の手順を実行します。

* [local hosting for multipass](../multipass) の手順に従ってください
  * `terraform.tfvars` ファイルで `splunk_diab` を `true` に設定し、**すべての**他のオプションが `false` に設定されていることを確認します
  * 次に、必要かつ重要な他のトークン/URL を設定します
  * その後、terraform の手順を実行します
* インスタンスが起動したら、ブラウザで `http://<IP>:8083` にアクセスします
  * `terraform.tfvars` ファイルの `wsversion` は、デフォルトでワークショップの現行バージョン（例: `4.64`）に設定されています。
    * 最新の開発版を使用するには、`wsversion` を `main` に変更します
    * 維持されているワークショップは、開発版（`main`）、現行版（例: `4.64`）、および前バージョン（例: `4.63`）の 3 つのみです
    * 変更後、`terraform apply` を実行して変更を適用します
* これで、任意のデモをデプロイできます。デプロイの一環として Collector もデプロイされます
