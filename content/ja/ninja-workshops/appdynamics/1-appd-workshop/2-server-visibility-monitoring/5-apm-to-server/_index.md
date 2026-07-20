---
title: サーバーとAPMの相関
time: 3 minutes
weight: 5
description: サーバーメトリクスとサーバー上で稼働するアプリケーション間の相関を確認する方法を学びます
---

## サーバーとアプリケーションのコンテキスト間を移動する

Server Visibility Monitoringエージェントは、同じホスト上で稼働するSplunk AppDynamics APMエージェントと自動的に関連付けられます。

Server Visibilityを有効にすると、アプリケーションのコンテキスト内でサーバーパフォーマンスメトリクスにアクセスできます。サーバーとアプリケーションのコンテキスト間をさまざまな方法で切り替えることができます。以下の手順に従って、サーバーのメインダッシュボードからサーバー上で稼働するNodeの1つに移動します。

1. **Dashboard** タブをクリックしてメインのServer Dashboardに戻ります。
2. **APM Correlation** リンクをクリックします。

![Server to APM](images/server-apm-link.png)

1. 一覧表示されたTierの1つで下矢印をクリックします。
2. TierのNodeリンクをクリックします。

![Dashboard Example](images/server-tier-link.png)

**Node Dashboard** が表示されます。

1. **Server** タブをクリックして関連するホストメトリクスを確認します

![Dashboard Example](images/server-node-server.png)

Server Visibility Monitoringエージェントがインストールされている場合、関連するNodeのコンテキスト内でホストメトリクスを常に確認できます。

サーバーとアプリケーションのコンテキスト間の移動について詳しくは[こちら](https://help.splunk.com/en/appdynamics-saas/infrastructure-visibility/25.7.0/server-visibility/monitor-your-servers-using-server-visibility/navigating-between-server-and-application-contexts)を参照してください。
