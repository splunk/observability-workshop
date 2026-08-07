---
title: Adicionando um gráfico personalizado
linkTitle: 2. Adicionando um gráfico personalizado
weight: 3
---

Nesta parte do workshop vamos criar um gráfico que adicionaremos ao nosso dashboard, também iremos vinculá-lo ao detector que construímos anteriormente. Isso nos permitirá ver o comportamento de nosso teste e ser alertados se um ou mais de nossos testes violarem seu SLA.

{{% notice title="Exercício" style="green" icon="running" %}}

* Na parte superior do painel, clique em **+** e selecione **Chart**.
  ![nova tela do gráfico](../images/new-chart.png)
* Primeiro, use o campo de entrada {{% button style="grey" %}}Untitled chart{{% /button %}} e dê ao gráfico o nome **Requests by version & error**.
* Para este exercício queremos um gráfico de barras ou colunas, então clique no terceiro ícone {{% icon icon="chart-bar" %}} na caixa de opções do gráfico.
* No **Plot editor**, insira `spans.count` (esse é o tempo de execução do nosso teste) na caixa **Signal** e pressione Enter.
* Clique em {{% button style="blue" %}}Add filter{{% /button %}} e escolha `sf_service:wire-transfer-service`.
* No momento vemos barras coloridas diferentes, uma cor diferente para cada região de onde o teste é executado. Como isso não é necessário, podemos mudar esse comportamento adicionando algumas análises.
* Clique no botão {{% button style="blue" %}}Add analytics{{% /button %}}.
* No menu suspenso, escolha a opção **Sum**, selecione `sum:aggregation`, clique em `version` e depois em `sf_error` para agrupar por essas duas dimensões. Observe como o gráfico muda agora que as métricas estão agregadas.
![new chart screen](../images/spans-sum-version-error.png)
* Clique no botão {{% button style="blue" %}}Save and close{{% /button %}}.
* No painel, mova os gráficos para que fiquem como na captura de tela abaixo:
  ![Painel de integridade do serviço](../images/service-health-dashboard.png)
* Para a tarefa final, clique nos três pontos **...** na parte superior da página (ao lado de **Event Overlay**) e clique em **View fullscreen**. Essa é a visualização que você usaria no monitor de TV na parede (pressione Esc para voltar).

{{% /notice %}}

{{% notice title="Dica" style="primary" icon="lightbulb" %}}

Quando tiver tempo, experimente adicionar outro gráfico personalizado ao dashboard usando métricas do APM ou de Infrastructure. Você pode copiar um gráfico do grupo de dashboards pronto para uso **Kubernetes**. Também pode usar a métrica `traces.count` do APM para criar um gráfico que mostre o número de erros em um endpoint específico.

{{% /notice %}}

 Por fim, faremos um encerramento do workshop.
