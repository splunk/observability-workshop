---
title: 4. APM Service Breakdown
weight: 4
---

{{% notice title="Exercício" style="green" icon="running" %}}

* Selecione o **wire-transfer-service** no Service Map.
* No painel direito, clique em {{% button style="grey"  %}}Breakdown{{% /button %}}.
* Selecione `tenant.level` na lista.
* De volta ao Service Map, clique em **gold** (nosso nível de usuário mais valioso).
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

{{% /notice %}}

Agora você verá o **wire-transfer-service** dividido em três serviços: **gold**, **silver** e **bronze**. Cada tenant é dividido em dois serviços, um para cada versão (`v350.10` e `v350.9`).

![Detalhamento do serviço APM](../images/apm-service-breakdown.png)

{{% notice title="Período Tags" style="info" %}}
Usar tags de span para dividir serviços é um recurso muito poderoso. Ele permite ver o desempenho de seus serviços para diferentes clientes, versões, regiões etc. Neste exercício, determinamos que a versão `v350.10` do **wire-transfer-service** está causando problemas para todos os nossos clientes.
{{% /notice %}}

Em seguida, precisamos detalhar um rastreamento para ver o que está acontecendo.
