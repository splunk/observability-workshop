---
title: 1. RUM Dashboard
weight: 1
---

Clique em **Digital Experience** e, em Real User Monitoring, clique em **Overview** no menu principal. Você chega à RUM Home Page; essa visualização já foi abordada na breve introdução anterior.

![vários aplicativos](../images/rum-dashboard.png)

{{% exercise title="Filtre RUM para sua workshop" %}}

* Certifique-se de selecionar sua workshop garantindo que os menus suspensos estejam definidos/selecionados da seguinte forma:
  * O **Time frame** está configurado como **-15m**.
  * O **Environment** selecionado é **[NAME OF WORKSHOP]-workshop**.
  * O **App** selecionado é **[NAME OF WORKSHOP]-store**.
  * O **Source** está configurado como **All**.
* Em seguida, clique em **[NAME OF WORKSHOP]-store** acima do gráfico **Page Views / JavaScript Errors**.
* Isso abrirá uma nova visualização do painel detalhando as métricas por **UX Metrics**, **Front-end Health**, **Back-end Health** e **Custom Workflows** e comparando-as com métricas históricas (1 hora por padrão).

{{% /exercise %}}

![Painel RUM](../images/rum-metrics-dashboard.png)

* **UX Metrics:** métricas de visualizações de página, carregamento de página e Web Vitals.
* **Front-end Health:** Detalhamento de erros de Javascript e longa duração e contagem de tarefas.
* **Back-end Health:** Erros e solicitações de rede e tempo até o primeiro byte.
* Métricas **Custom Workflows:** RED (taxa, erro e duração) para eventos personalizados.

{{% exercise title="Explore as guias RUM" %}}

* Clique em cada uma das guias (**UX Metrics**, **Front-end Health**, **Back-end Health** e **Custom Workflows**) e examine os dados.

{{< tabs >}}
{{% tab title="Pergunta" %}}
**Se você examinar os gráficos na guia *Fluxos de trabalho personalizados*, **qual gráfico **mostra** claramente os** picos de latência?**
{{% /tab %}}
{{% tab title="Resposta" %}}
**É o gráfico *Duração do fluxo de trabalho personalizado***
{{% /tab %}}
{{< /tabs >}}

{{% /exercise %}}
