---
title: 7. APM para Logs
weight: 7
---

{{% exercise title="Ir de APM para Related Logs" %}}

Agora que identificamos a versão do **paymentservice** que está causando o problema, vamos ver se conseguimos encontrar mais informações sobre o erro. É aqui que entram os **Related Logs**.

Related Content depende de metadados específicos que permitem que APM, Infrastructure Monitoring e Log Observer passem filtros entre áreas do Observability Cloud. Para que logs relacionados funcionem, você precisa ter os seguintes metadados nos seus logs:

* `service.name`
* `deployment.environment`
* `host.name`
* `trace_id`
* `span_id`

* Bem no final do **Trace Waterfall**, clique em **Logs**. Isso destaca que existem **Related Logs** para este trace.
* Clique na entrada **Logs for trace xxx** no pop-up. Isso abrirá os logs do trace completo em **Logs**.

![Related Logs](../images/apm-related-logs.png)

* Agora vamos descobrir mais sobre o erro nos logs.

{{% /exercise %}}
