---
title: OpenTelemetry Collector 開発
linkTitle: 8.1 Project Setup
weight: 9
---

## プロジェクトのセットアップ {{% badge style=primary icon=user-ninja %}}**Ninja**{{% /badge %}}

{{% notice style="note" %}}

このワークショップセクションを完了するまでの時間は、経験によって異なります。

行き詰まった場合やインストラクターに沿って進めたい場合は、[**こちら**](https://github.com/splunk/collector-workshop-example)に完全なソリューションがあります。

{{% /notice %}}

新しい _Jenkins CI_ レシーバーの開発を始めるには、まず Golang プロジェクトをセットアップする必要があります。
新しい Golang プロジェクトを作成する手順は以下の通りです

1. `${HOME}/go/src/jenkinscireceiver` という名前の新しいディレクトリを作成し、そのディレクトリに移動します
    1. 実際のディレクトリ名や場所は厳密ではなく、独自の開発ディレクトリを選択して作成できます。
1. `go mod init splunk.conf/workshop/example/jenkinscireceiver` を実行して golang モジュールを初期化します
    1. これにより `go.mod` というファイルが作成され、直接的および間接的な依存関係を追跡するために使用されます
    1. 最終的には、インポートされる依存関係のチェックサム値である `go.sum` が生成されます。

{{% expand title="{{% badge icon=check color=green title=**Check-in** %}}go.mod を確認する{{% /badge %}}" %}}

``` text
module splunk.conf/workshop/example/jenkinscireceiver

go 1.20
```

{{% /expand %}}
