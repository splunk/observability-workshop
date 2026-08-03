---
title: 3. Session Replay
weight: 3
---

{{% notice title="Sessões" style="info" %}}

Uma sessão é uma coleção de rastreamentos que correspondem às ações que um único usuário realiza ao interagir com um aplicativo. Por padrão, uma sessão dura até 15 minutos desde o último evento capturado na sessão. A duração máxima da sessão é de 4 horas.

{{% /notice %}}

{{% exercise title="Abra a sessão mais longa" %}}

* Na tabela **User Sessions**, clique no **Session ID** superior com o **Duration** mais longo (mais de 20 segundos ou mais), isso o levará para a visualização da Sessão RUM.

{{% /exercise %}}

![Sessão RUM](../images/rum-session.png)

{{% exercise title="Assista ao replay da sessão" %}}

* Clique no botão RUM Session Replay {{% button icon="play" %}}Replay{{% /button %}}. RUM Session Replay permite reproduzir e ver a sessão do usuário. Essa é uma ótima maneira de ver exatamente o que o usuário experimentou.
* Clique no botão para iniciar o replay.

{{% /exercise %}}

O RUM Session Replay pode redigir informações; por padrão, o texto é redigido. Você também pode redigir imagens (o que foi feito neste exemplo de workshop). Isto é útil se você estiver reproduzindo uma sessão que contém informações confidenciais. Você também pode alterar a velocidade de reprodução e pausar a reprodução.

{{% notice title="Dica" style="primary"  icon="lightbulb" %}}

Ao reproduzir a sessão, observe como os movimentos do mouse são capturados. Isso é útil para ver onde o usuário está concentrando sua atenção.

{{% /notice %}}
