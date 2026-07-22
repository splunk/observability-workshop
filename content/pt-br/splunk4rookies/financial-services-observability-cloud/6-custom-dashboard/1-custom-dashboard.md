---
title: Aprimorando o painel
linkTitle: 1. Aprimorando o Painel
weight: 1
---

Como já salvamos alguns gráficos de log úteis em um painel no exercício Log Observer, vamos estender esse painel.

 ![Montado na parede](../images/wall-mount.png)

{{% notice title="Exercício" style="green" icon="running" %}}

* Para voltar ao seu painel com os dois gráficos de log, clique em **Dashboards** no menu principal e você será levado à visualização do painel da equipe. Em **Dashboards**, clique em **Search dashboards** para procurar seu grupo Service Health Dashboard.
* Clique no nome e isso abrirá o painel salvo anteriormente.
  ![log list](../images/log-observer-custom-dashboard.png)
* Mesmo que as informações de registro sejam úteis, serão necessárias mais informações para que façam sentido para nossa equipe, então vamos adicionar um pouco mais de informações
* A primeira etapa é adicionar um gráfico de descrição ao painel. Clique em {{% button style="grey" %}}New text note{{% /button %}} e substitua o texto na nota pelo texto a seguir e, em seguida, clique no botão {{% button style="blue" %}}Save and close{{% /button %}} e nomeie o gráfico como **Instructions**
{{% notice title="Informações para usar com nota de texto" style="grey" %}}

```text

This is a Custom Health Dashboard for the **wire-transfer-service**,  
Please pay attention to any errors in the logs.
For more detail visit [link](https://https://www.splunk.com/en_us/products/observability.html)

```

{{% /notice %}}

* Os gráficos não estão em uma boa ordem, vamos corrigir isso e reorganizar os gráficos para que sejam úteis.
* Mova o mouse sobre a borda superior do gráfico **Instructions**, o ponteiro do mouse mudará para **☩**. Isso permitirá que você arraste o gráfico no painel. Arraste o gráfico **Instructions** para o local superior esquerdo e redimensione-o para 1/3 da página arrastando a borda direita.
* Arraste e adicione o gráfico **Visualização da linha do tempo do log** ao lado do gráfico **Instruction**, redimensione-o para preencher os outros 2/3 da página para ser o gráfico de taxa de erro próximo aos dois gráficos e redimensione-o para preencher a página
* Em seguida, redimensione o gráfico **Linhas de registro** para ter a largura da página e redimensione-o para torná-lo pelo menos duas vezes maior.
* Você deve ter algo semelhante ao painel abaixo:
  ![Painel inicial](../images/initial-dashboard.png)

{{% /notice %}}

Parece ótimo, vamos continuar e adicionar gráficos mais significativos.
