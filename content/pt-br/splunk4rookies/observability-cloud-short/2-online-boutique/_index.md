---
title: Vamos às compras 💶
linkTitle: 2. Compras no Online Boutique
weight: 2
time: 5 minutos
description: Interaja com a aplicação web Online Boutique para gerar dados no Splunk Observability Cloud.
---

{{< presenter title="Timing" >}}
Reserve cerca de 10 minutos para os participantes concluírem esta seção.
{{< /presenter >}}

{{% notice icon="user" style="orange" title="Persona" %}}

Você é uma pessoa **profissional urbana e descolada**, querendo comprar seus próximos itens diferentes na famosa loja Online Boutique. Você ouviu dizer que a Online Boutique é o lugar certo para todas as suas necessidades hipster.

{{% /notice %}}

{{% exercise title="Terapia de varejo" %}}

* A aplicação já está implantada. O instrutor vai fornecer um link para o site Online Boutique (por exemplo, `http://<s4r-workshop-i-xxx.splunk>.show:81/`). As portas 80 e 443 também estão disponíveis se a porta 81 não estiver acessível.
* Navegue pelo Online Boutique, adicione alguns itens ao carrinho e conclua uma compra.
* Repita isso pelo menos 3 a 5 vezes para expor os problemas de desempenho criados de propósito na aplicação.

{{< tabs >}}
{{% tab title="Pergunta" %}}

**Todo o processo de checkout deveria levar apenas milissegundos. Você notou algo no processo de checkout?**

{{% /tab %}}
{{% tab title="Resposta" %}}

**Às vezes fica lento!** 🐌

{{% /tab %}}
{{< /tabs >}}

* Quando o processo de checkout fica lento, ele cria uma experiência frustrante para o usuário. Como isso impacta diretamente a satisfação do cliente, devemos priorizar a investigação e a correção do problema.

{{% image src="images/shop.png" align="center" %}}

{{% /exercise %}}

Vamos para a próxima página, onde começaremos a usar o Splunk Observability Cloud e veremos como os dados aparecem no **Splunk Real User Monitoring (RUM)**.
