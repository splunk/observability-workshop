---
title: Creating Services in ITSI
linkTitle: 3. Creating Services in ITSI
weight: 1
---

# エンティティタイプに基づく依存関係を持つITSIでのサービス作成

このワークショップでは、既存のエンティティを使用して Splunk IT Service Intelligence (ITSI) でサービスを作成し、エンティティのタイプに基づいて依存関係を確立する方法について説明します。Splunk Observability Cloud のビジネスワークフローを表すエンティティと、AppDynamics の Business Transactions を表すエンティティを区別します。

**シナリオ:**

既存のサービスが2つあります。「Online-Boutique-US」（Kubernetes 上で動作し、Splunk Observability Cloud で監視されているアプリケーションを表す）と「AD.ECommerce」（AppDynamics で監視されているアプリケーションを表す）です。新しいサービスを作成し、これらのサービスのいずれかの依存先として追加します。このワークショップを最初に進める際には両方のサービスを作成する必要はないので、より興味のある方を選んで始めてください。

![show-entry](../images/service_tree_start.png?classes=inline)

**Splunk 環境に戻り、Apps から IT Service Intelligence を選択します**

Default Analyzer で Filter を「Buttercup Business Health」に更新します
