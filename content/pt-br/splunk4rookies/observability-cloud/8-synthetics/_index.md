---
title: Splunk Synthetics
linkTitle: 8. Splunk Synthetics
archetype: chapter
weight: 8
time: 15 minutos
description: Nesta seção, você aprenderá como usar o Splunk Synthetics para monitorar o desempenho e a disponibilidade de seus aplicativos.
---

{{% notice icon="user" style="orange" title="Persona" %}}

Colocando seu chapéu **SRE** de volta, você foi solicitado a configurar o monitoramento para a Online Boutique. Você precisa garantir que o aplicativo esteja disponível e com bom desempenho 24 horas por dia, 7 dias por semana.

{{% /notice %}}

Não seria ótimo se pudéssemos monitorar nossa aplicação 24 horas por dia, 7 dias por semana, e sermos alertados quando houver algum problema? É aqui que entra o Synthetics. Mostraremos um teste simples que é executado a cada 1 minuto e verifica o desempenho e a disponibilidade de uma jornada típica do usuário pela Online Boutique.
