---
title: 2. Visualizando entradas de registro
weight: 2
---

Antes de olharmos para uma linha de registro específica, vamos recapitular rapidamente o que fizemos até agora e por que estamos aqui com base nos 3 pilares da Observabilidade:

| Métricas | Vestígios | Registros |
|:-------:|:------:|:----:|
| _**Tenho algum problema?**_ | _**Onde está o problema?**_ | _**Qual é o problema?**_ |

* Usando métricas, identificamos **que temos um problema** com nosso aplicativo. Isso ficou óbvio pela taxa de erro nos Painéis de Serviço, pois era maior do que deveria ser.
* Usando traces e tags de span, descobrimos **onde está o problema**. O **wire-transfer-service** tem duas versões, `v350.9` e `v350.10`, e a taxa de erros foi de **100%** na versão `v350.10`.
* Vimos que esse erro no **wire-transfer-service** `v350.10` causou várias tentativas e um longo atraso na resposta do serviço de verificação de conformidade.
* A partir do trace, usando o poder do **Related Content**, chegamos às entradas de log da versão com falha do **wire-transfer-service**. Agora podemos determinar **qual é o problema**.

{{% notice title="Exercício" style="green" icon="running" %}}

* Clique em uma entrada de erro na tabela de logs (confirme que ela mostra `hostname: "wire-transfer-service-xxxx"`, pois pode haver na lista algum erro raro de outro serviço).
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

{{% /notice %}}

{{% notice style="blue" title="Parabéns" icon="wine-bottle" %}}

Você usou o Splunk Observability Cloud com **sucesso** para entender por que os usuários estão enfrentando problemas ao utilizar o serviço de transferência bancária. Você usou o Splunk APM e o Splunk Log Observer para compreender o que aconteceu no ambiente de serviços e, em seguida, encontrou a causa subjacente, tudo com base nos três pilares da observabilidade: **métricas**, **traces** e **logs**.

Você também aprendeu a usar a **análise e marcação inteligentes** do Splunk com o **Tag Spotlight** para detectar padrões no comportamento de suas aplicações e a aproveitar o poder de **correlação de todo o stack** do **Related Content** para navegar rapidamente entre diferentes componentes e tipos de telemetria sem perder o contexto do problema.

{{% /notice %}}

Na próxima parte do workshop, passaremos do **modo de localização de problemas** para o **modo de mitigação**, **prevenção** e **modo de melhoria de processos**.

A seguir, criando gráficos de log em um painel personalizado.
