---
title: Painel de integridade do serviço personalizado 🏥
linkTitle: 9. Painel de integridade do serviço
weight: 9
archetype: chapter
time: 15 minutos
description: Nesta seção, você aprenderá como criar um painel de integridade de serviço personalizado para monitorar a integridade de seus serviços.
---

{{% notice icon="user" style="orange" title="Persona" %}}

Como o chapéu **SRE** combina com você, vamos mantê-lo, pois foi solicitado que você criasse um painel de integridade do serviço personalizado para o **paymentservice**. O requisito é exibir métricas RED, logs e resultados de duração de teste sintético.

{{% /notice %}}

É comum que as equipes de desenvolvimento e SRE exijam um resumo da integridade de seus aplicativos e/ou serviços. Mais frequentemente ou não, estes são exibidos em TVs montadas na parede. Splunk Observability Cloud tem a solução perfeita para isso, criando painéis personalizados.

Nesta seção vamos construir um **Service Health Dashboard** que podemos usar para exibir nos monitores ou TVs das equipes.
