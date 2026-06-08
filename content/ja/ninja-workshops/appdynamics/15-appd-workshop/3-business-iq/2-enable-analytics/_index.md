---
title: アプリケーションで Analytics を有効にする
time: 2 minutes
weight: 2
description: この演習では、Web ブラウザから AppDynamics Controller にアクセスし、Agentless Analytics を有効にします。

---

Analytics は以前、Machine Agent にバンドルされた別のエージェントが必要でした。しかし、現在 Analytics はエージェントレスとなり、.NET Agent >= 20.10 および Java Agent >= 4.5.15（Controllers >= 4.5.16）の APM Agent に組み込まれています。

この演習では、Web ブラウザから AppDynamics Controller にアクセスし、Agentless Analytics を有効にします。

## Controller にログインする

Cisco の認証情報を使用して [AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) にログインします。

## Analytics の設定に移動する

1. ** 画面左上の **Analytics** タブを選択します。
2. ** 左側の **Configuration** タブを選択します。
3. ** **Transaction Analytics - Configuration** タブを選択します。
4. ** アプリケーション **Supercat-Trader-YOURINITIALS** の横にある**チェックボックスをオン**にします。
5. ** **Save** ボタンをクリックします。

![Enable Analytics](images/05-biq-transaction-analytics.png)

## Transaction Summary の検証

Analytics がそのアプリケーションで動作しており、トランザクションが表示されていることを確認します。

1. 左メニューの **Analytics tab** タブを選択します。
2. **Home** タブを選択します。
3. **Transactions from** でアプリケーション **Supercar-Trader-YOURINITIALS** にフィルタリングします。

![Validate Analytics](images/05-biq-transaction-analytics.png)
