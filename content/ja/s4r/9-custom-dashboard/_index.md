---
title: カスタム サービスヘルスダッシュボード 🏥 
linkTitle: 9. Service Health Dashboard
weight: 9
archetype: chapter
---

{{% badge icon="clock" color="#ed0090" %}}15 分{{% /badge %}}

{{% notice icon="user" style="orange" title="ペルソナ" %}}

**SRE** の役割があなたに適しているので、引き続きそれを保ち、**paymentservice** 用のカスタムサービスヘルスダッシュボードの構築が求められています。要件は、RED メトリクス、ログ、および合成テストの所要時間の結果を表示することです。

{{% /notice %}}

開発チームやSREチームがアプリケーションやサービスの健康状態の概要を必要とすることは一般的です。これらは、壁に掛けられたテレビに表示されることがよくあります。Splunk Observability Cloud には、カスタムダッシュボードを作成するための完璧なソリューションがあります。

このセクションでは、モニターやテレビに表示するための **サービスヘルスダッシュボード** を構築します。
