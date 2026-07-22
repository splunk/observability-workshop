---
title: Exercício de Infraestrutura - Parte 2
linkTitle: Parte 2
weight: 2
time: 10 minutos
---

Esta é a Parte 2 do exercício de Monitoramento de Infraestrutura. Agora você deve ter um único cluster visível.

![Cluster Alt](../images/k8s-cluster.png)

* No Kubernetes Navigator, o cluster é representado pelo quadrado com a linha preta ao seu redor.
* Ele conterá um ou mais quadrados azuis representando o(s) nó(s) ou mecanismos de computação.
* Cada um deles contendo uma ou mais caixas coloridas que representam Pods. (é aqui que seus serviços são executados).
* E como você pode imaginar, **verde** significa saudável e **vermelho** significa que há um problema.

Dado que existem duas caixas ou blocos vermelhos, vamos ver o que está acontecendo e se isso afetará nosso site de Online Boutique.

{{% notice title="Exercício" style="green" icon="running" %}}

* Primeiro, defina a janela de tempo com a qual estamos trabalhando para os últimos 15 minutos. Você faz isso alterando o seletor de Tempo no painel de filtro de **-4h** para **Last 15 minutes**.
* Passe o mouse sobre o cluster, o nó e os pods, ambos **verdes** e **vermelhos**.
* O painel de informações resultante que aparece informará o estado do objeto. Observe que os pods **vermelhos** mostram que estão em **Pod Phase: Failed**. Isso significa que eles travaram e não estão funcionando.
* Examine os gráficos de métricas de cluster que fornecem informações sobre seu cluster. (Os gráficos abaixo da imagem do cluster). Eles fornecem informações gerais sobre a integridade do seu cluster, como consumo de memória e número de pods por nó.
* Nada sinaliza para os pods **vermelhos**, pois os pods travados não afetam o desempenho do Kubernetes.
* Vamos verificar se o Spunk Kubernetes Analyzer pode nos dizer algo mais útil, então clique em **K8s Analyzer**.
{{% notice title="Analisador Spunk Kubernetes" style="info" %}}

O Splunk Kubernetes Analyzer é um processo inteligente executado em segundo plano no Splunk Observability Cloud e foi projetado para detectar relações entre anomalias.

{{% /notice %}}

* O **K8s Analyzer** deveria ter detectado que os dois pods **vermelhos** são semelhantes, indicados pelo 2 após cada linha, e rodando no mesmo Namespace.
* Na visualização do analisador K8s você consegue encontrar qual namespace? (dica, procure `k8s.namespace.name`).
* Em seguida, queremos verificar isso também no nível do nó, então faça uma busca detalhada no nó, primeiro passando o mouse sobre o cluster até ver uma linha azul aparecer ao redor do nó com um ![triângulo azul](../images/node-blue-traingle.png?classes=inline) no canto superior esquerdo, dentro da linha preta do cluster.
* Clique no triângulo. Sua visualização agora deve mostrar pequenas caixas em cada pod, que representam os contêineres que executam o código real. O *K8s Analyzer* deve confirmar que esse problema também está ocorrendo no nível do nó.

![Resultado do analisador](../images/k8s-analyser-result.png?width=20vw)

* Clique em **K8s node**. Isso mostrará as métricas do nó e, se você examinar os gráficos, poderá ver que há apenas dois pods no namespace de desenvolvimento.
* É mais fácil ver se você filtra `k8s.namespace.name=development` no Painel de Filtro. O gráfico **# Total Pods** mostra apenas dois pods e no gráfico **Node Workload** há apenas o *test-job* e ele falhou.

{{% notice title="Analisador Spunk Kubernetes" style="info" %}}

O cenário acima é comum em um ambiente Kubernetes compartilhado, onde as equipes implantam aplicações em diferentes estágios. O Kubernetes foi projetado para manter esses ambientes completamente separados.

{{% /notice %}}

{{% /notice %}}

Nenhum dos pods que compõem nosso site Online Boutique é executado no namespace de desenvolvimento e todos os outros pods são verdes. Podemos assumir com segurança que esses pods não nos afetam, então vamos examinar mais algumas coisas.
