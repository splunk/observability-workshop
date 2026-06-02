---
title: OpenTelemetry Collector Development
linkTitle: 8.1 Project Setup
weight: 9
---

## Project Setup {{% badge style=primary icon=user-ninja %}}**Ninja**{{% /badge %}}

{{% notice style="note" %}}

このセクションを完了するまでにかかる時間は、経験により異なります。

詰まったときやインストラクターと一緒に進めたい場合は、完成版のソリューションを[**こちら**](https://github.com/splunk/collector-workshop-example)で確認できます。

{{% /notice %}}

新しい _Jenkins CI_ receiver の開発を始めるために、まずは Golang プロジェクトをセットアップする必要があります。
新しい Golang プロジェクトを作成する手順は以下のとおりです。

1. `${HOME}/go/src/jenkinscireceiver` という名前の新しいディレクトリを作成し、そこに移動します
    1. 実際のディレクトリ名や場所に厳密な決まりはなく、ご自身の開発ディレクトリを自由に選んで作成して構いません。
1. `go mod init splunk.conf/workshop/example/jenkinscireceiver` を実行して golang モジュールを初期化します
    1. これにより `go.mod` というファイルが作成され、直接および間接の依存関係を追跡するために使用されます
    1. 最終的には `go.sum` も作成され、これはインポートされる依存関係のチェックサム値を保持します。

{{% expand title="{{% badge icon=check color=green title=**Check-in** %}}Review your go.mod{{% /badge %}}" %}}

``` text
module splunk.conf/workshop/example/jenkinscireceiver

go 1.20
```

{{% /expand %}}
