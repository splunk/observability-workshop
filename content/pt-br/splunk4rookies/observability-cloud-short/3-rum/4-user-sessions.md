---
title: 4. User Sessions
weight: 4
---

Uma **User Session** no RUM representa a interação completa de um único usuário com sua aplicação web, desde o momento em que ele chega até sair ou ficar inativo. Cada sessão captura uma linha do tempo com todas as visualizações de página, interações do usuário (cliques, rolagens, envios de formulário), requisições de rede, erros e métricas de desempenho.

As sessões são identificadas por um Session ID único e incluem metadados como tipo de navegador, dispositivo, localização geográfica e tags customizadas. Isso permite reproduzir e analisar a experiência exata de um usuário específico, o que é muito valioso para troubleshooting, entendimento do comportamento do usuário e identificação de gargalos de desempenho.

{{% exercise title="Investigar a sessão mais longa" %}}

* Na tabela **User Sessions**, clique no **Session ID** com a maior **Duration** (mais de 15 segundos ou mais). Isso levará você para a visualização RUM Session.
* Observe a duração do span **PlaceOrder**. Esse é o tempo que levou para concluir o pedido. Nada bom!

![RUM Session](../images/rum-waterfall-place-order.png)

* Procure pelo **Fetch** **(1)**, que estará acima ou abaixo do span **PlaceOrder**.
  * Ele será parecido com `POST https://labob...y.com/cart/checkout`.
* Passe o mouse sobre o **APM** azul **(2)**. Depois de alguns segundos, um pop-up aparecerá.
* Você verá que **paymentservice** e **checkoutservice** estão em estado de erro, como na captura de tela acima.
* Em **Workflow Name**, clique em `front-end:/cart/checkout` **(3)**. Isso abrirá o **APM Service Map**. Aqui vamos investigar os serviços de back-end e suas dependências para identificar a causa raiz do problema.

![RUM Session](../images/rum-waterfall.png)

{{% /exercise %}}
