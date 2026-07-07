---
title: 1. APM Service Map
weight: 1
---

O APM Service Map exibe as dependências e conexões entre seus serviços instrumentados e inferidos em APM. O mapa é gerado dinamicamente com base nas suas seleções de intervalo de tempo, ambiente, transação de negócio, serviço e filtros de tags.

Quando clicamos no link de APM no waterfall de RUM, filtros foram adicionados automaticamente à visualização do service map para mostrar os serviços envolvidos naquela **Transaction** (`frontend:/cart/checkout`).

Você pode ver os serviços envolvidos no workflow no **Service Map**. No painel lateral, são exibidos gráficos para a transação selecionada. Quando você seleciona um serviço no **Service Map**, os gráficos no painel lateral são atualizados para mostrar métricas do serviço selecionado.

{{% exercise title="Inspecionar paymentservice no mapa" %}}

* Clique no **paymentservice** no Service Map para selecioná-lo.

![APM Explore](../images/apm-business-workflow.png)

{{< tabs >}}
{{% tab title="Pergunta" %}}
**Com o `paymentservice` selecionado, o que você pode concluir a partir do gráfico Service Requests & Errors no painel lateral?** **(1)**
{{% /tab %}}
{{% tab title="Resposta" %}}
**O percentual de Errors está muito alto.**
{{% /tab %}}
{{< /tabs >}}

* O Splunk APM também oferece **Service Centric Views** integradas para ajudar você a ver problemas em tempo real e determinar rapidamente se o problema está associado a um serviço, um endpoint específico ou à infraestrutura subjacente. Vamos olhar mais de perto.
* No painel à direita, clique em **paymentservice** em azul **(2)**.

{{% /exercise %}}
