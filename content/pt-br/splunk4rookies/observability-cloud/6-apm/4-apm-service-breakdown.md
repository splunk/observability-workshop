---
title: 4. APM Service Breakdown
weight: 4
---

{{% exercise title="Dividir por nível de inquilino" %}}

* Selecione **paymentservice** no Mapa de serviços.
* No painel direito, clique em {{% button style="grey"  %}}Breakdown{{% /button %}}.
* Selecione `tenant.level` na lista.
* De volta ao Service Map, clique em **ouro**.
* Clique em {{% button style="grey"  %}}Breakdown{{% /button %}} e selecione `version`, esta é a tag que expõe a versão do serviço.
* Repita isso para **prata** e **bronze**.
{{< tabs >}}
{{% tab title="Pergunta" %}}
**O que você pode concluir do que está vendo?**
{{% /tab %}}
{{% tab title="Resposta" %}}
**Cada `tenant.level` está sendo impactado por `v350.10`**
{{% /tab %}}
{{< /tabs >}}

{{% /exercise %}}

Agora você verá o **paymentservice** dividido em três serviços, **ouro**, **prata** e **bronze**. Cada locatário é dividido em dois serviços, um para cada versão (`v350.10` e `v350.9`).

![Detalhamento do serviço APM](../images/apm-service-breakdown.png)

{{% notice title="Período Tags" style="info" %}}
Usar tags span para dividir serviços é um recurso muito poderoso. Ele permite que você veja o desempenho de seus serviços para diferentes clientes, diferentes versões, diferentes regiões, etc. Neste exercício, determinamos que `v350.10` do **paymentservice** está causando problemas para todos os nossos clientes.
{{% /notice %}}

Em seguida, precisamos detalhar um rastreamento para ver o que está acontecendo.
