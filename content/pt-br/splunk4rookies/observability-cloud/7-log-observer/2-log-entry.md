---
title: 2. Visualizando entradas de registro
weight: 2
---

Antes de olharmos para uma linha de registro específica, vamos recapitular rapidamente o que fizemos até agora e por que estamos aqui com base nos 3 pilares da Observabilidade:

| Métricas | Vestígios | Registros |
|:-------:|:------:|:----:|
| _**Tenho algum problema?**_ | _**Onde está o problema?**_ | _**Qual é o problema?**_ |

* Usando métricas, identificamos **que temos um problema** com nosso aplicativo. Isso ficou óbvio pela taxa de erro nos Painéis de Serviço, pois era maior do que deveria ser.
* Usando rastreamentos e tags span, descobrimos **onde está o problema**. O **paymentservice** é composto por duas versões, `v350.9` e `v350.10`, e a taxa de erro foi **100%** para `v350.10`.
* Vimos que esse erro do **paymentservice** `v350.10` causou várias tentativas e um longo atraso na resposta do checkout da Online Boutique.
* A partir do rastreamento, usando o poder de **Related Content**, chegamos às entradas de log da versão **paymentservice** com falha. Agora, podemos determinar **qual é o problema**.

{{% exercise title="Abra um log de erros" %}}

* Clique em uma entrada de erro na tabela de log (certifique-se de que diz `hostname: "paymentservice-xxxx"` caso haja um erro raro de um serviço diferente na lista também).
{{< tabs >}}
{{% tab title="Pergunta" %}}
**Com base na mensagem, o que você diria à equipe de desenvolvimento para resolver o problema?**
{{% /tab %}}
{{% tab title="Resposta" %}}
**A equipe de desenvolvimento precisa reconstruir e implantar o contêiner com um token de API válido ou reverter para `v350.9`**.
{{% /tab %}}
{{< /tabs >}}

  ![Mensagem de registro](../images/log-observer-log-message.png)
* Clique em **X** no painel de mensagens de log para fechá-lo.

{{% /exercise %}}

{{% notice style="blue" title="Parabéns" icon="wine-bottle" %}}

Você **usou com sucesso** o Splunk Observability Cloud para entender por que teve uma experiência de usuário ruim ao fazer compras na Online Boutique. Você usou RUM, APM e logs para entender o que aconteceu em seu cenário de serviços e, posteriormente, encontrou a causa subjacente, tudo com base nos três pilares de observabilidade, **métricas**, **traces** e **logs**

Você também aprendeu como usar a **marcação e análise inteligente** do Splunk com **Tag Spotlight** para detectar padrões no comportamento de seus aplicativos e usar o poder de **correlação de pilha completa** do **Related Content** para mover-se rapidamente entre os diferentes componentes enquanto se mantém no contexto do problema.

{{% /notice %}}

Na próxima parte do workshop, passaremos do **modo de localização de problemas** para o **modo de mitigação**, **prevenção** e **modo de melhoria de processos**.

A seguir, criando gráficos de log em um painel personalizado.
