---
title: 1. Filtragem de registros
weight: 1
---

**Log Observer (LO)**, pode ser usado de várias maneiras. No tour rápido, você usou a LO **interface sem código** para pesquisar entradas específicas nos logs. Esta seção, entretanto, pressupõe que você chegou em LO a partir de um rastreamento no APM usando o link **Related Content**.

A vantagem disso é, como aconteceu com o link entre RUM e APM, que você está vendo seus logs dentro do contexto de suas ações anteriores.  Nesse caso, o contexto é o intervalo de tempo **(1)**, que corresponde ao do rastreamento e ao filtro **(2)** que está definido como **trace_id**.

![Registros de rastreamento](../images/log-observer-trace-logs.png)

Essa visualização incluirá **todas** as linhas de registro de **todos** aplicativos ou serviços que participaram da transação de back-end iniciada pela interação do usuário final com a Online Boutique.

Mesmo em uma aplicação pequena, a enorme quantidade de logs pode dificultar a identificação das linhas específicas que importam para o incidente que estamos investigando.

{{% notice title="Exercício" style="green" icon="running" %}}

Precisamos nos concentrar apenas nas mensagens de erro nos logs:

* Clique na caixa suspensa **Group By** e use o filtro para encontrar **Severity**.
* Uma vez selecionado, clique no botão {{% button style="blue" %}}Apply{{% /button %}} (observe que a legenda do gráfico muda para mostrar depuração, erro e informações).
  ![legenda](../images/severity-logs.png)
* A seleção apenas dos logs de erros pode ser feita clicando na palavra erro **(1)** na legenda, seguido da seleção de **Add to filter**. Em seguida, clique em {{% button style="blue" %}}Run Search{{% /button %}}
* Você também poderia adicionar o nome do serviço, `sf_service=wire-transfer-service`, ao filtro caso existam linhas de erro de vários serviços, mas isso não é necessário no nosso caso.
  ![Registros de erros](../images/log-observer-errors.png)

{{% /notice %}}

A seguir, veremos as entradas de log em detalhes.
