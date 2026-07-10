---
title: 2. APM Service View
weight: 2
---
{{% notice title="Service View" style="info" %}}

Como responsável por um serviço, você pode usar a service view no Splunk APM para obter uma visão completa da saúde do seu serviço em um único painel. A service view inclui um indicador em nível de serviço (SLI) para disponibilidade, dependências, métricas de request, error e duration (RED), métricas de runtime, métricas de infraestrutura, Tag Spotlight, endpoints e logs para um serviço selecionado. Você também pode navegar rapidamente para code profiling e memory profiling do seu serviço a partir da service view.

{{% /notice %}}

{{% exercise title="Ampliar o período para expor erros" %}}

* Confira a caixa **Time**. Você pode ver que os dashboards mostram apenas dados relevantes ao tempo que o trace de APM selecionado anteriormente levou para concluir (observe que os gráficos são estáticos).
* Na caixa **Time**, altere o período para **-1h** **(1)**.

![Service Dashboard](../images/apm-service-dashboard.png)

* Você consegue ver claramente que a **Success rate** não é 100%, porque temos erros em nosso serviço.
* Precisamos entender se existe um padrão nessa taxa de erro. Temos uma ferramenta prática para isso: clique na aba **Tag Spotlight** **(2)**.

{{% /exercise %}}
