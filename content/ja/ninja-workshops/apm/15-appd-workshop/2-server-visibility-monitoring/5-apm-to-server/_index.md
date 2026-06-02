---
title: サーバーと APM の相関分析
time: 3 minutes
weight: 5
description: サーバーメトリクスとサーバー上で稼働するアプリケーションの相関分析方法を確認します
---

## サーバーとアプリケーションのコンテキスト間を移動する

Server Visibility Monitoring エージェントは、同一ホスト上で実行されている Splunk AppDynamics APM エージェントと自動的に関連付けられます。

Server Visibility を有効化すると、アプリケーションのコンテキストでサーバーのパフォーマンスメトリクスにアクセスできます。サーバーとアプリケーションのコンテキスト間は、さまざまな方法で切り替えられます。以下の手順に従って、サーバーのメインダッシュボードから、そのサーバー上で稼働している Node へと移動します。

1. **Dashboard** タブをクリックし、メインの Server Dashboard に戻ります。
2. **APM Correlation** リンクをクリックします。

![Server to APM](images/server-apm-link.png)

1. 表示されている Tier のいずれかの下矢印をクリックします。
2. Tier の Node リンクをクリックします。

![Dashboard Example](images/server-tier-link.png)

これで **Node Dashboard** に遷移します。

1. **Server** タブをクリックすると、関連するホストメトリクスが表示されます。

![Dashboard Example](images/server-node-server.png)

Server Visibility Monitoring エージェントをインストールしている場合、ホストメトリクスは関連する Node のコンテキストで常に参照できます。

サーバーとアプリケーションのコンテキスト間の移動については、[こちら](https://help.splunk.com/en/appdynamics-saas/infrastructure-visibility/25.7.0/server-visibility/monitor-your-servers-using-server-visibility/navigating-between-server-and-application-contexts)で詳しく確認できます。
