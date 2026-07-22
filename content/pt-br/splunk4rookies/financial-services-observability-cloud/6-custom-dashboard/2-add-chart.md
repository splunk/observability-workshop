---
title: Adicionando gráficos copiados
linkTitle: 2. Adicionando gráficos copiados
weight: 2
hidden: true
---

Nesta seção, usaremos a funcionalidade **Copy and Paste** para estender nosso painel. Lembre-se de que copiamos alguns gráficos durante a seção Painel de serviço do APM, agora iremos adicionar esses gráficos ao nosso painel.

{{% notice title="Exercício" style="green" icon="running" %}}

* Selecione **2+** na parte superior da página e selecione **Paste charts**, isso criará os gráficos em seu painel personalizado.
* O gráfico atualmente mostra dados de todos os **Environments** e **Services**, então vamos adicionar um filtro para nosso ambiente e **paymentservice**.
* Clique nos 3 pontos **...** no canto superior direito do gráfico de valor único **Request Rate**. Isso abrirá o gráfico no modo de edição.
* Na nova tela, clique no **x** no botão {{% button style="blue" %}}sf_environment:* x{{% /button %}} **(1)** no meio da tela para fechá-la.
* Clique em {{% button style="blue" %}}**+**{{% /button %}} para adicionar um novo filtro e selecione **sf_environment**, escolha [WORKSHOPNAME] no menu suspenso e clique em **Apply**. O botão mudará para **sf_environment:[WORKSHOPNAME]**
* Faça o mesmo com o botão {{% button style="blue" %}}sf_service.{{% /button %}} **(2)**, feche-o e crie um novo filtro para **sf_service**. Só que desta vez mude para `paymentservice`.
  ![editar gráfico](../images/edit-chart.png)
* Clique no botão {{% button style="blue" %}}Save and close {{% /button %}} **(3)**.
* Repita as 4 etapas anteriores para o gráfico de texto **Request Rate**
* Clique em {{% button style="blue" %}}Save{{% /button %}} depois de atualizar os dois gráficos.
* Como os novos gráficos colados apareceram na parte inferior do nosso painel, precisamos reorganizar nosso painel novamente.
* Usando as habilidades de arrastar e soltar e redimensionar que você aprendeu anteriormente, faça com que seu painel se pareça com a imagem abaixo.
  ![Nova aparência do painel](../images/copyandpastedcharts.png)
{{% /notice %}}

A seguir, criaremos um gráfico personalizado com base em nosso teste sintético que está em execução.
