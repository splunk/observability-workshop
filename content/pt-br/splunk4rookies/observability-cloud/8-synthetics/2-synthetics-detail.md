---
title: 2. Detalhe do teste de Synthetics
weight: 2
---

No momento, estamos analisando o resultado de um único teste de navegador sintético. Este teste é dividido em **Business Transactions**. Pense nele como um grupo de uma ou mais interações relacionadas logicamente que representam um fluxo de usuário crítico para os negócios.

{{% notice title="Informações" style="info" %}}

A captura de tela abaixo não contém um banner vermelho com um erro, mas você pode ver um nos resultados da execução. Isto é esperado, pois em alguns casos o teste falha e não afeta o workshop.

{{% /notice %}}

![cachoeira](../images/synth-waterfall.png)

1. **Filter:** Concentre-se em partes específicas do seu teste; filtra a tira de filme, o vídeo e a cascata.
2. **Filmstrip:** Oferece um conjunto de capturas de tela do desempenho do site para que você possa ver como a página responde em tempo real.
3. **Gráfico em cascata:** O gráfico em cascata é uma representação visual da interação entre o executor de teste e o site que está sendo testado.
4. **Video:** Isso permite que você veja exatamente o que um usuário que tentasse carregar seu site a partir do local e do dispositivo de uma execução de teste específica experimentaria.
5. **Métricas de teste do navegador:** uma visualização que oferece uma imagem do desempenho do site.

Por padrão, o Splunk Synthetics fornece capturas de tela e captura de vídeo do teste. Isso é útil para depurar problemas. Você pode ver, por exemplo, o carregamento lento de imagens grandes, a renderização lenta de uma página etc.

{{% exercise title="Inspecione a reprodução de teste" %}}

* Use o mouse para rolar para a esquerda e para a direita na tira de filme para ver como o site estava sendo renderizado durante a execução do teste.
* No painel Vídeo, pressione o botão de reprodução **▶** para ver a reprodução de teste. Se você clicar nos três pontos verticais **⋮** você pode alterar a *velocidade de reprodução*, visualizá-la *Picture in Picture* e até mesmo *Baixar* o vídeo.
* Usando o filtro acima da película, no cabeçalho *Synthetic Transactions*, clique em **Home**
* A cascata abaixo mostrará todos os objetos que compõem a página. A primeira linha é a própria página HTML. As próximas linhas são os objetos que compõem a página (HTML, CSS, JavaScript, Imagens, Fontes, etc.).
* Na cascata encontre a linha **GET** *splunk-otel-web.js*.
* Clique no botão **>** para abrir a seção de metadados e ver as informações do cabeçalho de solicitação/resposta.
* No filtro, alterne para a segunda transação sintética **Shop**. Observe que a película e o vídeo se ajustam e passam para o início da nova transação.
* Repita isso para todas as outras transações e, finalmente, selecione a transação **PlaceOrder**.

{{% /exercise %}}
