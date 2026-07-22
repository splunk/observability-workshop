---
title: 5. APM Trace Analyzer
weight: 5
---

Como o Splunk APM fornece **NoSample Tracing** e suporta traces de ponta a ponta de cada serviço, o Splunk APM captura todos os rastreamentos. Para este workshop, o **Order Confirmation ID** está disponível como tag. Isso significa que podemos usar isso para procurar o traço exato da experiência ruim do usuário que você encontrou anteriormente no workshop.

{{% notice title="Analisador de rastreamento" style="info" %}}

Splunk Observability Cloud fornece diversas ferramentas para explorar dados de monitoramento de aplicativos. **Trace Analyzer** é adequado para cenários em que você tem pesquisas e explorações de alta cardinalidade e alta granularidade para pesquisar problemas novos ou desconhecidos.
{{% /notice %}}

{{% exercise title="Abra o analisador de rastreamento" %}}

* Com a caixa externa de **paymentservice** selecionada, no painel direito, clique em **Traces**.
* Configure **Time Range** como **Last 15 minutes**.
* Certifique-se de que **Sample Ratio** esteja definido como `1:1` e **não** `1:10`.

{{% /exercise %}}

![Analisador de rastreamento APM](../images/apm-trace-analyzer.png)

A visualização **Trace & error count** mostra o total de rastreamentos e rastreamentos com erros em um gráfico de barras empilhadas. Você pode usar o mouse para selecionar um período específico dentro do período disponível.

{{% exercise title="Mudar para visualização de duração do rastreamento" %}}

* Clique no menu suspenso que diz **Contagem de rastreamento e erros** e altere para **Duração do rastreamento**

{{% /exercise %}}

![Mapa de calor do analisador de rastreamento APM](../images/apm-trace-analyzer-heat-map.png)

A visualização **Trace Duration** mostra um mapa térmico de rastreamentos por duração.  O mapa de calor representa 3 dimensões de dados:

* Tempo no eixo x
* Duração do rastreamento no eixo y
* Os rastreamentos (ou solicitações) por segundo são representados pelos tons do mapa de calor

Você pode usar o mouse para selecionar uma área no mapa de calor, para focar em um período de tempo específico e em um intervalo de duração do rastreamento.

{{% exercise title="Compare rastreamentos de erros ao longo de uma hora" %}}

* Mude de **Duração do rastreamento** de volta para **Contagem de rastreamento e erros**.
* No seletor de horário, selecione **Last 1 hour**.
* Observe que a maioria de nossos rastreamentos contém erros (vermelho) e há apenas uma quantidade limitada de rastreamentos livres de erros (azul).
* Certifique-se de que **Sample Ratio** esteja definido como `1:1` e **não** `1:10`.
* Clique em **Adicionar filtros**, digite `orderId` e selecione **orderId** na lista.
* Cole seu **Order Confirmation ID** de quando você foi às compras anteriormente no workshop e pressione Enter. Se você não capturou um, peça um ao seu instrutor.
  ![Traços por duração](../images/apm-trace-by-duration.png)

{{% /exercise %}}

Agora filtramos o trace exato onde você encontrou uma experiência de usuário ruim com uma espera de checkout muito longa.

Um benefício secundário da visualização desse rastreamento é que ele estará acessível por até 13 meses. Isso permitirá que os desenvolvedores retornem a esse problema posteriormente e ainda visualizem esse trace, por exemplo.

{{% exercise title="Abra um rastreamento com falha" %}}

* Clique no traço na lista.

{{% /exercise %}}

A seguir, caminharemos pela cachoeira tracejada.
