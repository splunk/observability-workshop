---
title: カスタム サービスヘルスダッシュボード 🏥 
linkTitle: 9. Service Health Dashboard
weight: 9
archetype: chapter
---

{{% badge icon="clock" color="#ed0090" %}}15 分{{% /badge %}}

{{% notice icon="user" style="orange" title="ペルソナ" %}}

**SRE** の役割はあなたにぴったりです。そのため **paymentservice** 用のカスタムサービスヘルスダッシュボードを作り上げてほしいと求められています。要件は、RED メトリクス、ログ、および Synthetic テストの所要時間の結果を表示することです。

{{% /notice %}}

一般的に、開発チームやSREチームがアプリケーションやサービスのヘルスステータスの概要を必要とします。壁掛けのテレビ画面にこういった情報を常時表示しておくこともよくあります。Splunk Observability Cloud は、カスタムダッシュボードを作成することで、こういった要望に完璧に応えることができます。

このセクションでは、チームのモニターやテレビに表示するため、**サービスヘルスダッシュボード**を構築します。
