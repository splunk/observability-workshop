---
title: OrbStack
weight: 2
description: Apple Silicon Mac上でのOrbStackによるローカルホスティング。
---

Orbstackとjqをインストールします:

``` bash
brew install orbstack jq
```

ワークショップのリポジトリをクローンします:

``` bash
git clone https://github.com/splunk/observability-workshop
```

Orbstackディレクトリに移動します:

```bash
cd observability-workshop/local-hosting/orbstack
```

スクリプトを実行し、インスタンス名と[SWiPE ID](https://swipe.splunk.show)を指定します。例:

``` bash
./start.sh my-instance 12345678
```

インスタンスが正常に作成されると（数分かかることがあります）、自動的にインスタンスにログインします。一度抜けた場合は、以下のコマンドでSSH接続できます（`<my_instance>`はご自身のインスタンス名に置き換えてください）:

```bash
ssh splunk@<my_instance>@orb
```

シェルに入った後、以下のコマンドを実行することでインスタンスが準備できているか確認できます:

```bash
kubectl version --output=yaml
```

インスタンスのIPアドレスを取得するには、以下のコマンドを実行します:

```bash
ifconfig eth0
```

インスタンスを削除するには、以下のコマンドを実行します:

```bash
orb delete my-instance
```
