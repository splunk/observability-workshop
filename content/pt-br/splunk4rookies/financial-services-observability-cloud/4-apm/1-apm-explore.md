---
title: 1. APM Explore
weight: 1
---

Ao acessar a seção APM do Splunk Observability Cloud, você verá uma visão geral dos dados do APM, incluindo os principais serviços por taxa de erros e as métricas R.E.D. de serviços e workflows.

O Service Map do APM exibe as dependências e conexões entre seus serviços instrumentados e inferidos no APM. O mapa é gerado dinamicamente com base nas suas seleções nos filtros de intervalo de tempo, ambiente, fluxo de trabalho, serviço e tag.

Você pode ver os serviços envolvidos em qualquer workflow de usuário do APM acessando o **Service Map**. Quando um serviço é selecionado no **Service Map**, os gráficos do painel lateral **Business Workflow** são atualizados para exibir as métricas do serviço selecionado. O **Service Map** e todos os indicadores são sincronizados com o seletor de tempo e com os dados exibidos nos gráficos.

{{% notice title="Exercício" style="green" icon="running" %}}

* Clique no **wire-transfer-service** no Service Map.

{{% /notice %}}

![Explorar APM](../images/apm-business-workflow.png)

O Splunk APM também fornece **Service Centric Views** integrado para ajudá-lo a ver os problemas que ocorrem em tempo real e determinar rapidamente se o problema está associado a um serviço, um endpoint específico ou à infraestrutura subjacente. Vamos dar uma olhada mais de perto.

{{% notice title="Exercício" style="green" icon="running" %}}

* No painel à direita, clique em **wire-transfer-service**, exibido em azul.

{{% /notice %}}

![Serviço APM](../images/apm-service.png)
