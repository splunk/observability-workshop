---
title: 4. Detector de Synthetics
weight: 4
---
Dado que você pode executar esses testes 24 horas por dia, 7 dias por semana, é uma ferramenta ideal para ser avisado antecipadamente se seus testes estiverem falhando ou começando a durar mais do que o SLA acordado, em vez de ser informado pelas mídias sociais ou sites do Uptime.

![Mídia social](../images/social-media-post.png)

 Para impedir que isso aconteça, vamos detectar se nosso teste está demorando mais de 1,1 minuto.

 {{% exercise title="Crie um detector sintético" %}}

* Volte para a página inicial do Synthetics através do menu à esquerda
* Selecione o teste do workshop novamente e clique no botão {{% button %}}**Create Detector**{{% /button %}} na parte superior da página.

  ![detector de sintetizador](../images/synth-detector.png)
* Edite o texto **New Synthetics Detector** **(1)** e substitua-o por `INITIALS - [WORKSHOPNAME]`.
* Altere os critérios de alerta para que a métrica seja Duração da execução (em vez de Tempo de atividade) e a condição seja Limite estático.
* Defina **Trigger threshold** **(2)** em torno de `65,000` para `68,000` e pressione Enter para atualizar o gráfico.  Certifique-se de ter mais de um pico cortando a linha de limite, conforme mostrado acima (talvez seja necessário ajustar um pouco o valor do limite para corresponder à sua latência real).
* Deixe o resto como padrão.
* Observe que agora há uma linha de triângulos vermelhos e brancos aparecendo abaixo dos picos **(3)**. Os triângulos vermelhos informam que seu detector descobriu que seu teste estava acima do limite determinado e o triângulo branco indica que o resultado retornou abaixo do limite. Cada triângulo vermelho acionará um alerta.
* Você pode alterar a criticidade dos alertas **(4)** alterando o menu suspenso para um nível diferente, bem como o método de alerta.  Certifique-se de adicionar um destinatário **NOT**, pois isso pode fazer com que você seja submetido a uma tempestade de alertas!
* Clique em {{% button style="blue" %}}Activate{{% /button %}} para implantar seu detector.
* Para ver seu novo detector criado, clique no botão {{% button %}}Edit Test{{% /button %}}
* Na parte inferior da página há uma lista de detectores ativos.

  ![lista de detectores](../images/detector-list.png)

* Se você não consegue encontrar o seu, mas vê um chamado *Novo Detector Sintético*, talvez você não o tenha salvo corretamente com seu nome. Clique no link *Novo Detector Sintético* e refaça a renomeação.
* Clique no botão {{% button %}}Close{{% /button %}} para sair do modo de edição.
{{% /exercise %}}
