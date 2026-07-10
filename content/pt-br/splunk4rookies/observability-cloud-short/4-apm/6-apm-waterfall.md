---
title: 6. APM Waterfall
weight: 6
---

A visualização **Trace Waterfall** mostra todos os spans de um trace como uma linha do tempo hierárquica. Cada span aparece como uma barra horizontal, em que o comprimento da barra representa sua duração e sua posição mostra quando ele ocorreu em relação aos outros spans.

Um trace é uma coleção de spans que compartilham o mesmo trace ID, representando uma transação única processada pela sua aplicação e pelos serviços que a compõem.

Um span representa uma única unidade de trabalho dentro de um trace, capturando informações sobre uma operação específica, como uma chamada de API, consulta a banco de dados ou requisição de serviço. Cada span inclui metadados como nome da operação, horário de início, duração e tags ou atributos associados que fornecem contexto sobre o trabalho executado.

{{% exercise title="Abrir o span com falha" %}}

* Clique no {{% button style="red"  %}}!{{% /button %}} ao lado de qualquer um dos spans `paymentservice:grpc.hipstershop.PaymentService/Charge` no waterfall.

![Trace Waterfall](../images/apm-trace-waterfall.png)

{{< tabs >}}
{{% tab title="Pergunta" %}}
**Qual mensagem de erro e qual versão são reportadas em Span Details?**
{{% /tab %}}
{{% tab title="Resposta" %}}
**`Invalid request` e `v350.10`**.
{{% /tab %}}
{{< /tabs >}}

{{% /exercise %}}
