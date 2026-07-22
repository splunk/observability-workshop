---
title: 1. Filtragem de registros
weight: 1
---

**Log Observer (LO)**, pode ser usado de várias maneiras. No tour rápido, você usou a LO **interface sem código** para pesquisar entradas específicas nos logs. Esta seção, entretanto, pressupõe que você chegou em LO a partir de um rastreamento no APM usando o link **Related Content**.

A vantagem disso é, como aconteceu com o link entre RUM e APM, que você está vendo seus logs dentro do contexto de suas ações anteriores.  Nesse caso, o contexto é o intervalo de tempo **(1)**, que corresponde ao do rastreamento e ao filtro **(2)** que está definido como **trace_id**.

![Registros de rastreamento](../images/log-observer-trace-logs.png)

Essa visualização incluirá **todas** as linhas de registro de **todos** aplicativos ou serviços que participaram da transação de back-end iniciada pela interação do usuário final com a Online Boutique.

Mesmo em um aplicativo pequeno como nossa Online Boutique, a grande quantidade de logs encontrados pode dificultar a visualização das linhas de log específicas que são importantes para o incidente real que estamos investigando.

{{% exercise title="Filtrar para logs de erros" %}}

Precisamos nos concentrar apenas nas mensagens de erro nos logs:

* Clique na caixa suspensa **Group By** e use o filtro para encontrar **Severity**.
* Uma vez selecionado, clique no botão {{% button style="blue" %}}Apply{{% /button %}} (observe que a legenda do gráfico muda para mostrar depuração, erro e informações).
  ![legenda](../images/severity-logs.png)
* A seleção apenas dos logs de erros pode ser feita clicando na palavra erro **(1)** na legenda, seguido da seleção de **Add to filter**. Em seguida, clique em {{% button style="blue" %}}Run Search{{% /button %}}
* Você também pode adicionar o nome do serviço, `sf_service=paymentservice`, ao filtro se houver linhas de erro para vários serviços, mas em nosso caso, isso não é necessário.
  ![Registros de erros](../images/log-observer-errors.png)

{{% /exercise %}}

A seguir, veremos as entradas de log em detalhes.
