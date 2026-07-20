---
title: ITSIでのサービス作成
linkTitle: 3. ITSIでのサービス作成
weight: 1
---

# エンティティタイプに基づく依存関係を持つITSIでのサービス作成

このワークショップでは、Splunk IT Service Intelligence（ITSI）で既存のエンティティを使用してサービスを作成し、エンティティのタイプに基づいて依存関係を確立する方法を説明します。Splunk Observability Cloudのビジネスワークフローを表すエンティティと、AppDynamics Business Transactionsを表すエンティティを区別します。

**シナリオ:**

既存のサービスが2つあります。「Online-Boutique-US」（Kubernetesで実行され、Splunk Observability Cloudによってモニタリングされているアプリケーションを表す）と「AD.ECommerce」（AppDynamicsによってモニタリングされているアプリケーションを表す）です。新しいサービスを作成し、これらのサービスのいずれかの依存サービスとして追加します。このワークショップの初回実行時に両方のサービスを作成する必要はありませんので、より興味のある方を選んで始めてください。

![show-entry](../images/service_tree_start.png?classes=inline)

**Splunk環境に戻り、Appsの下からIT Service Intelligenceを選択します**

Default Analyzerで、Filterを「Buttercup Business Health」に更新します
