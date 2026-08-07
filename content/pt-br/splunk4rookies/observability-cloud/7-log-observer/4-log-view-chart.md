---
title: 4. Gráfico de visualização de registro
weight: 4
---

O próximo tipo de gráfico que pode ser usado com logs é o tipo de gráfico **Log View**. Este gráfico nos permitirá ver mensagens de log com base em filtros predefinidos.

Tal como acontece com o gráfico anterior da Linha do Tempo do Log, adicionaremos uma versão deste gráfico ao nosso Painel do Serviço de Saúde do Cliente:

{{% notice title="Informações" style="green" title="Exercício" icon="running" %}}

* Após o exercício anterior, certifique-se de ainda estar em **Log Observer**.
* Os filtros devem ser os mesmos do exercício anterior, com o seletor de tempo definido como **Last 15 minutes** e filtragem em gravidade=erro, `sf_service=paymentservice` e `sf_environment=[WORKSHOPNAME]`.
* Certifique-se de que temos o cabeçalho apenas com os campos que desejamos.
* Clique novamente em **Save** e depois em **Save to Dashboard**.
* Isso fornecerá novamente a caixa de diálogo de criação de gráfico.
* Para o **Nome do gráfico** use **Log View**.
* Desta vez, clique em {{% button style="blue" %}}Select Dashboard{{% /button %}} e procure o painel que você criou no exercício anterior. Você pode começar digitando suas iniciais na caixa de pesquisa **(1)**.
  ![painel de pesquisa](../images/search-dashboard.png)
* Clique no nome do seu painel para destacá-lo **(2)** e clique em {{% button style="blue" %}}OK{{% /button %}} **(3)**.
* Isso o levará de volta à caixa de diálogo de criação de gráfico.
* Certifique-se de que **Log View** esteja selecionado como **Chart Type**.
  ![visualização de registro](../images/log-view.png?classes=left&width=30vw)
* Para ver seu painel, clique em {{% button style="blue" %}}Save and go to dashboard{{% /button %}}.
* O resultado deve ser semelhante ao painel abaixo:
  ![Painel personalizado](../images/log-observer-custom-dashboard.png)
* Como última etapa deste exercício, vamos adicionar seu painel à página da equipe do workshop, o que facilitará sua localização posteriormente no workshop.
* No topo da página, clique no menu vertical de 3 pontos **⋮** no canto superior direito, selecione **Dashboard Group Actions** > **Link para equipes**.
  ![vinculando](../images/linking.png)
* Na seguinte caixa de diálogo **Link para equipes**, encontre a equipe do Workshop que seu instrutor fornecerá para você e clique em {{% button style="blue" %}}Done{{% /button %}}.

{{% /notice %}}

Na próxima sessão, daremos uma olhada no Splunk Synthetics e veremos como podemos automatizar o teste de aplicações baseadas na web.
