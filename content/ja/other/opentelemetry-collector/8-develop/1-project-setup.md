---
title: OpenTelemetry Collector を開発する
linkTitle: 8.1 セットアップ
weight: 9
---

## プロジェクトのセットアップ {{% badge style=primary icon=user-ninja %}}**Ninja**{{% /badge %}}

{{% notice style="note" %}}

このワークショップのセクションを完了する時間は経験によって異なる場合があります。

完成したものは[こちら](https://github.com/splunk/collector-workshop-example)にあります。詰まった場合や講師と一緒に進めたい場合に利用してください。

{{% /notice %}}

新しい _Jenkins CI_ レシーバーの開発を始めるため、まずは Go プロジェクトのセットアップから始めていきます。
新しい Go プロジェクトを作成する手順は以下の通りです：

1. `${HOME}/go/src/jenkinscireceiver` という名前の新しいディレクトリを作成し、そのディレクトリに移動します。
    1. 実際のディレクトリ名や場所は厳密ではありません。自分の開発ディレクトリを自由に選ぶことができます。
1. `go mod init splunk.conf/workshop/example/jenkinscireceiver` を実行して、Go のモジュールを初期化します。
    1. 依存関係を追跡するために使用される `go.mod` というファイルが作成されます。
    1. インポートされている依存関係のチェックサム値が `go.sum` として保存されます。

{{% expand title="{{% badge icon=check color=green title=**Check-in** %}}go.modをレビューする{{% /badge %}}" %}}

`` text
module splunk.conf/workshop/example/jenkinscireceiver

go 1.20
```

{{% /expand %}}
