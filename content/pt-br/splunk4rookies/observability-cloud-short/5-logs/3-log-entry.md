---
title: 3. Visualizar entradas de log
weight: 3
---

{{% exercise title="Abrir um log de erro" %}}

* Clique em uma entrada de erro na tabela de logs (garanta que ela diga `hostname: "paymentservice-xxxx"`, caso também apareça algum erro raro de outro serviço na lista).
{{< tabs >}}
{{% tab title="Pergunta" %}}
**Com base na mensagem, o que você diria à equipe de desenvolvimento para fazer e resolver o problema?**
{{% /tab %}}
{{% tab title="Resposta" %}}
**A equipe de desenvolvimento precisa reconstruir e implantar o container com um API Token válido ou fazer rollback para `v350.9`**.
{{% /tab %}}
{{< /tabs >}}

  ![Log Message](../images/log-observer-log-message.png)
* Clique no **X** no painel da mensagem de log para fechá-lo.

{{% /exercise %}}

{{% notice style="blue" title="Parabéns" icon="wine-bottle" %}}

Você usou o Splunk Observability Cloud com **sucesso** para entender por que teve uma experiência ruim ao comprar no Online Boutique. Você usou RUM, APM e logs para entender o que aconteceu no seu conjunto de serviços e, em seguida, encontrou a causa subjacente, tudo com base nos 3 pilares da Observabilidade: **métricas**, **traces** e **logs**.

Você também aprendeu a usar a **marcação e análise inteligentes** da Splunk com **Tag Spotlight** para detectar padrões no comportamento das suas aplicações, além do poder de **correlação full stack** do **Related Content** para mover rapidamente entre diferentes componentes mantendo o contexto do problema.

{{% /notice %}}

Na próxima parte do workshop, vamos sair do **modo de descoberta de problemas** e entrar nos modos de **mitigação**, **prevenção** e **melhoria de processo**.
