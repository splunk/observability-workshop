---
title: 14. Trace details
weight: 24
---

{{% notice style="grey" title="Click on a trace that has root (solid red) errors on the paymentservice" %}}
![Trace detail showing multiple paymentservice requests with errors](../img/trace.png?width=50vw)

{{% /notice %}}

{{% notice style="blue" title="Say" icon="user" %}}
Now I’m starting to get a good picture of what’s going on. This checkout process is making an API call to an external service over and over again and failing.

I’d like to look at the logs to see precisely what the error is.

{{% /notice %}}