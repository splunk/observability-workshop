---
title: Adicionando um gráfico personalizado
linkTitle: 2. Adicionando um gráfico personalizado
weight: 3
---

Nesta parte do workshop vamos criar um gráfico que adicionaremos ao nosso dashboard, também iremos vinculá-lo ao detector que construímos anteriormente. Isso nos permitirá ver o comportamento de nosso teste e ser alertados se um ou mais de nossos testes violarem seu SLA.

{{% exercise title="Adicione um gráfico de barras personalizado" %}}

* Na parte superior do painel, clique em **+** e selecione **Chart**.
  ![nova tela do gráfico](../images/new-chart.png)
* Primeiro, use o campo de entrada {{% button style="grey" %}}Untitled chart{{% /button %}} e nomeie o gráfico como **Overall Test Duration**.
* Para este exercício queremos um gráfico de barras ou colunas, então clique no terceiro ícone {{% icon icon="chart-bar" %}} na caixa de opções do gráfico.
* Em **Plot editor**, insira `synthetics.run.duration.time.ms` (este é o tempo de execução do nosso teste) na caixa **Signal** e pressione Enter.
* No momento vemos barras coloridas diferentes, uma cor diferente para cada região de onde o teste é executado. Como isso não é necessário, podemos mudar esse comportamento adicionando algumas análises.
* Clique no botão {{% button style="blue" %}}Add analytics{{% /button %}}.
* No menu suspenso, escolha a opção **Mean**, escolha `mean:aggregation` e clique fora da caixa de diálogo. Observe como o gráfico muda para uma única cor à medida que as métricas são agregadas.
* O eixo x atualmente não representa o tempo para alterar este clique no ícone de configurações {{% icon icon="cog" %}} no final da linha do gráfico. A seguinte caixa de diálogo será aberta:
  ![configuração do sinal](../images/signal-setup.png)
* Altere **Display units** **(2)** na caixa suspensa de **None** para **Tempo (escalonamento automático)/Milisegundos(ms)**. O menu suspenso muda para **Millisecond** e o eixo x do gráfico agora representa o tempo de duração do teste.
* Feche a caixa de diálogo clicando no ícone de configurações {{% icon icon="cog" %}} ou no botão {{% button style="gray" %}}close{{% /button %}}.
* Adicione nosso detector clicando no botão {{% button style="blue" %}}Link Detector{{% /button %}} e comece a digitar o nome do detector que você criou anteriormente.
* Clique no nome do detector para selecioná-lo.
* Observe que uma borda colorida aparece ao redor do gráfico, indicando o status do alerta, junto com um ícone de sino na parte superior do painel, conforme mostrado abaixo:
  ![detector adicionado](../images/detector-added.png)
* Clique no botão {{% button style="blue" %}}Save and close{{% /button %}}.
* No painel, mova os gráficos para que fiquem como na captura de tela abaixo:
  ![Painel de integridade do serviço](../images/service-health-dashboard.png)
* Para a tarefa final, clique em três pontos verticais **⋮** no canto superior direito da página (ao lado de **AI Assistant**) e clique em **View fullscreen**. Esta será a visualização que você usaria no monitor de TV na parede (pressione Esc para voltar).

{{% /exercise %}}

{{% notice title="Dica" style="primary" icon="lightbulb" %}}

Em seu tempo livre, tente adicionar outro gráfico personalizado ao painel usando métricas RUM. Você pode copiar um gráfico do grupo de painel pronto para uso **Aplicativos RUM**. Ou você pode usar a métrica RUM `rum.client_error.count` para criar um gráfico que mostre o número de erros do cliente no aplicativo.

{{% /notice %}}

 Por fim, faremos um encerramento do workshop.
