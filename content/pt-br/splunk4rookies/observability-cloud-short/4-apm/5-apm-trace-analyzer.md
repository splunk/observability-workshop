---
title: 5. APM Trace Analyzer
weight: 5
---

Chegamos ao **Trace Analyzer**.

O **Trace Analyzer** é uma ferramenta poderosa do Splunk APM para explorar e analisar traces distribuídos em escala. Como o Splunk APM captura todos os traces com fidelidade completa (NoSample), você tem visibilidade total de todas as transações que passam pelos seus serviços.

O Trace Analyzer permite:

* **Pesquisar com tags de alta cardinalidade**: filtre traces usando qualquer span tag indexada, como IDs de cliente, IDs de pedido ou atributos customizados de negócio.
* **Visualizar padrões de trace**: veja contagens de traces e erros ao longo do tempo para identificar tendências e anomalias.
* **Analisar a distribuição de latência**: use a visualização de heatmap para entender padrões de duração dos traces e localizar outliers.
* **Aprofundar em traces específicos**: encontre rapidamente o trace exato de que você precisa, seja para investigar uma reclamação de cliente ou depurar uma transação específica.

Isso torna o Trace Analyzer ideal para investigar problemas desconhecidos, pesquisar transações específicas e fazer análise de causa raiz quando você precisa encontrar uma agulha no palheiro.

{{% exercise title="Encontrar um trace de checkout com falha" %}}

![APM Trace Analyzer](../images/apm-trace-analyzer.png)

* Encontre um trace com:
  * um erro no **checkoutservice** e no **paymentservice** **(1)**
  * e uma **Initiating Operation** de `frontend: POST /cart/checkout`
  * então selecione o **Trace ID** azul **(2)** para continuar
* Isso abrirá o **Trace Waterfall** desse trace específico.

{{% /exercise %}}
