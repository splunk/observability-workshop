---
title: 4. User Sessions
weight: 4
---
{{% exercise title="Encontre o ponto de partida do APM" %}}

* Feche o RUM Session Replay clicando em **X** no canto superior direito.
* Observe a duração do vão, esse é o tempo que levou para concluir o pedido, não é bom!
* Role a página para baixo e você verá os metadados **Tags** (que são usados ​​no Tag Spotlight). Após as tags, chegamos à cascata que mostra os objetos da página que foram carregados (HTML, CSS, imagens, JavaScript etc.)
* Continue rolando a página até chegar a um link azul **APM** (aquele com `/cart/checkout` no final do URL) e passe o mouse sobre ele.

{{% /exercise %}}

![Sessão RUM](../images/rum-waterfall.png)

Isso abre o Resumo de desempenho do APM. Ter essa visualização ponta a ponta (RUM para APM) é muito útil na solução de problemas.

{{% exercise title="Salte de RUM para APM" %}}

* Você verá que **paymentservice** e **checkoutservice** estão em estado de erro conforme a imagem acima.
* Em **Workflow Name**, clique em `front-end:/cart/checkout`, isso exibirá **APM Service Map**.

{{% /exercise %}}

![RUM para APM](../images/rum-to-apm.png)
