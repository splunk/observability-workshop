---
title: ITSIでのサービス作成
linkTitle: 3. ITSIでのサービス作成
weight: 1
---

# エンティティタイプに基づく依存関係を持つITSIでのサービス作成

このワークショップでは、Splunk IT Service Intelligence (ITSI) で既存のエンティティを使用してサービスを作成し、エンティティのタイプに基づいて依存関係を確立する方法を説明します。Splunk Observability Cloud のビジネスワークフローを表すエンティティと、AppDynamics Business Transactions を表すエンティティを区別します。

**シナリオ:**

2つの既存サービスがあります：「Online-Boutique-US」（Kubernetes上で実行され、Splunk Observability Cloud で監視されているアプリケーション）と「AD.ECommerce」（AppDynamics で監視されているアプリケーション）です。新しいサービスを作成し、これらのサービスのいずれかの依存サービスとして追加します。このワークショップの初回実行時に両方のサービスを作成する必要はありませんので、まずは興味のある方を選んで始めてください。

![show-entry](../images/service_tree_start.png?classes=inline)

**Splunk 環境に戻り、Apps から IT Service Intelligence を選択してください**

Default Analyzer で Filter を「Buttercup Business Health」に更新してください。
