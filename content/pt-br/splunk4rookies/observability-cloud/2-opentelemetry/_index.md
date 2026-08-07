---
title: O que é OpenTelemetry e por que você deveria se importar?
linkTitle: 2. OpenTelemetry
weight: 2
archetype: chapter
time: 2 minutos
description: Aprenda sobre o OpenTelemetry e por que você deve se preocupar com ele.
---

## OpenTelemetry

Com o surgimento da computação em nuvem, das arquiteturas de microsserviços e dos requisitos de negócios cada vez mais complexos, a necessidade de observabilidade nunca foi tão grande. Observabilidade é a capacidade de compreender o estado interno de um sistema examinando seus resultados. No contexto do software, isso significa ser capaz de compreender o estado interno de um sistema examinando seus dados de telemetria, que incluem **métricas**, **traces** e **logs**.

Para tornar um sistema observável, ele deve ser instrumentado. Ou seja, o código deve emitir traces, métricas e logs. Os dados instrumentados devem então ser enviados para um back-end de Observabilidade, como **Splunk Observability Cloud**.

| Métricas | Vestígios | Registros |
|:-------:|:------:|:----:|
| _**Tenho algum problema?**_ | _**Onde está o problema?**_ | _**Qual é o problema?**_ |

OpenTelemetry faz duas coisas importantes:

* Permite que você seja **proprietário** dos dados gerados, em vez de ficar preso a um formato ou ferramenta de dados proprietária.
* Permite que você aprenda **um único conjunto** de APIs e convenções

Essas duas coisas combinadas proporcionam às equipes e organizações a flexibilidade necessária no mundo da computação moderna de hoje.

Há muitas variáveis ​​a serem consideradas ao começar a usar Observabilidade, incluindo a importante questão: _"Como coloco meus dados em uma ferramenta de Observabilidade?"_. A adoção do OpenTelemetry em todo o setor torna esta questão mais fácil de responder do que nunca.

## Por que você deveria se importar?

OpenTelemetry é totalmente de código aberto e de uso gratuito. No passado, as ferramentas de monitoração e observabilidade dependiam fortemente de agentes proprietários, o que significa que o esforço necessário para alterar ou configurar ferramentas adicionais exigia uma grande quantidade de alterações nos sistemas, desde o nível da infraestrutura até ao nível da aplicação.

Como o OpenTelemetry é neutro em termos de fornecedor e é apoiado por muitos líderes do setor no espaço de Observabilidade, os adotantes podem alternar entre as ferramentas de Observabilidade suportadas a qualquer momento, com pequenas alterações em sua instrumentação. Isso é verdade independentemente de qual distribuição do OpenTelemetry é usada – como no Linux, as várias distribuições agrupam configurações e complementos, mas são todas fundamentalmente baseadas no projeto OpenTelemetry conduzido pela comunidade.

O Splunk está totalmente comprometido com o OpenTelemetry para que nossos clientes possam coletar e usar **TODOS** os seus dados, em qualquer tipo, qualquer estrutura, de qualquer fonte, em qualquer escala e tudo em tempo real. A OpenTelemetry está mudando fundamentalmente o cenário de monitoramento, permitindo que as equipes de TI e DevOps levem dados para cada pergunta e cada ação. Você experimentará isso durante esses workshops.

![Logotipo OpenTelemetry](images/otel.png)
