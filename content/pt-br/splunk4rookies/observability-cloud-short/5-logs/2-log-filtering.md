---
title: 2. Filtro de Logs
weight: 2
---

{{% exercise title="Filtrar para logs de erro" %}}

* Precisamos focar apenas nas mensagens de Error nos logs:
* Clique no menu suspenso **Group By** **(1)** e use o filtro para encontrar **severity**.
* Depois de selecionar, clique no botão {{% button style="blue" %}}Apply{{% /button %}} (observe que a legenda do gráfico muda para mostrar debug, error e info).

![legend](../images/severity-logs.png)

* Para selecionar apenas os logs de erro, clique na palavra error **(2)** na legenda e selecione **Add to filter**. Em seguida, clique em {{% button style="blue" %}}Run Search{{% /button %}} no topo da página.

![Error Logs](../images/log-observer-errors.png)

{{% /exercise %}}

Em seguida, veremos as entradas de log em detalhe.
