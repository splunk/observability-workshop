---
title: 3. APM Tag Spotlight
weight: 3
---

{{% exercise title="Encontrar a versão ruim no Tag Spotlight" %}}

* Ao entrar em **Tag Spotlight**, garanta que o toggle **Show tags with no values** esteja desligado.

![APM Tag Spotlight](../images/apm-tag-spotlight.png)

* Esta visualização exibe uma série de cards, cada um representando uma tag indexada (como Endpoint, Environment, Version ou tags customizadas como tenant.level). Dentro de cada card, você vê a distribuição dos valores da tag junto com métricas principais, incluindo contagem de requisições, contagem de erros, erros de causa raiz e percentis de latência (P50, P90, P99).

{{< tabs >}}
{{% tab title="Pergunta" %}}
**Qual card expõe a tag que identifica qual é o problema?**
{{% /tab %}}
{{% tab title="Resposta" %}}
**O card *version*. O número de requisições contra `v350.10` corresponde ao número de erros, ou seja, 100%.**
{{% /tab %}}
{{< /tabs >}}

* Agora que identificamos a tag que indica o problema, vamos ver se conseguimos encontrar mais informações sobre o erro.
* Clique no link **APM** acima de **paymentservice** no topo da página para voltar para o **APM Overview**.
* Em **APM Overview**, clique em **Service Map** no painel à direita.
{{% /exercise %}}
