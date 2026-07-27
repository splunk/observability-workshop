---
title: サーバーと APM の相関
time: 3 minutes
weight: 5
description: サーバーメトリクスとサーバー上で実行されているアプリケーション間の相関方法を確認します。
---

## サーバーとアプリケーションのコンテキスト間の移動

Server Visibility Monitoringエージェントは、同じホスト上で実行されているSplunk AppDynamics APMエージェントと自動的に関連付けられます。

Server Visibilityを有効にすると、アプリケーションのコンテキストでサーバーパフォーマンスメトリクスにアクセスできます。さまざまな方法でサーバーとアプリケーションのコンテキストを切り替えることができます。以下のステップに従って、サーバーメインダッシュボードからサーバー上で実行されているNodeの1つに移動します。

1. **Dashboard** タブをクリックしてメインのServer Dashboardに戻ります。
2. **APM Correlation** リンクをクリックします。

![Server to APM](images/server-apm-link.png)

1. リストされているTierの1つで下矢印をクリックします。
2. TierのNodeリンクをクリックします。

![Dashboard Example](images/server-tier-link.png)

これで **Node Dashboard** に移動しました。

1. **Server** タブをクリックして関連するホストメトリクスを確認します。

![Dashboard Example](images/server-node-server.png)

Server Visibility Monitoringエージェントがインストールされている場合、ホストメトリクスは関連するNodeのコンテキスト内で常に利用可能です。

サーバーとアプリケーションのコンテキスト間の移動について詳しくは[こちら](https://help.splunk.com/en/appdynamics-saas/infrastructure-visibility/25.7.0/server-visibility/monitor-your-servers-using-server-visibility/navigating-between-server-and-application-contexts)をご覧ください。
