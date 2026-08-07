---
title: Principais conclusões
linkTitle: 1. Principais conclusões
weight: 1
---

Durante o workshop, vimos como o Splunk Observability Cloud em combinação com os sinais OpenTelemetry (**métricas**, **traces** e **logs**) pode ajudá-lo a reduzir o tempo médio de detecção (**MTTD**) e também reduzir o tempo médio de resolução (**MTTR**).

* Temos uma melhor compreensão da interface do usuário principal e seus componentes, as páginas *Landing, Infrastructure, APM, RUM, Synthetics, Dashboard* e uma rápida olhada na página *Settings*.
* Dependendo do tempo, fizemos um exercício de *Infraestrutura* e analisamos as *Métricas* usadas nos Navegadores Kubernetes e vimos serviços relacionados encontrados em nosso cluster Kubernetes:

![Kubernetes](../images/infra.png)

* Entendeu o que os usuários estavam enfrentando e usou RUM e APM para solucionar problemas de carregamento de página particularmente longo, seguindo seu rastreamento no front e back-end e direto nas entradas de log.
Usamos ferramentas como RUM *Session replay* e APM *Dependency map* com Breakdown para descobrir o que está causando nosso problema:

![rum e apm](../images/rum-apm.png)

* Usamos *Tag Spotlight*, tanto em RUM quanto em APM, para entender o raio de explosão, detectar tendências e contexto para nossos problemas e erros de desempenho. Analisamos *Span's* no *Trace cascata* do APM para ver como os serviços interagiam e encontrar erros:

![tag e cascata](../images/tag-spotlight-waterfall.png)

* Usamos o recurso *Conteúdo relacionado* para seguir o link entre nosso *Trace* diretamente para os *Logs* relacionados ao nosso *Trace* e usamos filtros para detalhar a causa exata do nosso problema.

![registros](../images/log.png)

* Em seguida, analisamos o Synthetics, que pode simular o tráfego web e móvel e usamos o Teste Sintético disponível, primeiro para confirmar nossa descoberta do RUM/AMP e do Log Observer, depois criamos um *Detector* para sermos alertados se o tempo de execução de um teste excedesse nosso SLA.

* No exercício final, criamos um painel de saúde para mantê-lo funcionando para nossos desenvolvedores e SREs em uma tela de TV:

![sintetizador e TV](../images/synth-tv.png)
