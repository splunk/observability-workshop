---
title: サンプルアプリケーションのビルド
linkTitle: 1. サンプルアプリケーションのビルド
weight: 1
time: 10 minutes
---

## はじめに

このワークショップでは、マイクロサービスベースのアプリケーションを使用します。このアプリケーションはオンライン小売業者向けのもので、通常は12以上のサービスが含まれています。ただし、ワークショップをシンプルにするために、小売業者が決済処理ワークフローの一部として使用している2つのサービスに焦点を当てます。credit check サービスと credit processor サービスです。

## 前提条件

EC2 インスタンスから開始し、以下の状態にするためにいくつかの[初期ステップ](#初期ステップ)を実行します。

* **Splunk distribution of the OpenTelemetry Collector** をデプロイする
* `creditcheckservice` と `creditprocessorservice` をビルドしてデプロイする
* サービスにトラフィックを送信するロードジェネレーターをデプロイする

## 初期ステップ

初期セットアップは、EC2 インスタンスのコマンドラインで以下のステップを実行することで完了できます。

``` bash
cd workshop/tagging
./0-deploy-collector-with-services.sh
```

{{% notice title="Java" style="info" %}}
`creditcheckservice` には複数の言語による実装が用意されています。

```bash
./0-deploy-collector-with-services.sh java
```

を実行すると、Python の代わりに Java を選択できます。
{{% /notice %}}

## Splunk Observability Cloud でアプリケーションを確認する

セットアップが完了したので、**Splunk Observability Cloud** にデータが送信されていることを確認しましょう。アプリケーションを初めてデプロイした場合、データが表示されるまで数分かかることがあります。

APM に移動し、Environment ドロップダウンを使用して環境を選択します（例: `tagging-workshop-instancename`）。

すべてが正しくデプロイされていれば、サービスの一覧に `creditprocessorservice` と `creditcheckservice` が表示されるはずです。

![APM Overview](../images/apm_overview.png)

右側の **Service Map** をクリックして、サービスマップを表示します。`creditcheckservice` が `creditprocessorservice` を呼び出しており、平均応答時間が少なくとも3秒であることがわかります。

![Service Map](../images/service_map.png)

次に、右側の **Traces** をクリックして、このアプリケーションでキャプチャされたトレースを確認します。比較的高速に完了するトレース（数ミリ秒程度）もあれば、数秒かかるトレースもあることがわかります。

![Traces](../images/traces.png)

**Errors only** を `on` に切り替えると、エラーが発生しているトレースがあることにも気づくでしょう。

![Traces](../images/traces_with_errors.png)

**Errors only** を `off` に戻し、トレースを duration でソートしてから、実行時間の長いトレースの1つをクリックします。この例では、トレースに5秒かかっており、そのほとんどの時間が `creditprocessorservice` の一部である `/runCreditCheck` オペレーションの呼び出しに費やされていることがわかります。

![Long Running Trace](../images/long_running_trace.png)

現在のところ、一部のリクエストが数ミリ秒で完了し、他のリクエストが数秒かかる理由を理解するのに十分な詳細がトレースにありません。最高のカスタマーエクスペリエンスを提供するためには、この原因を理解することが非常に重要です。

また、一部のリクエストがエラーになり、他のリクエストがエラーにならない理由を理解するのに十分な情報もありません。たとえば、エラートレースの1つを見ると、`creditprocessorservice` が `otherservice` という別のサービスを呼び出そうとした際にエラーが発生していることがわかります。しかし、なぜ一部のリクエストは `otherservice` を呼び出し、他のリクエストは呼び出さないのでしょうか？

![Trace with Errors](../images/error_trace.png)

これらの疑問やその他の内容について、ワークショップで詳しく見ていきます。
