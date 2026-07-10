---
title: 5. Criar Detector
weight: 5
---

{{% exercise title="Receber alertas" %}}

* Vá para **Digital Experience → Synthetics tests** no menu principal.
* Selecione o teste do workshop **[NAME OF WORKSHOP]**.
* Clique no teste.
* Clique no botão {{% button %}}**Create Detector**{{% /button %}} no topo da página:
* Altere os critérios de alerta para que a métrica seja **Run Duration** **(1)** (em vez de Uptime) e a condição seja **Static Threshold**.
* Defina o **Trigger threshold** **(2)** para algo em torno de `50000` ms.
* Defina **Split by location** **(3)** como **No**.
* Observe que agora há uma linha de triângulos vermelhos e brancos aparecendo abaixo dos picos no gráfico.
* Os triângulos vermelhos indicam que o detector encontrou seu teste acima do limite definido, e o triângulo branco indica que o resultado voltou para baixo do limite. Cada triângulo vermelho disparará um alerta.

> [!WARNING] Não adicionaremos um destinatário nem ativaremos o detector, pois não queremos inundar seu e-mail com alertas.

![Detector](../images/synth-detector.png)

* Esta aplicação foi projetada para falhar constantemente, por isso a grande quantidade de alertas que seria gerada. Em um cenário real, você ajustaria o threshold para evitar falsos positivos.

{{% /exercise %}}
