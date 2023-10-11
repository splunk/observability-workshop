---
title: 21. Test failure details
weight: 42
---

{{% notice style="grey" title="Click the last Transaction or Page tab, scroll through the filmstrip to show the images, and scroll down to the long checkout request" %}}
![Checkout requests](../img/failed-run-example.png?width=50vw)

{{% /notice %}}

{{% notice style="blue" title="Say" icon="user" %}}
We see that this test run failed because it never got to confirm the Order ID. Looking at the requests in the checkout, we see a long POST request to checkout with an APM link. Familiar, right?
{{% /notice %}}