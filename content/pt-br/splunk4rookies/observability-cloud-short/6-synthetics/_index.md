---
title: Digital Experience (Synthetics)
linkTitle: 6. Digital Experience (Synthetics)
archetype: chapter
weight: 6
time: 15 minutos
description: Nesta seção, você aprenderá a usar Splunk Synthetics para monitorar o desempenho e a disponibilidade das suas aplicações.
---

{{% notice icon="user" style="orange" title="Persona" %}}

Colocando novamente o chapéu de **SRE**, pediram que você configure o monitoramento do Online Boutique. Você precisa garantir que a aplicação esteja disponível e com bom desempenho 24 horas por dia, 7 dias por semana.

{{% /notice %}}

> [!IMPORTANT]
> Não seria ótimo monitorar nossa aplicação 24/7 e receber um alerta quando houver um problema? É aqui que entra Synthetics. Vamos mostrar um teste simples que roda a cada 1 minuto e verifica o desempenho e a disponibilidade de uma jornada típica de usuário pelo Online Boutique.

{{< webex chat="Bill Grant" date="Hoje • 28/01/2026" seenby="BG" >}}
{{< webex-msg from="RC" name="Robert Castley" time="09:42" color="#ef950d" >}}
Oi, Bill, agora que resolvemos o problema do `paymentservice`, acho que devemos configurar algum monitoramento para garantir que vamos capturar problemas futuros antes que eles impactem nossos clientes.
{{< /webex-msg >}}
{{< webex-msg from="RC" name="Robert Castley" time="09:43" color="#ef950d">}}
Sugiro usarmos Synthetics para configurar um teste que roda a cada minuto e verifica o desempenho e a disponibilidade de uma jornada típica de usuário pelo Online Boutique. Assim, podemos ser alertados imediatamente se houver qualquer problema.
{{< /webex-msg >}}
{{< /webex >}}
