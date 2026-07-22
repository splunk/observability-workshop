---
title: 1. APM Explore
weight: 1
---

O Service Map do APM exibe as dependências e conexões entre seus serviços instrumentados e inferidos no APM. O mapa é gerado dinamicamente com base nas suas seleções nos filtros de intervalo de tempo, ambiente, fluxo de trabalho, serviço e tag.

Quando clicamos no link APM na cascata RUM, filtros foram adicionados automaticamente à visualização do Service Map para mostrar os serviços que estavam envolvidos naquele **WorkFlow Name** (`frontend:/cart/checkout`).

Você pode ver os serviços envolvidos no fluxo de trabalho em **Service Map**. No painel lateral, em **Business Workflow**, são exibidos gráficos para o fluxo de trabalho selecionado. Os gráficos **Service Map** e **Business Workflow** são sincronizados. Ao selecionar um serviço no **Service Map**, os gráficos no painel **Business Workflow** são atualizados para mostrar métricas do serviço selecionado.

{{% exercise title="Inspecione o serviço de pagamento no mapa" %}}

* Clique em **paymentservice** no Mapa de serviços.

{{% /exercise %}}

![Explorar APM](../images/apm-business-workflow.png)

O Splunk APM também fornece **Service Centric Views** integrado para ajudá-lo a ver os problemas que ocorrem em tempo real e determinar rapidamente se o problema está associado a um serviço, um endpoint específico ou à infraestrutura subjacente. Vamos dar uma olhada mais de perto.

{{% exercise title="Abra a visualização do serviço de pagamento" %}}

* No painel direito, clique em **paymentservice** em azul.

{{% /exercise %}}

![Serviço APM](../images/apm-service.png)
