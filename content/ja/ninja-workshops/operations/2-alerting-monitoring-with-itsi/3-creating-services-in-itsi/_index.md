---
title: ITSI でのサービスの作成
linkTitle: 3. ITSI でのサービスの作成
weight: 1
---

# エンティティタイプに基づく依存関係を持つ ITSI でのサービスの作成

このワークショップでは、既存のエンティティを使用してSplunk IT Service Intelligence (ITSI) でサービスを作成し、エンティティのタイプに基づいて依存関係を確立する方法について説明します。Splunk Observability Cloudからのビジネスワークフローを表すエンティティと、AppDynamics Business Transactionsを表すエンティティを区別します。

**シナリオ:**

2つの既存サービスがあります: "Online-Boutique-US"（Kubernetesで実行され、Splunk Observability Cloudによって監視されているアプリケーションを表す）と "AD.ECommerce"（AppDynamicsによって監視されているアプリケーションを表す）。新しいサービスを作成し、これらのサービスの1つの依存関係として追加したいと思います。このワークショップの最初の実行時に両方のサービスを作成する必要はないので、まずは興味のある方を選択してください。

![show-entry](../images/service_tree_start.png?classes=inline)

**Splunk 環境に戻り、Apps から IT Service Intelligence を選択してください**

Default Analyzerでフィルターを "Buttercup Business Health" に更新してください
