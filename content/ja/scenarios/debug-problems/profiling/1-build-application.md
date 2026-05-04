---
title: サンプルアプリケーションのビルド
linkTitle: 1 サンプルアプリケーションのビルド
weight: 1
time: 10 minutes
---

## はじめに

このワークショップでは、`The Door Game` という Java ベースのアプリケーションを使用します。このアプリケーションは Kubernetes 上でホストされます。

## 前提条件

EC2 インスタンスから開始し、以下の状態にするためにいくつかの[初期ステップ](#初期ステップ)を実行します。

* **Splunk distribution of the OpenTelemetry Collector** をデプロイする
* MySQL データベースコンテナをデプロイしてデータを投入する
* `doorgame` アプリケーションコンテナをビルドしてデプロイする

## 初期ステップ

初期セットアップは、EC2 インスタンスのコマンドラインで以下のステップを実行することで完了できます。

環境の名前を入力するよう求められます。`profiling-workshop-yourname`（`yourname` を実際の名前に置き換えてください）を使用してください。

``` bash
cd ~/workshop/profiling
./1-deploy-otel-collector.sh
./2-deploy-mysql.sh
./3-deploy-doorgame.sh
```

## The Door Game をプレイしよう

アプリケーションがデプロイされたので、実際に操作してオブザーバビリティデータを生成してみましょう。

EC2 インスタンスの IP アドレスのポート 81 にブラウザでアクセスすると、The Door Game アプリケーションにアクセスできます。例:

```` text
http://52.23.184.60:81
````

The Door Game のイントロ画面が表示されます。

![Door Game Welcome Screen](../images/door_game_initial_screen.png)

`Let's Play` をクリックしてゲームを開始します。

![Let's Play](../images/lets_play.png)

`Let's Play` をクリックしてから実際にゲームをプレイできるようになるまで、長い時間がかかったことに気づきましたか？

**Splunk Observability Cloud** を使用して、アプリケーションの起動がなぜこんなに遅いのかを調べてみましょう。
