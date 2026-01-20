---
title: Let's go shopping 💶
linkTitle: 4. Shopping at the Online Boutique
weight: 4
time: 5 minutes
description: Interact with the Online Boutique web application to generate data for Splunk Observability Cloud.
---

{{% notice icon="user" style="orange" title="Persona" %}}

You are a **hip urban professional**, longing to buy your next novelty items in the famous Online Boutique shop. You have heard that the Online Boutique is the place to go for all your hipster needs.

{{% /notice %}}

The purpose of this exercise is for you to interact with the Online Boutique web application.  This is a sample application that is used to demonstrate the capabilities of Splunk Observability Cloud. The application is a simple e-commerce site that allows you to browse items, add them to your cart, and then checkout.

The application will already be deployed for you and your instructor will provide you with a link to the Online Boutique website e.g:

* **http://<s4r-workshop-i-xxx.splunk>.show:81/**. The application is also running on ports **80** & **443** if you prefer to use those or port **81** is unreachable.

{{% notice style="green" icon="running" title="Exercise - Let's go shopping" %}}

* Once you have the link to the Online Boutique, have a browse through a few items, add them to your cart and then, finally, do a checkout.
* Repeat this exercise a few times and if possible use different browsers, mobile devices or tablets as this will generate more data for you to explore.

{{% /notice %}}

<!--
{{% notice style="primary" icon="lightbulb" title="Tip" %}}

While you are waiting for pages to load, please move your mouse cursor around the page. This will generate more data for us to explore at a later date in this workshop.

{{% /notice %}}
-->

{{% notice style="green" icon="running" title="Exercise (cont.)" %}}

* Did you notice anything about the checkout process? Did it seem to take a while to complete, but it did ultimately complete? When this happens please copy the **Order Confirmation ID** and save it locally somewhere as we will need it later.
* Close the browser sessions you used to shop.

{{% /notice %}}

This is what a poor user experience can feel like and since this is a potential customer satisfaction issue we had better jump on this and troubleshoot.

![Online Boutique](images/shop.png)

Let’s go take a look at what the data looks like in **Splunk RUM**.
