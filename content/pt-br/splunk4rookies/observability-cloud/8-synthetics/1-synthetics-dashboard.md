---
title: 1. Dashboard de Synthetics
weight: 1
---

No Splunk Observability Cloud, no menu principal, clique em **Synthetics**. Clique em **All** ou **Browser tests** para ver a lista de testes ativos.

Durante nossa investigação na seção RUM, descobrimos que havia um problema com a transação **Place Order**. Vamos ver se podemos confirmar isso também no teste Synthetics. Usaremos a métrica **Tempo do primeiro byte** para a 4ª página do teste, que é a etapa **Place Order**.

{{% exercise title="Analise o desempenho do seu teste" %}}

* Na caixa **Search** digite **[WORKSHOP NAME]** e selecione o teste para o seu workshop (seu instrutor irá aconselhar qual deles selecionar).
* Em **Performance KPIs**, defina o Seletor de tempo como **Last 1 hour** e pressione Enter.
* Clique em **Location** e no menu suspenso selecione **Page**. O próximo filtro será preenchido com as páginas que fazem parte do teste.
* Clique em **Duration**, desmarque **Duration** e selecione **Tempo do primeiro byte**.
  ![Filtro de transação](../images/synthetics-transaction-filter.png)
* Observe a legenda e observe a cor de **Tempo do primeiro byte - Página 4**.
* Selecione o ponto de dados mais alto para **Tempo do primeiro byte - Página 4**. Agora você será levado ao **Run results** para esta execução de teste específica.
{{% /exercise %}}
