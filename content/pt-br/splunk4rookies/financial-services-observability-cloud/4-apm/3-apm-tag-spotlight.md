---
title: 3. APM Tag Spotlight
weight: 3
---

{{% notice title="Exercício" style="green" icon="running" %}}

* Para ver as tags do **wire-transfer-service**, clique em **wire-transfer-service** e depois em **Tag Spotlight** no painel de funções à direita (dependendo da resolução da tela, talvez seja necessário rolar para baixo). Quando estiver no **Tag Spotlight**, verifique se a opção **Show tags with no values** está desativada.

{{% /notice %}}

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

Percorra os cartões e familiarize-se com as tags fornecidas pela telemetria do wire-transfer-service.

{{% notice title="Exercício" style="green" icon="running" %}}

{{< tabs >}}
{{% tab title="Pergunta" %}}
**Qual cartão expõe a etiqueta que identifica qual é o problema?**
{{% /tab %}}
{{% tab title="Resposta" %}}
**O cartão *versão*. O número de solicitações em `v350.10` corresponde ao número de erros, ou seja, 100%**
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

Agora que identificamos a versão do **wire-transfer-service** que está causando o problema, vamos buscar mais informações sobre o erro. Pressione o botão Voltar do navegador para retornar ao Service Map.
