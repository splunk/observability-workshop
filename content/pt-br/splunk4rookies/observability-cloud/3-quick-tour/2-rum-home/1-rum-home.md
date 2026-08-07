---
title: Real User Monitoring Home Page
linkTitle: 2.1 RUM Home Page
weight: 2
---

Clique em **Digital Experience** e, em Real User Monitoring, clique em **Overview** no menu principal, que o levará à RUM Home Page principal. O conceito desta página é mostrar rapidamente o status geral de todos os aplicativos RUM selecionados, seja em um dashboard completo ou na visualização compacta.

Independentemente do tipo de Painel de Status utilizado, a Home Page do RUM é composta por 3 seções distintas:

![Página RUM](../images/rum-main.png)

1. **Onboarding Pane:** Vídeos de treinamento e links para documentação para você começar a usar o Splunk RUM. (Você pode ocultar este painel caso precise do espaço da tela).
2. **Filter Pane:** Filtre por período, ambiente, aplicativo e tipo de fonte.
3. **Application Summary Pane:** Resumo de todos os seus aplicativos que enviam dados RUM.

{{% notice title="Ambientes RUM e aplicação e tipo de fonte" style="info" %}}

* O Splunk Observability usa a tag **environments** que é enviada como parte dos traces do RUM (criado a cada interação com seu site ou aplicativo móvel), para separar dados provenientes de diferentes ambientes como "Produção" ou "Desenvolvimento".
* Uma separação adicional pode ser feita pela Tag **Applications**. Isso permite distinguir entre navegadores/aplicativos móveis separados em execução no mesmo ambiente.
* O Splunk RUM está disponível para navegador e aplicativos móveis, você pode usar **Source Type** para distinguir entre eles, no entanto, para este workshop, usaremos apenas RUM baseado em navegador.

{{% /notice %}}

{{% exercise title="Filtre RUM e siga um erro JS" %}}

* Certifique-se de que a janela de tempo esteja definida como **-15m**
* Selecione o ambiente para sua workshop na caixa suspensa. A convenção de nomenclatura é **[NAME OF WORKSHOP]-workshop** (selecionar esta opção garantirá que o aplicativo RUM do workshop esteja visível)
* Selecione o nome **App**. Lá a convenção de nomenclatura é **[NAME OF WORKSHOP]-store** e deixe **Source** definido como **All**
* No bloco **JavaScript Errors**, clique na entrada **TypeError** que diz: *Não é possível ler propriedades de indefinido (lendo 'Prcie')* para ver mais detalhes. Observe que você receberá uma indicação rápida de em qual parte do site ocorreu o erro, permitindo que você corrija isso rapidamente.
* Feche o painel.
* O terceiro bloco relata **Web Vitals**, uma métrica que se concentra em três aspectos importantes da experiência do usuário: *carregamento*, *interatividade* e *estabilidade visual*.
{{< tabs >}}
{{% tab title="Pergunta" %}}
**Com base nas métricas **Web Vitals**, como você avalia o desempenho atual do site na Web?**
{{% /tab %}}
{{% tab title="Resposta" %}}
**De acordo com as métricas *Web Vitals*, o carregamento inicial do site está OK e foi classificado como *Bom***
{{% /tab %}}
{{< /tabs >}}

* O último bloco, bloco **Most recent detectors**, mostrará se algum alerta foi acionado para o aplicativo.
* Clique na seta **⌵** para baixo na frente do nome do aplicativo para alternar a visualização para o estilo compacto. Observe que você também tem todas as informações principais disponíveis nesta visualização. Clique em qualquer lugar da visualização compacta para voltar à visualização completa.

{{% /exercise %}}

A seguir, vamos verificar **Splunk Application Performance Monitoring (APM)**.
