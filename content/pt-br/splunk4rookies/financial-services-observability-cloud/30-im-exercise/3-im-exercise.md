---
title: Exercício de Infraestrutura - Parte 3
linkTitle: Parte 3
weight: 3
time: 10 minutos
---

Vejamos algumas outras partes da UI, como o *Painel de Informações* à direita do navegador ou o *painel Related Content* na parte inferior.

Primeiro, vamos dar uma olhada no *Painel de Informações*. Esse painel fornece informações de alertas e serviços detectados e os metadados relacionados ao objeto que você está vendo.

![painel de informações](../images/k8s-info-pane.png)

Os metadados são enviados junto com as métricas e são muito úteis para identificar tendências na análise de problemas. Um exemplo poderia ser a falha de um pod quando implantado em um sistema operacional específico.

{{% notice title="Exercício" style="green" icon="running" %}}

* Você consegue identificar o sistema operacional e a arquitetura do nó a partir dos metadados?

{{% /notice %}}

Como vimos no exercício anterior, estes campos são muito úteis para filtrar a visualização em gráficos e navegadores até um subconjunto específico de métricas que nos interessam.

Outro recurso da IU é **Related content**.

{{% notice title="Conteúdo relacionado" style="info" %}}

A interface de usuário do Splunk Observability tentará mostrar informações adicionais relacionadas ao que você está olhando ativamente.
Um bom exemplo disso é o Kubernetes Navigator mostrando blocos de conteúdo relacionados no painel de informações para os serviços encontrados em execução neste nó.

{{% /notice %}}

No **Information Pane**, você deverá ver dois blocos para serviços detectados, os dois bancos de dados usados ​​por nosso aplicativo de comércio eletrônico. Vamos usar este **Related Content**.

{{% notice title="Exercício" style="green" icon="running" %}}

* Primeiro, certifique-se de não ter mais um filtro ativo para o namespace de desenvolvimento. (Basta clicar em **x** para removê-lo do Painel de Filtro), pois não há bancos de dados no Namespace de Desenvolvimento.
* Passe o mouse sobre o bloco **Redis** e clique no botão {{% button style="blue" %}}Goto all my Redis instances{{% /button %}}
* A visualização do Navegador deve mudar para a visualização geral das instâncias do Redis.
* Selecione a instância em execução no seu cluster. (Clique no link azul, denominado **redis-[o nome do seu workshop]**, no painel Instâncias do Redis).
* Agora devemos ver apenas as informações da sua instância Redis e também deve haver um **Information Pane**.
* Novamente vemos metadados, mas também vemos que a UI está mostrando nos blocos **Related Content** que este servidor Redis é executado em um contêiner em execução no Kubernetes.
* Vamos verificar isso clicando no bloco **Kubernetes**.
* Devemos estar de volta ao Kubernetes Navigator, no nível do contêiner.
* Confirme se os nomes do nosso cluster e nó estão todos visíveis no topo da página e estamos de volta ao nosso Cluster K8s, onde começamos.

{{% /notice %}}

Isso conclui o tour pelo Splunk Observability Cloud. Vamos dar uma olhada em nosso site de comércio eletrônico e fazer algumas compras.
