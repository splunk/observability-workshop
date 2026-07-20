---
title: アプリケーションでAnalyticsを有効にする
time: 2 minutes
weight: 2
description: この演習では、WebブラウザからAppDynamics Controllerにアクセスし、Agentless Analyticsを有効にします。

---

Analyticsは以前、Machine Agentにバンドルされた別のエージェントが必要でした。しかし現在、Analyticsはエージェントレスとなり、.NET Agent >= 20.10およびJava Agent >= 4.5.15（Controllers >= 4.5.16）のAPM Agentに組み込まれています。

この演習では、WebブラウザからAppDynamics Controllerにアクセスし、Agentless Analyticsを有効にします。

## Controllerにログインする

Ciscoの認証情報を使用して [AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) にログインします。

## Analytics設定に移動する

1. ** 画面左上の **Analytics** タブを選択します。
2. ** 左側の **Configuration** タブを選択します。
3. ** **Transaction Analytics - Configuration** タブを選択します。
4. ** アプリケーション **Supercat-Trader-YOURINITIALS** の横にある **チェックボックスをオン** にします。
5. ** **Save** ボタンをクリックします。

![Enable Analytics](images/05-biq-transaction-analytics.png)

## Transaction Summaryを検証する

Analyticsがそのアプリケーションで動作し、トランザクションが表示されていることを確認します。

1. 左メニューの **Analytics tab** タブを選択します。
2. **Home** タブを選択します。
3. **Transactions from** でアプリケーション **Supercar-Trader-YOURINITIALS** にフィルタリングします。

![Validate Analytics](images/05-biq-transaction-analytics.png)
