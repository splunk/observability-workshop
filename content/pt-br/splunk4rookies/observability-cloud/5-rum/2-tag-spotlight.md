---
title: 2. Tag Spotlight
weight: 2
---

{{% exercise title="Abra o gráfico de latência de eventos personalizados" %}}

* Certifique-se de estar na guia **Custom Workflows** selecionando-a.
* Dê uma olhada no gráfico **Custom Workflow Duration**. As métricas mostradas aqui mostram a latência do aplicativo. As métricas de comparação ao lado mostram a latência em comparação com 1 hora atrás (que está selecionada na barra de filtro superior).

* Clique no link **see all** abaixo do título do gráfico.

{{% /exercise %}}

![Destaque da etiqueta RUM](../images/rum-tag-spotlight.png)

Nesta visualização do painel, são apresentadas todas as tags associadas aos dados RUM. Tags são pares de valores-chave usados ​​para identificar os dados. Neste caso, as tags são geradas automaticamente pela instrumentação OpenTelemetry. As tags são usadas para filtrar os dados e criar gráficos e tabelas. A visualização Tag Spotlight permite detalhar uma sessão do usuário.

{{% exercise title="Filtrar para retardar transações PlaceOrder" %}}

* Altere o prazo para **Last 1 hour**.
* Clique em **Add Filters**, selecione **OS Version**, clique em **!=** e selecione **Synthetics** e **RUMLoadGen** e clique no botão {{% button style="blue" %}}Apply Filter{{% /button %}}.
* Encontre o gráfico **Custom Event Name**, localize **PlaceOrder** na lista, clique nele e selecione **Add to filter**.
* Observe os grandes picos no gráfico na parte superior.
* Clique na guia **User Sessions**.
* Clique duas vezes no título **Duration** para classificar as sessões por duração (a mais longa na parte superior).
* Clique em {{% icon icon="cog" %}} acima da tabela e selecione **Sf Geo City** na lista de colunas adicionais e clique em {{% button style="blue" %}}Save{{% /button %}}

{{% /exercise %}}

Agora temos uma tabela de Sessões de Usuário que é ordenada pela ordem decrescente de maior duração e inclui as cidades de todos os usuários que fizeram compras no site. Poderíamos aplicar mais filtros para restringir ainda mais os dados, por exemplo. Versão do sistema operacional, versão do navegador, etc.

![Destaque da etiqueta RUM](../images/rum-user-sessions.png)
