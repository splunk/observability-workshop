---
title: From Token Counts to Token Value
linkTitle: 1. From Token Counts to Token Value
weight: 1
time: 5 minutes
---

In this workshop, we're going to cover how agentic applications consume tokens and how
we can validate that those tokens are effectively used.

Our goal is not simply to minimize tokens. The cheapest agent that produces the wrong answer
is not efficient. Neither is a highly accurate agent whose unnecessary loops, oversized
context, and expensive model choices make it impossible to scale.

> The question we will keep asking is: **what outcome did we receive for the tokens we spent?**

We will use a number of tools, both reactive and proactive. We will investigate the data
from a high level, all the way down to each granular trace records, reviewing every LLM 
invocation, chunk retrieval, and tool call. 

LLM provider bills by themselves do not explain:

* Which users, agents, models, and workflow steps consume the tokens?
* Are expensive requests better than inexpensive requests?
* Does a prompt, model, retrieval, or tool change improve the ratio?

{{< checkpoint title="Knowledge Check" >}}

If your bill doubled for AI this month, what would you check to make sure it was justified?

{{< details summary="Click here to see the answer" >}}
You could check which agents, models, and workflows consumed the tokens, what value
proposition those use cases support, and whether that has led to an improvement in outcome. How do you
qualify those improvements? Read on!
{{< /details >}}