---
title: Cause 1 — The Wrong Model
linkTitle: 4. Choose the Right Model
weight: 4
time: 15 minutes
---

Adding an AI Assistant to an online store can enable several new ways for customers to interact
with our company: they can ask questions about policies and procedures, they can ask for help
finding the perfect product, they can get help with returns and refunds, etc.

Enabling this new path to revenue brings a huge opportunity; however, it also brings risk:
poor service that might drive customers away, wrong answers or promises that are legally binding,
massive cost spikes driven by untamed token consumption, etc.

Fortunately, technology is evolving to keep these risks under control, while exploring the new
opportunities brought on by AI Agents.

For instance, a critical part of our AI Shopping Assistant is determining how to fulfill the user's
request. We saw that in the previous section, when we looked into one of the traces.

One of the ways to optimize token costs is to send each request to the most appropriate model:
simple requests should be handled by cheaper models, while more complex or critical tasks should
be given to more robust (and expensive) models. Sending a simple task to an expensive model will
yield good results, but cost more than necessary; on the other hand, sending a complex task to a 
simpler model might cause problems and issues (that might require the task to be re-sent to the
expensive model).

Part of the development process for our AI Shopping Assistant is to map the different tasks that
the agent will be able to execute, and understand which model is more appropriate for the different
tasks. One way to do this validation is by leveraging Experiments.

## Experiments

The goal for this section is to find the best LLM to handle the task. For this lab, we have 2 
tasks that the agent must perform:
- **Answer Q&A questions**, which are questions related to policies and procedures, like returns,
refunds, loyalty, etc. This usually involves a vector search against a knowledge base.
- **Answer Product related questions**, such as availability, sizes, price, etc. These require
interactions with the product catalog and inventory systems.

Q&A questions are simpler and more straightforward; we expect a simpler, cheaper model to be able
to handle them. However, we cannot risk hallucinations or poor responses driving customers away.

Product questions are a lot more critical, because they can lead to a purchase, or drive a potential
customer away. These are worth the cost of more robust models, which can provide a more complete
and compelling response. Or so we expect.

To put our theories to the test, we can run an experiment: have 2 datasets, one with Q&A questions,
and one with Product-related questions. Each dataset contains a curated, representative set of 
inputs, meant to emulate the type of input that our customers will have, when the agent is running
in production. These datasets also include the 'Ground Truth', which represents the answer we should
expect from the agent; this information gives us a strong understanding of response quality.

> [!TIP]
> When you implement real-time monitoring with Splunk Agent Observability, you can save real production
prompts as a new dataset to validate against new versions of your agent.

Experiments allows us to compare an agentic workload under different conditions: different models, 
prompts, datasets, retrieval settings, and more. Instead of changing these conditions at once, 
we run controlled sets of experiments, changing one condition at a time; otherwise, we would not be 
able to explain the results. In this lab, we will see a simplified version of this iteration, by
focusing on the models and tools used to fulfill each type of task.

In this comparison, both experiments received the same 18 product questions. One agent used a
simpler (cheaper) model, with its own options for retrieval, while the other agent leveraged
the more robust (expensive) model, also with its own retrieval logic. Each LLM determines 
how to handle each of the 18 prompts that it received.

The experiments are divided into 2 groups:
- **Product Model Comparison**: evaluates which model is best suited to handle product-related inputs
- **Q&A Model Comparison**: evaluates how each model handles Q&A questions.

Go to the **Experiments** page, where we will find the 2 experiment groups.

First, let's see how the agents handled the Product questions.

Open **Experiment Groups > Product Model Comparison**.

Before we even compare the experiments, we can see the key results at a glance:

![Product Questions Experiment](../_images/6/4_01_experiment_product.png?width=750px)

Let's understand what our key metrics represent for these experiments:
- **Context Adherence**: Measures how well the response aligns with the provided context.
A great eval to detect hallucinations in LLM responses.
- **Ground Truth Adherence**: Measures how well the response aligns with established ground truth.
The datasets we used for the experiment include the ground truth, which is the response we *expect*
to receive from the agent at the end. This metric helps us evaluate how close to an optimal response
the agent got.

Before we even compare these experiments, we can already tell that, by using the simpler (cheaper) LLM,
we got a number of responses that deviated from the retrieved context, which caused these responses to 
be quite different from the ground truth. This is not ideal, and it signals that our LLM is hallucinating 
most of the responses.

Meanwhile, the more robust (and expensive) LLM was able to properly handle all the dataset prompts,
providing correct answers every time.

Based on these results *alone*, we can confidently say that it's better to keep the more expensive
model for product-related questions. 

However, there's more we can learn from these experiments.


{{< step title="Product Related Questions Experiment" >}}

Go to the **Compare** tab. Because there are only 2 experiments, they will be automatically selected. 
Alternatively, you can select both experiments and click on the **Compare Experiments** button.

![Product Questions Experiment Comparison](../_images/6/4_02_experiment_product_comparison.png?width=750px)

The comparison screens shows all information about each experiment: *Details* (including duration, costs and
token counts), *Evaluators* (we can enable as many as needed in our experiments) and the *Trace* information,
including the inputs and outputs.

Notice that the input is the exact same between both agents; this happens because each experiment runs with
the same dataset. The responses, however, will be very different. In the traces with negative Ground Truth 
Adherence, they will be too simple and generic, using nothing of the retrieved documents. Something like:

> We have a selection of footwear that might interest you..

The expensive model will have a better answer, addressing the specific question directly, providing
more details in some cases and always providing a response to the question.

What do you notice about the two answers? The first is concise to the point where it doesn't really
help. The second is more useful, but it is also longer. And more compelling to a potential buyer.

#### Compare quality

The quality evaluators tell us that the simpler model could not handle the product questions very well.
In most of the cases, it produced responses that are too simple. Were this to happen in production,
there's a good chance the user would just ask the same question again, or worse, move on to another
e-commerce store.

Examine the comparison traces, even between outputs that have positive Ground Truth Adherence:

![Product Questions Experiment Comparison](../_images/6/4_03_experiment_product_comparison_2.png?width=750px)

Even with what is considered here a 'valid' response, we can see that the response provided by the
simpler agent is still vague and not compelling, while the responses provided by the more expensive
model are more complete, more compelling and more likely to generate follow-up from the user.

> [!TIP]
> If we don't agree with the reasoning that this was indeed a valid response, we can provide feedback that
will change how the eval is computed. This will help align the evals with the business purpose of our AI agent.


#### Compare tokens, latency, and cost

| System metric | Inexpensive model | Expensive model |
|---------------|-------------------|-----------------|
| Input tokens | 279 | 298 |
| Output tokens | 12 | 59 |
| Total tokens | 291 | 357 |
| Latency | 292 ms | 2.36 sec |
| Agent cost | less than $0.0001 | $0.0026 |

*(PS: These numbers may be different for you)*

These values describe a single prepared comparison; they are not universal model benchmarks.
The inexpensive model is faster and cheaper here, but it fails Ground Truth Adherence. The
expensive model completes the task, but costs more and produces a longer answer.

> Token efficiency is not always proportional to price or token count. A response that uses fewer
> tokens but does not complete the task may create another user turn, an escalation, or an
> abandoned journey.

In this case, the need for the more expensive model can be clearly justified, since these 
responses are meant to stimulate the customer to purchase products. However, this break even
will be different, depending on the scope of your AI agent.

#### Decide how to route

This was a simple example; the reality will be more granular, and offer more solutions
to this type of challenge, with options such as:

1. Send every request to the inexpensive model.
2. Send every request to the expensive model.
3. Route by task complexity and required quality.

A configuration should advance only when it:

1. Meets the defined quality and safety thresholds.
2. Improves cost, latency, or both for the target task.
3. Remains consistent across the dataset, not just one favorable example.

<hr>


Do not conclude that larger models are always better. The right model is workload-specific and
should be selected with controlled, repeatable evidence.

To illustrate that, let's look at the other experiment.

{{< /step >}}

{{< step title="Q&A Questions Experiment" >}}

Back on the **Experiments** page, click on the **Q&A Model Commparison** experiment group.

Here we again see 2 experiments, but these tell a different story.

![Q&A Questions Experiment Comparison](../_images/6/4_04_experiment_qa_comparison.png?width=750px)

At a glance, we can tell that both are delivering almost the same quality, while the simpler model
is showing considerable lower latency (which is great for user experience).

Let's go to the **Compare** tab and take a closer look.
Alternatively, you can select both experiments and click on the **Compare Experiments** button.

![Q&A Questions Experiment Comparison](../_images/6/4_05_experiment_qa_comparison_2.png?width=750px)

Browse through the traces. You will see that, even though the responses from the simpler model are 
shorter, they are usually more concise and to the point, which works well for Q&A type questions.
Also, there should be no hallucinations in the response (if there are, take a look at the rationale
for the eval).

Also, compare the costs between them. Very small difference individually, sure, but at production scale,
it could impact your budget considerably.

Based on first impressions, it seems like the cheaper model might be a good option here to keep
inferencing costs low, without compromising on response quality.

#### Compare quality

Overall, quality is very similar between the models, to the point where it becomes hard to
justify the more expensive model. There are basically no hallucinations in the cheap model.

Even if a trace has the **Ground Truth Adherence** eval as `false`, you can click on the eval
to see the reasoning for the score:

![Q&A Questions Experiment Comparison](../_images/6/4_06_experiment_qa_comparison_3.png?width=750px)

It might be more related to the fact that the answer is slightly incomplete, omitting details from
the retrieved context, than a hallucination. The out-of-the-box eval might be too sensitive for this
type of omission, but it doesn't mean it's not a valid response. Compare the retrieved document in the
input with the generated response, and determine whether this was a valid response or not.

> [!TIP]
> As mentioned before, we can change how the eval reasons over the data. If we believe this this is indeed
a valid response, we can provide feedback to change and adapt the eval to the business purpose of our agent.


#### Compare tokens, latency, and cost

| System metric | Inexpensive model | Expensive model |
|---------------|-------------------|-----------------|
| Input tokens | 117 | 121 |
| Output tokens | 22 | 76 |
| Total tokens | 139 | 197 |
| Latency | 763 ms | 2.64 sec |
| Agent cost | less than $0.0001 | $0.0023 |

*(PS: These numbers will be different for you)*

The performance difference is considerable here, especially the latency. Token costs are also
something to consider, especially when we think about production scale, with millions of these
interactions happening over the year.

> Fast and good beats slow and good every time. Through the use of Experiments, we can
> select the best model to take on the task, by evaluating quality, performance and cost,
> to arrive at the best option.

{{< /step >}}

<hr>

#### Decide how to route

Based on these experiments, our recommendation would be:

- Leverage the simpler (cheaper) model for the Q&A questions;
- Rely on the more robust (expensive) model for the product-related questions;



{{< checkpoint title="Knowledge Check" >}}

Why is the inexpensive and token-efficient response not always the winner, despite using
fewer tokens and costing less?

{{< details summary="Click here to see the answer" >}}
What matters is that the agent completes the user's task. The Ground Truth Adherence eval returns
false when the response fails to provide the proper information. Efficiency must include the outcome, 
not just consumption. Quality evals must be taken into account as critically as performance metrics.
{{< /details >}}