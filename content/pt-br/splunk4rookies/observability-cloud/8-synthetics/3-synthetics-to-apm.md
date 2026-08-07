---
title: 3. Synthetics para APM
weight: 3
---

Agora devemos ter uma visão semelhante à abaixo.

![Fazer pedido](../images/run-results-place-order.png)

{{% exercise title="Salte de Sintéticos para APM" %}}

* Na cascata, encontre uma entrada que comece com **POST checkout**.
* Clique no botão **>** na frente dele para abrir a seção de metadados. Observe os metadados coletados e observe o cabeçalho **Server-Timing**. Este cabeçalho é o que nos permite correlacionar a execução do teste a um rastreamento de back-end.
* Clique no link azul {{% icon icon="link" %}} **APM** na linha **POST checkout** na cascata.
{{% /exercise %}}

![Rastreamento de APM](../images/apm-trace.png)

{{% exercise title="Valide a falha no pagamento no APM" %}}

* Valide se você vê um ou mais erros para **paymentservice** **(1)**.
* Para validar que é o mesmo erro, clique no conteúdo relacionado a **Logs** **(2)**.
* Repita o exercício anterior para filtrar apenas os erros.
* Visualize o log de erros para validar a falha no pagamento devido a um token inválido.

{{% /exercise %}}
