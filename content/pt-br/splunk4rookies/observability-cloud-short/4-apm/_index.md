---
title: Application Performance Monitoring (APM)
linkTitle: 4. APM
weight: 4
archetype: chapter
time: 20 minutos
description: Nesta seção, usaremos APM para aprofundar a investigação e identificar onde está o problema.
---

{{% notice icon="user" style="orange" title="Persona" %}}

Você é uma pessoa **desenvolvedora back-end** e foi chamada para ajudar a investigar um problema encontrado pela pessoa SRE. A SRE identificou uma experiência ruim para o usuário e pediu que você investigue o problema.

{{% /notice %}}

> [!IMPORTANT]
> RUM é a visão do lado do cliente; APM é a visão do lado do servidor. Seguir um trace de RUM até o trace correspondente em APM mostra visibilidade de ponta a ponta na prática - e é assim que vamos aprofundar a investigação até o problema no back-end.

{{< webex chat="Pieter Hagen" date="Hoje • 28/01/2026" seenby="RC" >}}
{{< webex-msg from="PH" name="Pieter Hagen" time="09:42" color="#571bc0" >}}
Oi Robert, fiz a triagem de um problema de satisfação do cliente no Online Boutique. O RUM mostra tempos ruins de carregamento de página. Segui uma sessão de usuário até o backend usando Related Content - a latência está vindo do **paymentservice**.
{{< /webex-msg >}}

{{< webex-msg from="PH" name="Pieter Hagen" time="09:43" color="#571bc0" >}}
Você consegue investigar o back-end e encontrar a causa raiz? Vou te enviar um link para o trace.
{{< /webex-msg >}}

{{< webex-msg me=true time="09:43" >}}
Estou nisso. Vou verificar o APM e o service map. 👍
{{< /webex-msg >}}
{{< /webex >}}
