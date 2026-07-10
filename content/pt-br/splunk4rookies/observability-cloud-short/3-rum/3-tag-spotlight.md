---
title: 3. Tag Spotlight
weight: 3
---

{{% exercise title="Filtrar para sessões PlaceOrder lentas" %}}

* Este dashboard exibe todas as tags associadas aos dados de RUM, pares chave-valor gerados automaticamente pela instrumentação de RUM. Tags são usadas para filtrar dados e criar gráficos e tabelas. A visualização Tag Spotlight permite aprofundar a análise em sessões individuais de usuários.

![RUM Tag Spotlight](../images/rum-tag-spotlight.png)

* Altere o período para **Last 1 hour** **(1)**.
<!--* Clique em **Add Filters**, selecione **OS Version**, clique em **!=**, selecione **Synthetics** e **RUM.LoadGen** e então clique no botão {{% button style="blue" %}}Apply Filter{{% /button %}} **(2)**.-->
* Encontre o gráfico **Operation**, localize **PlaceOrder** na lista, clique nele e selecione **Add to filter** **(2)**.
* Clique na aba **User Sessions** **(3)**.
* Clique duas vezes no cabeçalho **Duration** para ordenar as sessões por duração (as mais longas no topo) **(4)**.

* Agora temos uma tabela de User Sessions ordenada pela maior duração (decrescente), mostrando usuários que estiveram comprando no site. Poderíamos aplicar mais filtros para refinar ainda mais os dados, por exemplo versão do sistema operacional, versão do navegador etc.

![RUM Tag Spotlight](../images/rum-user-sessions.png)

{{% /exercise %}}
