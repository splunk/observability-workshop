---
title: サーバーと APM 間の相関
time: 3 minutes
weight: 5
description: サーバーメトリクスとサーバー上で実行されているアプリケーション間の相関方法を確認します
---

## サーバーとアプリケーションのコンテキスト間のナビゲーション

Server Visibility Monitoring エージェントは、同じホスト上で実行されている Splunk AppDynamics APM エージェントと自動的に関連付けられます。

Server Visibility を有効にすると、アプリケーションのコンテキストでサーバーパフォーマンスメトリクスにアクセスできます。サーバーとアプリケーションのコンテキストをさまざまな方法で切り替えることができます。以下の手順に従って、サーバーのメインダッシュボードからサーバー上で実行されている Node の1つに移動します。

1. **Dashboard** タブをクリックして、メインの Server Dashboard に戻ります。
2. **APM Correlation** リンクをクリックします。

![Server to APM](images/server-apm-link.png)

1. リストされた Tier の1つの下矢印をクリックします。
2. Tier の Node リンクをクリックします。

![Dashboard Example](images/server-tier-link.png)

これで **Node Dashboard** に移動しました。

1. **Server** タブをクリックして、関連するホストメトリクスを確認します。

![Dashboard Example](images/server-node-server.png)

Server Visibility Monitoring エージェントがインストールされている場合、ホストメトリクスは関連する Node のコンテキスト内で常に利用可能です。

サーバーとアプリケーションのコンテキスト間のナビゲーションについての詳細は、[こちら](https://help.splunk.com/en/appdynamics-saas/infrastructure-visibility/25.7.0/server-visibility/monitor-your-servers-using-server-visibility/navigating-between-server-and-application-contexts)をご覧ください。
