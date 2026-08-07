---
title: Exercício de Infraestrutura - Parte 1
linkTitle: Parte 1
weight: 1
time: 5 minutos
---

Esta é a primeira seção do nosso exercício ideal do Kubernetes Navigator. Abaixo estão algumas informações de alto nível sobre o Kubernetes, caso você não esteja familiarizado com ele.

{{% notice title="Terminologia do Kubernetes" style="info" %}}
K8s, abreviação de Kubernetes, é uma plataforma de orquestração de contêineres de código aberto. Ele gerencia a implantação, o dimensionamento e a manutenção de aplicativos em contêineres e o utilizamos neste workshop para hospedar nosso aplicativo de comércio eletrônico

**Alguma terminologia:**

* Um cluster Kubernetes é um grupo de máquinas, chamadas nós, que trabalham juntas para executar aplicativos em contêineres.
* Os nós são servidores individuais ou VMs no cluster. Normalmente, você teria vários nós em um cluster, mas pode ter apenas um nó, assim como neste workshop.
* Pods são as menores unidades implantáveis ​​no Kubernetes, representando um ou mais contêineres que compartilham a mesma rede e armazenamento, permitindo dimensionamento e gerenciamento eficientes de aplicativos
* Os aplicativos são uma coleção de um ou mais pods interagindo entre si para fornecer um serviço.
* Os namespaces ajudam você a manter seus aplicativos organizados e separados dentro do cluster, fornecendo uma separação lógica para diversas equipes ou projetos dentro de um cluster.
* As cargas de trabalho são como uma lista de tarefas e definem quantas instâncias da sua aplicação devem ser executadas, como devem ser criadas e como devem responder às falhas.
{{% /notice %}}

Selecione o bloco **K8s nodes** no painel Bloco, se ainda não tiver feito isso.
(Selecione **Kubernetes** como sua tecnologia). Isso o levará à página do Kubernetes Navigator.

![Kubernetes](../images/im-kubernetes.png)

A captura de tela acima mostra a parte principal do navegador Kubernetes. Ele mostrará todos os clusters e seus nós que enviam métricas para o Splunk Observability Cloud e a primeira linha de gráficos que mostram métricas baseadas em cluster. No workshop, você verá principalmente clusters Kubernetes de nó único.

Antes de nos aprofundarmos, vamos ter certeza de que estamos observando nosso cluster.

{{% notice title="Exercício" style="green" icon="running" %}}

* Primeiro, use a opção ![k8s filter](../images/k8s-add-filter.png?classes=inline) para escolher seu cluster.
* Isso pode ser feito selecionando `k8s.cluster.name` na caixa suspensa de filtro.
* Você pode então começar a digitar o nome do seu cluster (conforme fornecido pelo seu instrutor). O nome também deve aparecer nos valores suspensos. Selecione o seu e certifique-se de que apenas aquele para o seu workshop esteja destacado com um ![marca azul](../images/select-checkmark.png?classes=inline&width=30px).
* Clique no botão {{% button style="blue"  %}} Apply Filter  {{% /button %}} para focar em nosso cluster
* Agora devemos ter um único cluster visível.
{{% /notice %}}

Vamos para a próxima página deste exercício e examinaremos seu cluster em detalhes.
