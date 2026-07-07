---
title: 4. APM Service Breakdown
weight: 4
---

{{% exercise title="Detalhar o serviço por versão" %}}

* Selecione o **paymentservice** no Service Map.
* No painel à direita, clique em {{% button style="grey"  %}}Breakdown{{% /button %}}.
* Selecione `version` na lista.
{{< tabs >}}
{{% tab title="Pergunta" %}}
**O que você pode concluir a partir do que está vendo?**
{{% /tab %}}
{{% tab title="Resposta" %}}
**Não há erros para `v350.9`, mas `v350.10` claramente tem um problema.**
{{% /tab %}}
{{< /tabs >}}

![APM Service Breakdown](../images/apm-service-breakdown.png)

{{% notice title="Span Tags" style="info" %}}
Usar span tags para detalhar serviços é um recurso muito poderoso. Ele permite ver como seus serviços se comportam para diferentes clientes, versões, regiões etc. Neste exercício, determinamos que a versão `v350.10` do **paymentservice** está causando problemas.
{{% /notice %}}

* Agora precisamos aprofundar em um trace para ver o que está acontecendo. Clique no círculo vermelho de `v350.10` **(1)** no **paymentservice** e depois clique na aba **Traces** **(2)** no painel à direita.

{{% /exercise %}}
