---
title: From token counts to token value
linkTitle: 1. From token counts to token value
weight: 1
time: 5 minutes
---

For the next 90 minutes, we're going to cover how agentic applications consume tokens and how
we can validate that those tokens are effectively used.

Our goal is not simply to minimize tokens. The cheapest agent that produces the wrong answer
is not efficient. Neither is a highly accurate agent whose unnecessary loops, oversized
context, and expensive model choices make it impossible to scale.

> The question we will keep asking is: **what outcome did we receive for the tokens we spent?**

We will use a number of tools, including the health agent assistant. It looks up patient records
using an LLM, retrieval, and tools. Bills by themselves do not explain:

* Which users, agents, models, and workflow steps consume the tokens?
* Whether expensive requests are better than inexpensive requests?
* Whether a prompt, model, retrieval, or tool change would improve the ratio?

{{< checkpoint title="Knowledge Check" >}}

If your bill doubled for AI this month, what would you check to make sure it was justified?

{{< details summary="Click here to see the answer" >}}
You could check which agents, models, and workflows consumed the tokens, what value
proposition those use cases support, and whether that has led to an improvement in outcome. How do you
qualify those improvements? Read on!
{{< /details >}}