---
title: 5. RUM para APM
weight: 5
---

{{% exercise title="Localizar o serviço com falha" %}}

* No **APM Service Map**, você consegue ver claramente que há um problema com o `paymentservice`.

![RUM to APM](../images/rum-to-apm.png)

{{% /exercise %}}

Agora navegamos com sucesso de **RUM** para **APM**, obtendo uma visão de ponta a ponta da experiência do usuário. Essa integração permite rastrear problemas de desempenho desde o front-end até os serviços de back-end, tornando o troubleshooting e a otimização mais eficazes.

As métricas de RUM inicialmente apontaram o Checkout Service como a origem do problema. Sem **APM**, as equipes poderiam perder tempo investigando esse serviço sem necessidade. Com **APM**, porém, conseguimos identificar rapidamente que a causa raiz está no `paymentservice`, economizando tempo e reduzindo significativamente o MTTx.

Vamos pedir aos nossos amigos de desenvolvimento back-end que continuem a investigação.
