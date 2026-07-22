---
title: Synthetics Home Page
linkTitle: 5.1 Synthetics Home Page
weight: 2
---

Clique em **Digital Experience** no menu principal e, em seguida, em Monitoramento Sintético, clique em **Synthetic Tests**. Isso nos levará à página inicial do Synthetics. Possui 3 seções distintas que fornecem informações úteis ou permitem escolher ou criar um teste sintético.

![Principal sintético](../images/synthetics-main.png)

1. **Onboarding Pane:** Vídeos de treinamento e links para documentação para você começar a usar o Splunk Synthetics.
2. **Test Pane:** Lista de todos os testes que estão configurados (**Browser**, **API** e **HTTP**)
3. **Create New Test:** Menu suspenso para criar novos testes sintéticos.

{{% notice title="Informações" style="info" %}}
Como parte do workshop, criamos um teste de navegador padrão para o aplicativo que estamos executando. Você o encontra no Painel de Teste **(2)**. Ele terá o seguinte nome **Workshop Browser Test for**, seguido do nome do seu Workshop (seu instrutor deverá ter fornecido isso a você).
{{% /notice %}}
Para continuar nosso tour, vejamos o resultado do teste automático de navegador do nosso workshop.

{{% exercise title="Abra a visão geral de Sintéticos" %}}

* No Painel de Teste, clique na linha que contém o nome do seu workshop. O resultado deve ficar assim:

![Visão geral da síntese](../images/synthetics-test-overview.png)

* Observe que na página Testes Sintéticos, o primeiro painel mostrará o desempenho do seu site no último dia, 8 dias e 30 dias. Conforme mostrado na captura de tela acima, somente se um teste tiver começado o suficiente no passado, o gráfico correspondente conterá dados válidos. Para o workshop, isso depende de quando foi criado.
* No menu suspenso KPI de desempenho, altere o tempo padrão de 4 horas para a última hora.
{{< tabs >}}
{{% tab title="Pergunta" %}}
**Com que frequência o teste é executado e de onde?**
{{% /tab %}}
{{% tab title="Resposta" %}}
**O teste é executado em **um intervalo de **round-robin** de 1 minuto de ** Frankfurt, London and Paris**
{{% /tab %}}
{{< /tabs >}}

{{% /exercise %}}

A seguir, vamos examinar a infraestrutura em que nosso aplicativo está sendo executado usando **Splunk Infrastructure Monitoring (IM)**.
