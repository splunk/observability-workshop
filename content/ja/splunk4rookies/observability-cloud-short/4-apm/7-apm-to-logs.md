---
title: 7. APM to Logs
weight: 7
---

{{% exercise title="APM から関連ログへジャンプ" %}}

問題を引き起こしている **paymentservice** のバージョンを特定できたので、エラーに関するより詳しい情報を見つけられるか確認しましょう。ここで **Related Logs**（関連ログ）の出番です。

Related Content は、APM、Infrastructure Monitoring、Log Observer が Observability Cloud 全体にフィルタを引き継ぐための特定のメタデータに依存しています。Related Logs を機能させるためには、ログに以下のメタデータが含まれている必要があります。

* `service.name`
* `deployment.environment`
* `host.name`
* `trace_id`
* `span_id`

* **Trace Waterfall** の一番下にある **Logs** をクリックします。これにより、このトレースに **Related Logs** が存在することが示されます。
* ポップアップ内の **Logs for trace xxx** エントリをクリックすると、トレース全体に対応するログが **Logs** で開かれます。

![Related Logs](../images/apm-related-logs.png)

* 次に、ログでエラーに関する詳細を確認していきましょう。

{{% /exercise %}}
