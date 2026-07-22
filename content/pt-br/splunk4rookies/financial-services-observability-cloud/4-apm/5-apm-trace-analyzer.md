---
title: 5. APM Trace Analyzer
weight: 5
---

Como o Splunk APM oferece visibilidade **NoSample** de ponta a ponta de todos os serviços, ele captura cada trace. Neste workshop, o **orderId** da transferência bancária está disponível como uma tag. Isso significa que podemos usá-lo para localizar o trace exato da experiência insatisfatória encontrada pelos usuários.

{{% notice title="Analisador de rastreamento" style="info" %}}

Splunk Observability Cloud fornece diversas ferramentas para explorar dados de monitoramento de aplicativos. **Trace Analyzer** é adequado para cenários em que você tem pesquisas e explorações de alta cardinalidade e alta granularidade para pesquisar problemas novos ou desconhecidos.
{{% /notice %}}

{{% notice title="Exercício" style="green" icon="running" %}}

* Com a caixa externa do **wire-transfer-service** selecionada, clique em **Traces** no painel à direita.
* Configure **Time Range** como **Last 15 minutes**.
* Certifique-se de que **Sample Ratio** esteja definido como `1:1` e **não** `1:10`.

{{% /notice %}}

![Analisador de rastreamento APM](../images/apm-trace-analyzer.png)

A visualização **Trace & error count** mostra o total de rastreamentos e rastreamentos com erros em um gráfico de barras empilhadas. Você pode usar o mouse para selecionar um período específico dentro do período disponível.

{{% notice title="Exercício" style="green" icon="running" %}}

* Clique no menu suspenso que diz **Contagem de rastreamento e erros** e altere para **Duração do rastreamento**

{{% /notice %}}

![Mapa de calor do analisador de rastreamento APM](../images/apm-trace-analyzer-heat-map.png)

A visualização **Trace Duration** mostra um mapa térmico de rastreamentos por duração.  O mapa de calor representa 3 dimensões de dados:

* Tempo no eixo x
* Duração do rastreamento no eixo y
* Os rastreamentos (ou solicitações) por segundo são representados pelos tons do mapa de calor

Você pode usar o mouse para selecionar uma área no mapa de calor, para focar em um período de tempo específico e em um intervalo de duração do rastreamento.

{{% notice title="Exercício" style="green" icon="running" %}}

* Mude de **Duração do rastreamento** de volta para **Contagem de rastreamento e erros**.
* No seletor de horário, selecione **Last 1 hour**.
* Observe que a maioria de nossos rastreamentos contém erros (vermelho) e há apenas uma quantidade limitada de rastreamentos livres de erros (azul).
* Certifique-se de que **Sample Ratio** esteja definido como `1:1` e **não** `1:10`.
* Clique em **Adicionar filtros**, digite `orderId` e selecione **orderId** na lista.
* Localize e selecione o **orderId** fornecido pelo instrutor do workshop e pressione Enter.
  ![Traces by Duration](../images/apm-trace-by-id.png)

{{% /notice %}}

Agora filtramos até chegar ao trace exato no qual os usuários relataram uma experiência insatisfatória, com uma espera muito longa pelo processamento.

Um benefício secundário da visualização desse rastreamento é que ele estará acessível por até 13 meses. Isso permitirá que os desenvolvedores retornem a esse problema posteriormente e ainda visualizem esse trace, por exemplo.

{{% notice title="Exercício" style="green" icon="running" %}}

* Clique no traço na lista.

{{% /notice %}}

A seguir, caminharemos pela cachoeira tracejada.
