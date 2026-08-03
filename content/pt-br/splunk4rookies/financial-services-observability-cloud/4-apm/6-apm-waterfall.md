---
title: 6. APM Waterfall
weight: 6
---

Chegamos ao **Trace Waterfall** do **Trace Analyzer**. Um trace é uma coleção de intervalos que compartilham o mesmo ID de rastreamento, representando uma transação exclusiva tratada pelo seu aplicativo e seus serviços constituintes.

Cada intervalo no Splunk APM captura uma única operação. O Splunk APM considera um intervalo como um intervalo de erro se a operação que o intervalo captura resultar em um erro.

![Traçar cascata](../images/apm-trace-waterfall.png)

{{% notice title="Exercício" style="green" icon="running" %}}

* Clique em {{% button style="red"  %}}!{{% /button %}} ao lado de qualquer span do `wire-transfer-service` no waterfall.

{{< tabs >}}
{{% tab title="Pergunta" %}}
**Qual é a mensagem de erro e a versão relatada nos Span Details?**
{{% /tab %}}
{{% tab title="Resposta" %}}
**`Invalid request` e `v350.10`**.
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}
Agora que identificamos a versão do **wire-transfer-service** que está causando o problema, vamos buscar mais informações sobre o erro. É aqui que entram os **Related Logs**.

O Related Content depende de metadados específicos que permitem que APM, Monitoramento de Infraestrutura e Log Observer passem filtros pelo Observability Cloud. Para que os logs relacionados funcionem, você precisa ter os seguintes metadados nos seus logs:

* `service.name`
* `deployment.environment`
* `host.name`
* `trace_id`
* `span_id`

{{% notice title="Exercício" style="green" icon="running" %}}

* Na parte inferior de **Trace Waterfall**, clique em **Logs (1)**. Isso destaca que existem **Related Logs** para esse rastreamento.
* Clique na entrada **Logs for trace xxx** no pop-up, isso abrirá os logs para o rastreamento completo em **Log Observer**.

{{% /notice %}}

![Registros relacionados](../images/apm-related-logs.png)

A seguir, vamos descobrir mais sobre o erro nos logs.
