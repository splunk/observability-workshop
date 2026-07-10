---
title: Logs
linkTitle: 5. Logs
weight: 5
archetype: chapter
time: 20 minutos
description: Nesta seção, usaremos Log Observer para aprofundar a investigação e identificar qual é o problema.
---

{{% notice icon="user" style="orange" title="Persona" %}}

Permanecendo no papel de **desenvolvedor back-end**, você precisa inspecionar os logs da aplicação para determinar a causa raiz do problema.

{{% /notice %}}

> [!IMPORTANT]
> Usando o conteúdo relacionado ao trace de **APM** (logs), agora vamos usar **Logs** para aprofundar a investigação e entender exatamente qual é o problema. Related Content é um recurso poderoso que permite saltar de um componente para outro e está disponível para **métricas**, **traces** e **logs**.

{{< webex chat="Robert Castley" date="Hoje • 28/01/2026" seenby="PH" >}}
{{< webex-msg from="RC" name="Robert Castley" time="09:42" color="#ef950d" >}}
Verifiquei o APM e confirmei que o problema está no paymentservice. Há um pico significativo de latência nos traces.
{{< /webex-msg >}}
{{< webex-msg from="RC" name="Robert Castley" time="09:43" color="#ef950d">}}
Vou usar Related Content para ir aos logs e ver se encontro erros ou anomalias que expliquem esse pico de latência.
{{< /webex-msg >}}
{{< /webex >}}
