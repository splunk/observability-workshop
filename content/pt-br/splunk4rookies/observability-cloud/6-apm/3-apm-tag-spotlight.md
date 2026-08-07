---
title: 3. APM Tag Spotlight
weight: 3
---

{{% exercise title="Abra Tag Spotlight para serviço de pagamento" %}}

* Para visualizar as tags de **paymentservice**, clique em **paymentservice** e, em seguida, clique em **Tag Spotlight** no painel de funções do lado direito (pode ser necessário rolar para baixo dependendo da resolução da tela).* Uma vez em **Tag Spotlight**, certifique-se de que a alternância **Show tags with no values** esteja desativada.

{{% /exercise %}}

![Destaque da etiqueta APM](../images/apm-tag-spotlight.png)

As visualizações em **Tag Spotlight** são configuráveis ​​tanto para o gráfico quanto para os cartões. A visualização é padronizada como **Requests & Errors**.

Também é possível configurar quais métricas de tags serão exibidas nos cards. É possível selecionar qualquer combinação de:

* Solicitações
* Erros
* Erros de causa raiz
* Latência P50
* Latência P90
* Latência P99

Certifique-se também de que a alternância **Show tags with no values** esteja desmarcada.

{{% exercise title="Encontre a versão ruim no Tag Spotlight" %}}

{{< tabs >}}
{{% tab title="Pergunta" %}}
**Qual cartão expõe a etiqueta que identifica qual é o problema?**
{{% /tab %}}
{{% tab title="Resposta" %}}
**O cartão *versão*. O número de solicitações em `v350.10` corresponde ao número de erros, ou seja, 100%**
{{% /tab %}}
{{< /tabs >}}

{{% /exercise %}}

Agora que identificamos a versão do **paymentservice** que está causando o problema, vamos ver se conseguimos encontrar mais informações sobre o erro. Clique em **← Tag Spotlight** na parte superior da página para voltar ao Service Map.
