---
title: OpenTelemetry Collector Development
linkTitle: 8.1 Project Setup
weight: 9
---

## プロジェクトのセットアップ {{% badge style=primary icon=star %}}**Ninja**{{% /badge %}}

{{% notice style="note" %}}

このセクションの所要時間は経験によって異なります。

行き詰まった場合やインストラクターと一緒に進めたい場合は、[**こちら**](https://github.com/splunk/collector-workshop-example)に完全なソリューションがあります。

{{% /notice %}}

新しい _Jenkins CI_ Receiverの開発を始めるには、まずGolangプロジェクトをセットアップする必要があります。
新しいGolangプロジェクトを作成する手順は以下の通りです。

1. `${HOME}/go/src/jenkinscireceiver` という名前の新しいディレクトリを作成し、そのディレクトリに移動します
    1. 実際のディレクトリ名や場所に厳密な決まりはありません。任意の開発ディレクトリを選択できます。
1. `go mod init splunk.conf/workshop/example/jenkinscireceiver` を実行してGolangモジュールを初期化します
    1. これにより、直接的および間接的な依存関係を追跡するための `go.mod` ファイルが作成されます
    1. 最終的に、インポートされる依存関係のチェックサム値である `go.sum` も作成されます。

{{% expand title="{{% badge icon=check color=green title=**Check-in** %}}go.modを確認{{% /badge %}}" %}}

``` text
module splunk.conf/workshop/example/jenkinscireceiver

go 1.20
```

{{% /expand %}}
