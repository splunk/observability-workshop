---
title: Vamos às compras 💶
linkTitle: 4. Compras na Online Boutique
weight: 4
time: 5 minutos
description: Interaja com o aplicativo da web Online Boutique para gerar dados para o Splunk Observability Cloud.
---

{{% notice icon="user" style="orange" title="Persona" %}}

Você é um **profissional urbano descolado** e deseja comprar suas próximas novidades na famosa loja Online Boutique. Você já ouviu falar que a Online Boutique é o lugar ideal para todas as suas necessidades hipster.

{{% /notice %}}

Interaja com o Online Boutique — um exemplo de aplicativo de comércio eletrônico (navegar, carrinho, finalizar compra) conectado ao Splunk Observability Cloud.

O aplicativo já estará implantado para você e seu instrutor fornecerá um link para o site da Online Boutique, por exemplo:

* **http://<s4r-workshop-i-xxx.splunk>.show:81/**. O aplicativo também está sendo executado nas portas **80** & **443** se você preferir usá-las ou a porta **81** está inacessível.

{{% notice style="green" icon="running" title="Exercício – Vamos às compras" %}}

* Depois de ter o link da Online Boutique, navegue por alguns itens, adicione-os ao carrinho e, por fim, finalize a compra.
* Repita este exercício algumas vezes e se possível utilize navegadores, dispositivos móveis ou tablets diferentes, pois isso gerará mais dados para você explorar.

{{% /notice %}}

{{% notice style="primary" icon="lightbulb" title="Dica" %}}

Enquanto espera o carregamento das páginas, mova o cursor do mouse pela página. Isso gerará mais dados para explorarmos posteriormente neste workshop.

{{% /notice %}}

{{% notice style="green" icon="running" title="Exercício (cont.)" %}}

* Você notou alguma coisa sobre o processo de checkout? Pareceu demorar um pouco para ser concluído, mas finalmente foi concluído? Quando isso acontecer, copie **Order Confirmation ID** e salve-o localmente em algum lugar, pois precisaremos dele mais tarde.
* Feche as sessões do navegador que você usou para fazer compras.

{{% /notice %}}

É assim que pode ser uma experiência ruim do usuário e, como esse é um problema potencial de satisfação do cliente, é melhor abordarmos isso e solucionar o problema.

![Boutique on-line](images/shop.png)

Vamos dar uma olhada na aparência dos dados em **Splunk RUM**.
