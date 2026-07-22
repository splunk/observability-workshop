---
title: Painel de integridade do serviço personalizado 🏥
linkTitle: 6. Painel de integridade do serviço
weight: 6
archetype: chapter
time: 15 minutos
description: Nesta seção, você aprenderá como criar um painel de integridade de serviço personalizado para monitorar a integridade de seus serviços.
---

{{% notice icon="user" style="orange" title="Persona" %}}

Como o chapéu de **SRE** combina com você, vamos mantê-lo, pois foi solicitado que você crie um painel de integridade do serviço personalizado para o **wire-transfer-service**. O requisito é exibir métricas RED, logs e resultados de duração de testes sintéticos.

{{% /notice %}}

É comum que as equipes de desenvolvimento e SRE exijam um resumo da integridade de seus aplicativos e/ou serviços. Mais frequentemente ou não, estes são exibidos em TVs montadas na parede. Splunk Observability Cloud tem a solução perfeita para isso, criando painéis personalizados.

Nesta seção vamos construir um **Service Health Dashboard** que podemos usar para exibir nos monitores ou TVs das equipes.
