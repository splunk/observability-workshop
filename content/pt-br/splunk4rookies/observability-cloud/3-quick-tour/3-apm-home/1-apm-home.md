---
title: Application Performance Monitoring Home Page
linkTitle: 3.1 APM Home Page
weight: 2
---

Clique em **APM** no menu principal e selecione **Overview**. A página inicial do APM é composta por 3 seções distintas:

![página APM](../images/apm-main.png)

1. **Onboarding Pane Pane:** Vídeos de treinamento e links para documentação para você começar a usar o Splunk APM.
2. **APM Overview Pane:** Métricas em tempo real para os principais serviços e principais fluxos de trabalho de negócios.
3. **Functions Pane:** Links para análise mais profunda de seus serviços, tags, rastreamentos, desempenho de consulta de banco de dados e criação de perfil de código.

O painel **APM Overview** fornece uma visão de alto nível da integridade do seu aplicativo. Inclui um resumo dos serviços, latência e erros em seu aplicativo. Também inclui uma lista dos principais serviços por taxa de erro e dos principais fluxos de trabalho de negócios por taxa de erro (um fluxo de trabalho de negócios é a jornada do início ao fim da coleção de traces associados a uma determinada atividade ou transação e permite o monitoramento de KPIs de ponta a ponta e a identificação de causas raízes e gargalos).

{{% notice title="Sobre ambientes" style="info" %}}

Para diferenciar facilmente entre vários aplicativos, o Splunk usa **ambientes**. A convenção de nomenclatura para ambientes de workshop é **[NAME OF WORKSHOP]-workshop**. Seu instrutor fornecerá a você o correto para selecionar.

{{% /notice %}}

{{% exercise title="Filtre APM para sua workshop" %}}

* Verifique se a janela de tempo com a qual estamos trabalhando está definida para os últimos 15 minutos (**-15m**).
* Mude o ambiente para o do workshop selecionando seu nome na caixa suspensa e certifique-se de que seja o único selecionado.
{{< tabs >}}
{{% tab title="Pergunta" %}}
**O que você pode concluir do gráfico *Principais serviços por taxa de erro*?**
{{% /tab %}}
{{% tab title="Resposta" %}}
**O *paymentservice* tem uma alta taxa de erro**
{{% /tab %}}
{{< /tabs >}}
<!--
* Clique no bloco Explorar no painel de funções. Isso nos levará ao mapa gerado automaticamente de nossos serviços. Este mapa mostra como os serviços interagem entre si com base nos dados de rastreamento enviados ao Splunk Observability Cloud.
-->
{{% /exercise %}}

Se você rolar para baixo na página de visão geral, notará que alguns serviços listados têm **Inferred Service** próximos a eles.

O Splunk APM pode inferir a presença do serviço remoto, ou serviço inferido se o intervalo que chama o serviço remoto tiver as informações necessárias. Exemplos de possíveis serviços inferidos incluem bancos de dados, terminais HTTP e filas de mensagens. Os serviços inferidos não são instrumentados, mas são exibidos no Service Map e na lista de serviços.

A seguir, vamos verificar **Splunk Log Observer (LO)**.
