---
title: 7. APM to Logs
weight: 7
---

{{% exercise title="APM から関連ログへジャンプする" %}}

問題を引き起こしている **paymentservice** のバージョンを特定できたので、エラーに関するより詳細な情報を見つけられるか確認してみましょう。ここで活躍するのが **Related Logs** です。

Related Content は、APM、Infrastructure Monitoring、Log Observer が Observability Cloud 全体でフィルタを引き継げるようにする特定のメタデータに依存しています。Related Logs を機能させるには、ログに以下のメタデータが含まれている必要があります。

* `service.name`
* `deployment.environment`
* `host.name`
* `trace_id`
* `span_id`

* **Trace Waterfall** の一番下にある **Logs** をクリックします。これにより、このトレースに対する **Related Logs** が存在することが強調表示されます。
* ポップアップ内の **Logs for trace xxx** エントリをクリックすると、完全なトレースのログが **Logs** で開きます。

![Related Logs](../images/apm-related-logs.png)

* 次に、ログ内のエラーについてさらに詳しく調べていきましょう。

{{% /exercise %}}
