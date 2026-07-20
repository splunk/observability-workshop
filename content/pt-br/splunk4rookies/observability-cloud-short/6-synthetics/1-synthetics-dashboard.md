---
title: 1. Dashboard de Synthetics
weight: 1
---

{{% exercise title="Encontrar uma execução com falha em Synthetics" %}}

* No Splunk Observability Cloud, no menu principal, clique em **Digital Experience → Synthetics tests**. Clique em **All** ou **Browser tests** para ver a lista de testes ativos.

* Durante nossa investigação na seção de RUM, encontramos um problema com a Transaction **Place Order**. Vamos ver se também conseguimos confirmar isso pelo teste de Synthetics.

---

* Na caixa **Search**, digite **[NAME OF WORKSHOP]** para filtrar os testes deste workshop.
* Selecione o teste.
* Clique em **Go to all run results**.
* Altere **All** para **Failure** **(1)**.

  ![Transaction Filter](../images/failed-run-results.png)

* Clique em um dos resultados com falha.

{{% /exercise %}}
