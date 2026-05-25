---
title: OrbStack
weight: 2
description: OrbStack を使用してローカルホスティング環境を作成する方法 - Mac (Apple Silicon)
---

OrbStack と jq をインストールします:

``` bash
brew install orbstack jq
```

ワークショップリポジトリをクローンします:

``` bash
git clone https://github.com/splunk/observability-workshop
```

OrbStack ディレクトリに移動します:

```bash
cd observability-workshop/local-hosting/orbstack
```

スクリプトを実行し、インスタンス名と [SWiPE ID](https://swipe.splunk.show) を指定します（例）:

``` bash
./start.sh my-instance 12345678
```

インスタンスが正常に作成されると（数分かかる場合があります）、自動的にインスタンスにログインされます。終了した場合は、以下のコマンドで SSH 接続できます（`<my_instance>` をインスタンス名に置き換えてください）:

```bash
ssh splunk@<my_instance>@orb
```

シェルに入ったら、以下のコマンドを実行してインスタンスの準備ができていることを確認できます:

```bash
kubectl version --output=yaml
```

インスタンスの IP アドレスを取得するには、以下のコマンドを実行します:

```bash
ifconfig eth0
```

インスタンスを削除するには、以下のコマンドを実行します:

```bash
orb delete my-instance
```
