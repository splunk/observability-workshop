---
title: アプリケーションでの Analytics の有効化
time: 2 minutes
weight: 2
description: この演習では、Web ブラウザから AppDynamics Controller にアクセスし、そこから Agentless Analytics を有効化します。

---

Analytics はかつて Machine Agent にバンドルされた別個のエージェントを必要としていました。しかし現在は agentless となり、Controller >= 4.5.16 上で .NET Agent >= 20.10 および Java Agent >= 4.5.15 の両方で APM Agent に組み込まれています。

この演習では、Web ブラウザから AppDynamics Controller にアクセスし、そこから Agentless Analytics を有効化します。

## Controller へのログイン

Cisco の認証情報を使用して [AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) にログインします。

## Analytics 設定への移動

1. ** 画面左上の **Analytics** タブを選択します。
2. ** 左側の **Configuration** タブを選択します。
3. ** **Transaction Analytics - Configuration** タブを選択します。
4. ** お使いのアプリケーション **Supercat-Trader-YOURINITIALS** の隣の **チェックボックスをマーク** します。
5. ** **Save** ボタンをクリックします。

![Enable Analytics](images/05-biq-transaction-analytics.png)

## トランザクションサマリーの検証

そのアプリケーションで Analytics が動作し、トランザクションが表示されていることを確認します。

1. 左メニューの **Analytics tab** タブを選択します。
2. **Home** タブを選択します。
3. **Transactions from** で、お使いのアプリケーション **Supercar-Trader-YOURINITIALS** にフィルターします。

![Validate Analytics](images/05-biq-transaction-analytics.png)
