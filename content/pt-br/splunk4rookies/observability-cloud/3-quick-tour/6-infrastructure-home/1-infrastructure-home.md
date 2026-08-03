---
title:  Navegadores de infraestrutura
linkTitle: 6.1 Navegadores de Infraestrutura
weight: 2
hidden: true
---

Clique em **Infrastructure** no menu principal, a Home Page da Infraestrutura é composta por 4 seções distintas.

![Infra principal](../images/infrastructure-main.png)

1. **Onboarding Pane:** Vídeos de treinamento e links para documentação para você começar a usar o Splunk Infrastructure Monitoring.
2. **Time & Filter Pane:** Janela de tempo (não configurável no nível superior)
3. **Integrations Pane:** Lista de todas as tecnologias que estão enviando métricas para o Splunk Observability Cloud.
4. **Tile Pane:** Número total de serviços monitorados divididos por integração.

Usando o painel Infraestrutura, podemos selecionar a infraestrutura/tecnologia que nos interessa, vamos fazer isso agora.

{{% exercise title="Explore o navegador Kubernetes" %}}

* Na seção **Containers** no painel Integrações **(3)**, selecione **Kubernetes** como a tecnologia que você deseja examinar.
* Isso deve mostrar dois blocos, **K8s Nodes** e **K8s Workloads**.
* A parte inferior de cada bloco terá um gráfico de histórico e a parte superior mostrará notificações de alertas disparados. Em todos os blocos, essas informações adicionais em cada um dos blocos lhe darão uma boa visão geral da integridade da sua infraestrutura.
* Clique no bloco **K8s Nodes**.
* Serão apresentadas a você uma ou mais representações de um cluster Kubernetes.
* Clique no botão {{% button %}}Add filters{{% /button %}}. Digite `k8s.cluster.name` e clique no resultado da pesquisa.
* Na lista, selecione **[NAME OF WORKSHOP]-k3s-cluster** e clique no botão {{% button style="blue" %}}Apply Filter{{% /button %}}.

  ![cluster](../images/k8s-cluster.png)

* O Kubernetes Navigator usa cores para indicar a integridade. Como você pode ver, há dois pods ou serviços que não estão íntegros e estão em estado de falha **(1)**. O resto está saudável e funcionando. Isso não é incomum em ambientes Kubernetes compartilhados, então replicamos isso para o workshop.
* Observe os blocos ao lado, em **Dependências de nós** **(2)**, especificamente os blocos MySQL e Redis. Estas são as duas bases de dados utilizadas pela nossa aplicação de e-commerce.

{{% /exercise %}}

{{% notice title="Dependências de nó" style="info" %}}

A UI mostrará os serviços que estão em execução no nó selecionado se eles tiverem sido configurados para serem monitorados pelo OpenTelemetry Collector.

{{% /notice %}}

{{% exercise title="Abra o navegador da instância Redis" %}}

* Clique no bloco **Redis** e isso o levará ao navegador **Redis instances**. Em **REDIS INSTANCE** clique em **redis-[NAME OF WORKSHOP]**.
* Isso o levará ao **Redis instance**. Este navegador mostrará gráficos com dados métricos da instância ativa do Redis em nosso site de comércio eletrônico.
  ![redis](../images/redis-2.png)
{{< tabs >}}
{{% tab title="Pergunta" %}}
**Você pode nomear o bloco de dependências da instância nesta visualização?**
{{% /tab %}}
{{% tab title="Resposta" %}}
**Sim, existe um para Kubernetes.**
{{% /tab %}}
{{< /tabs >}}

* Clique no bloco e isso nos levará de volta ao Kubernetes Navigator, desta vez no nível do Pod, mostrando o Pod que executa o serviço Redis.
* Para retornar ao nível Cluster, basta clicar no link **Cluster** **(1)** no topo da tela.

![nó](../images/node-link.png)

{{% /exercise %}}

Isso conclui o tour por **Splunk Observability Cloud**.

Aqui, tome um 💶 virtual e vamos dar uma olhada em nosso site de e-commerce, a 'Online Boutique' e fazer algumas compras.
