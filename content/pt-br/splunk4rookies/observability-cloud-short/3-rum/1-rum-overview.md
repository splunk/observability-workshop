---
title: Visão geral do RUM
linkTitle: 1. Visão geral do RUM
weight: 1
time: 5 minutos
---

{{% exercise title="Filtrar para sua loja" %}}

* No Splunk Observability Cloud, no menu principal, passe o mouse sobre **Digital Experience** e clique em **Overview** **(1)** na seção **Real User Monitoring**, como mostrado abaixo.

![RUM](../images/rum-de.png)

* Isso abrirá o **Application Summary Dashboard**. Esta seção mostra uma visão rápida de **todas** as aplicações monitoradas.

* O dashboard Real User Monitoring (RUM) Overview no Splunk Observability Cloud oferece visibilidade sobre como usuários reais experimentam suas aplicações web. Ele captura métricas de desempenho do navegador, erros de JavaScript e falhas em requisições de rede conforme ocorrem em sessões reais de usuários. O dashboard destaca Core Web Vitals (LCP, INP, CLS) para medir o desempenho de carregamento das páginas, exibe tendências de erro ao longo do tempo e mostra alertas recentes, dando às equipes de front-end os insights necessários para identificar e corrigir problemas que afetam a experiência do usuário final.

* Para garantir que estamos vendo os dados corretos, confira as seguintes configurações **(2)**:
  * O **Time frame** está definido como **-15m**.
  * O **Environment** selecionado é **[NAME OF WORKSHOP]-workshop**.
  * O **App** selecionado é **[NAME OF WORKSHOP]-store**.
  * O **Source** está definido como **Browser**.
* Em seguida, clique em **[NAME OF WORKSHOP]-store** **(3)** acima do gráfico **Page Views / JavaScript Errors**.

![main page](../images/rum-dashboard.png)

{{% /exercise %}}
