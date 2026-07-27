---
title: Principais conclusões
linkTitle: 1. Principais conclusões
weight: 1
---

Durante o workshop, vimos como o Splunk Observability Cloud em combinação com os sinais OpenTelemetry (**métricas**, **traces** e **logs**) pode ajudá-lo a reduzir o tempo médio de detecção (**MTTD**) e também reduzir o tempo médio de resolução (**MTTR**).

* Compreendemos melhor a interface principal do usuário e seus componentes, as páginas *Landing, Infrastructure, APM, Log Observer* e *Dashboard*, além de termos dado uma rápida olhada na página *Settings*.
* Dependendo do tempo, fizemos um exercício de *Infraestrutura* e analisamos as *Métricas* usadas nos Navegadores Kubernetes e vimos serviços relacionados encontrados em nosso cluster Kubernetes:

![Kubernetes](../images/infra-k8s.png)

* Entendemos o que os usuários estavam vivenciando e usamos o APM para investigar um tempo de carregamento particularmente longo e um erro, seguindo o trace pelo front-end, pelo back-end e até as entradas de log.
Usamos ferramentas como o *Dependency map* do APM com Breakdown para descobrir o que estava causando o problema:

![apm](../images/apm.png)

* Usamos o *Tag Spotlight* no APM para entender o raio de impacto, detectar tendências e obter contexto sobre nossos problemas de desempenho e erros. Analisamos os *spans* no *Trace waterfall* do APM para ver como os serviços interagiam e encontrar erros:

![tag e cascata](../images/tag-spotlight-waterfall.png)

* Usamos o recurso *Conteúdo relacionado* para seguir o link entre nosso *Trace* diretamente para os *Logs* relacionados ao nosso *Trace* e usamos filtros para detalhar a causa exata do nosso problema.

![registros](../images/log.png)

* No exercício final, criamos um painel de saúde para mantê-lo funcionando para nossos desenvolvedores e SREs em uma tela de TV:

![sintetizador e TV](../images/synth-tv.png)
