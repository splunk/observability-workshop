---
title: 2. Visualização da aplicação
weight: 2
---

{{% exercise title="Explorar o dashboard de RUM" %}}

* Agora você verá uma visualização de dashboard que detalha as métricas por **UX Metrics**, **Front-end Health**, **Back-end Health**, **Custom Events**, **Network Requests**, **Pages** e uma **Map View**, comparando tudo com métricas históricas (1 hora por padrão).

![RUM Dashboard](../images/rum-metric-map-charts.png)

* As abas disponíveis nesta página incluem:
  * **UX Metrics** Métricas de Page Views, Page Load e Web Vitals
  * **Front-end Health** Detalhamento de JavaScript Errors e duração/contagem de Long Tasks
  * **Back-end Health** Network Errors, Requests e Time to First Byte
  * **Custom Events** Métricas RED (Rate, Error e Duration) para eventos customizados
  * **Network Requests** Agrupamento de URLs de rede e métricas principais
  * **Pages** Agrupamento de URLs, métricas principais e Web Vitals
  * **Map View** Requisições geográficas por localização

* Clique em cada uma das abas e examine os dados.

{{< tabs >}}
{{% tab title="Perguntas" %}}

1. Ao examinar os gráficos na aba **Custom Events**, qual gráfico mostra claramente os picos de latência?
2. Na aba **Map View**, de onde vem o maior volume de requisições?

{{% /tab %}}
{{% tab title="Respostas" %}}

1. **Custom Event Latency P75**
2. **Ireland**

{{% /tab %}}
{{< /tabs >}}

* Garanta que você esteja na aba **Custom Events**.
* Para identificar sessões de usuário problemáticas, vamos usar os picos de latência no gráfico **Custom Event Latency P75**.
* No gráfico **Custom Event Latency**, clique no link **see all** **(1)** abaixo do título do gráfico.

![RUM See All](../images/rum-see-all.png)

{{% /exercise %}}
