---
title: 1. Agent Basics
linkTitle: 1. Agent Basics
weight: 1
time: 5 minutes
---

An AI agent is a software loop that combines four pieces:

* **Instructions**: what the agent is allowed to do and how it should behave.
* **State**: the request, context, intermediate observations, and final answer.
* **Tools**: functions the agent can call to read data or take action.
* **Decision logic**: a model or controller that chooses the next step.

In a production agent, the decision logic is often an LLM. In this workshop, the
decision logic is intentionally small and deterministic so you can see the shape of the
system without debugging model behavior.

## The Agent Loop

Most agents follow this pattern:

1. Read the user request.
2. Decide whether more information or an action is needed.
3. Call a tool.
4. Add the tool result to state.
5. Repeat until the agent can produce a final answer.

The loop is what makes an agent different from a single prompt. A prompt asks a model to
respond. An agent can decide to use a tool, inspect the result, and continue.

## Safety Boundary

Every agent needs a clear boundary. For this workshop, the agent can only:

* Read a local profile file.
* Add tasks to an in-memory list.
* Draft a message.

It cannot send email, change infrastructure, or call external APIs.

{{% notice title="Knowledge Check" style="green" icon="running" %}}
What is the difference between a tool and a final answer?

{{< details summary="Click here to see the answer" >}}
A tool is code the agent calls to gather information or take an action. A final answer is
the response the agent gives back to the user after it has enough context.
{{< /details >}}
{{% /notice %}}
