---
title: 1. Introdução a Logs
weight: 1
---

Agora você navegou diretamente de um trace de **APM** para **Logs** usando o link de **Related Content**. **Logs** é a interface no-code do Splunk Observability Cloud para explorar e analisar dados de logs.

A principal vantagem, assim como na integração entre **RUM** e **APM**, é que você está vendo seus logs no contexto das ações anteriores. Neste caso, esse contexto inclui o intervalo de tempo correspondente **(1)** do trace e um filtro **(2)** aplicado automaticamente ao `trace_id`.

![Trace Logs](../images/log-observer-trace-logs.png)

Esta visualização incluirá **todas** as linhas de log de **todos** os serviços que participaram da transação de back-end iniciada pela interação do usuário final com o Online Boutique.

Mesmo em uma aplicação pequena como a nossa Online Boutique, a quantidade de logs encontrados pode dificultar a visualização das linhas específicas que realmente importam para o incidente que estamos investigando.

Antes de avançar, vamos recapitular rapidamente o que fizemos até aqui e por que estamos aqui, com base nos 3 pilares da Observabilidade:

|  Métricas                  | Traces                      |  Logs                      |
| :-------:                  | :------:                    | :----:                     |
| _**Tenho um problema?**_   | _**Onde está o problema?**_ | _**Qual é o problema?**_   |

* Usando métricas de **RUM**, identificamos que **temos um problema** em nossa aplicação. Isso ficou claro pelas métricas de duração das sessões de usuário.
* Usando traces e span tags, descobrimos **onde está o problema**. O **paymentservice** tem duas versões, `v350.9` e `v350.10`, e a taxa de erro era **100%** para `v350.10`.
* Vimos que esse erro do **paymentservice** `v350.10` causou múltiplas tentativas e um atraso longo na resposta do checkout do Online Boutique.
* A partir do trace, usando o poder do **Related Content**, chegamos às entradas de log da versão com falha do **paymentservice**. Agora podemos determinar **qual é o problema**.
