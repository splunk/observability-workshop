---
title: 3. Synthetics para APM
weight: 3
---

{{% exercise title="Ir de Synthetics para APM" %}}

* No waterfall, encontre uma entrada que começa com **POST checkout**. Se você não vir essa entrada, volte e selecione outro resultado com falha na página **Run results**.

![Place Order](../images/run-results-place-order.png)

* Clique em **>** **(1)** para abrir a seção de metadados. Observe os metadados coletados e repare no header **server-timing** em **Response Headers**. Esse header é o que nos permite correlacionar a execução do teste com um trace de back-end.
* Clique no link azul {{% icon icon="link" %}} **APM** **(2)** na linha **POST checkout** do waterfall.

![APM trace](../images/apm-trace.png)

* Valide que você vê um ou mais erros para o **paymentservice** **(1)**.
* Para validar que é o mesmo erro, clique no related content de **Logs** **(2)**.
* Repita o exercício anterior para filtrar apenas os erros.
* Visualize o log de erro para validar a falha no pagamento causada por um token inválido.

{{% /exercise %}}
