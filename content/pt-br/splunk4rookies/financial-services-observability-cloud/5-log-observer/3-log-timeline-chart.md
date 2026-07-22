---
title: 3. Gráfico de linha do tempo de registro
weight: 3
---

Depois de ter uma visualização específica no Log Observer, é muito útil poder usar essa visualização em um dashboard, para ajudar no futuro a reduzir o tempo de detecção ou resolução de problemas. Como parte do workshop, criaremos um exemplo de painel personalizado que usará esses gráficos.

Vejamos como criar um gráfico **Log Timeline**. O gráfico Log Timeline é usado para visualizar mensagens de log ao longo do tempo. É uma ótima maneira de ver a frequência das mensagens de log e identificar padrões. Também é uma ótima maneira de ver a distribuição de mensagens de log em seu ambiente. Esses gráficos podem ser salvos em um painel personalizado.

{{% notice title="Informações" style="green" title="Exercício" icon="running" %}}

Primeiro, reduziremos a quantidade de informações apenas para as colunas que nos interessam:

* Clique no ícone Configurar tabela {{% icon icon="cog" %}} acima de **Tabela de registros** para abrir **Table Settings**, desmarque `_raw` e certifique-se de que os seguintes campos estejam selecionados `k8s.pod.name`, `message` e `version`.
  ![Configurações da tabela de registros](../images/log-observer-table.png)
* Remova o horário fixo do seletor de horário e defina-o como **Last 15 minutes**.
* Para que isso funcione em todos os traces, remova `trace_id` do filtro e adicione os campos `sf_service=wire-transfer-service` e `sf_environment=[WORKSHOPNAME]`.
* Clique em **Save** e selecione **Save to Dashboard**.
  ![salve](../images/save-query.png)
* Na caixa de diálogo de criação de gráfico exibida, para **Nome do gráfico** use `Log Timeline`.
* Clique em {{% button style="blue" %}}Select Dashboard{{% /button %}} e depois clique em {{% button style="blue" %}}New dashboard{{% /button %}} na caixa de diálogo Seleção de painel.
* Na caixa de diálogo **New dashboard**, insira um nome para o novo painel (não é necessário inserir uma descrição). Use o seguinte formato: `Initials - Service Health Dashboard` e clique em {{% button style="blue" %}}Save{{% /button %}}
* Certifique-se de que o novo painel esteja destacado na lista **(1)** e clique em {{% button style="blue" %}}OK{{% /button %}} **(2)**.
  ![Salvar painel](../images/dashboard-save.png)
* Certifique-se de que **Log Timeline** esteja selecionado como **Chart Type**.
  ![linha do tempo do registro](../images/log-timeline.png?classes=left&width=25vw)
* Clique no botão {{% button %}}Save{{% /button %}} (**não** clique em **Save and goto dashboard** neste momento).

{{% /notice %}}

A seguir, criaremos um gráfico **Log View**.
