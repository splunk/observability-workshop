---
title: Log Observer Home Page
linkTitle: 4.1 Log Observer Home Page
weight: 2
---

Clique em **Logs** no menu principal e depois em **Log Observer**. A página inicial do Log Observer é composta por 4 seções distintas:

![Página Baixa](../images/log-observer-main.png)

1. **Onboarding Pane:** Vídeos de treinamento e links para documentação para você começar a usar o Splunk Log Observer.
2. **Filter Bar:** Filtre por hora, índices e campos e também salve consultas.
3. **Logs Table Pane:** Lista de entradas de log que correspondem aos critérios de filtro atuais.
4. **Fields Pane:** Lista de campos disponíveis no índice atualmente selecionado.

{{% notice title="Índices Splunk" style="info" %}}

Geralmente, no Splunk, um “índice” refere-se a um local designado onde seus dados são armazenados. É como uma pasta ou contêiner para seus dados. Os dados dentro de um índice do Splunk são organizados e estruturados de uma forma que facilita a pesquisa e a análise. Diferentes índices podem ser criados para armazenar tipos específicos de dados. Por exemplo, você pode ter um índice para logs de servidores web, outro para logs de aplicativos e assim por diante.

{{% /notice %}}

{{% notice title="Dica" style="primary" icon="lightbulb" %}}

Se você já usou o Splunk Enterprise ou o Splunk Cloud antes, provavelmente está acostumado a iniciar investigações com logs. Como você verá no exercício a seguir, você também pode fazer isso com o Splunk Observability Cloud. Este workshop, no entanto, utilizará todos os sinais **OpenTelemetry** para investigações.

{{% /notice %}}

Vamos fazer um pequeno exercício de pesquisa:

{{% exercise title="Filtrar Log Observer para transações Visa" %}}

* Defina o período como **-15m**.
* Clique em {{% button style="gray" %}}Add Filter{{% /button %}} na barra de filtro e clique em **Fields** na caixa de diálogo.
* Digite **cardType** e selecione-o.
* Em **Valores principais** clique em **visto** e, em seguida, clique em **=** para adicioná-lo ao filtro.
* Clique em {{% button style="blue" %}}Run search{{% /button %}}

  ![pesquisa de logotipo](../images/log-filter-bar.png?width=920px)

* Clique em uma das entradas de log na tabela Logs para validar se a entrada contém `cardType: "visa"`.
* Vamos encontrar todos os pedidos que foram enviados. Clique em **Clear All** na barra de filtro para remover o filtro anterior.
* Clique novamente em {{% button style="gray" %}}Add Filter{{% /button %}} na barra de filtros e selecione **Keyword**. Em seguida, basta digitar `order` na caixa **Enter Keyword...** e pressionar Enter.
* Clique em {{% button style="blue" %}}Run search{{% /button %}}
* Agora você deve ter apenas linhas de log que contenham a palavra `order`. Ainda há muitas linhas de log, então vamos filtrar mais algumas.
* Adicione outro filtro, desta vez selecione a caixa **Fields** e digite `severity` na caixa de pesquisa **Encontrar um campo ...** e selecione-o.
  ![gravidade](../images/find-severity.png?width=15vw&classes=left)
* Em **Valores principais** clique em **erro** e, a seguir, clique em **=** para adicioná-lo ao filtro.
* Clique em {{% button style="blue" %}}Run search{{% /button %}}
* Agora você deve ter uma lista de pedidos que não foram concluídos nos últimos 15 minutos.

{{% /exercise %}}

A seguir, vamos verificar **Splunk Synthetics**.
