---
title: 2. APM Service View
weight: 2
---
{{% notice title="Visualização de serviço" style="info" %}}

Como proprietários de serviço, você pode usar a visualização de serviço no Splunk APM para obter uma visão completa da integridade do seu serviço em um único painel. A visualização de serviço inclui um indicador de nível de serviço (SLI) para métricas de disponibilidade, dependências, solicitação, erro e duração (RED), métricas de tempo de execução, métricas de infraestrutura, Tag Spotlight, endpoints e logs para um serviço selecionado. Você também pode navegar rapidamente até a criação de perfil de código e de memória para seu serviço na visualização de serviço.

{{% /notice %}}

![Painel de serviço](../images/apm-service-dashboard.png)

{{% notice title="Exercício" style="green" icon="running" %}}

* Na caixa **Time**, altere o intervalo para **-1h**. Observe como os gráficos são atualizados.
* Esses gráficos são muito úteis para identificar rapidamente problemas de desempenho. Você pode usar este painel para ficar de olho na integridade do seu serviço.
* Role a página para baixo e expanda **Infrastructure Metrics**. Aqui você verá as métricas do Host e do Pod.
* **Runtime Metrics** não estão disponíveis porque os dados de criação de perfil não estão disponíveis para serviços escritos em Node.js.
* Agora vamos voltar para a visualização de exploração, você pode clicar no botão Voltar no seu navegador

{{% /notice %}}

![Explorar APM](../images/apm-business-workflow.png)

{{% notice title="Exercício" style="green" icon="running" %}}

{{< tabs >}}
{{% tab title="Pergunta" %}}
**No Service Map, passe o cursor sobre o **wire-transfer-service**. Que conclusão você pode tirar do gráfico pop-up do serviço?**
{{% /tab %}}
{{% tab title="Resposta" %}}
**A porcentagem de erro é muito alta.**
{{% /tab %}}
{{< /tabs >}}
{{% /notice %}}

![Gráfico de serviços APM](../images/apm-service-popup-chart.png)

Precisamos entender se existe um padrão para essa taxa de erro. Temos uma ferramenta útil para isso, **Tag Spotlight**.
