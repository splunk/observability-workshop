---
title: 4.6 Message Abstractions
linkTitle: 4.6 Message Abstractions
weight: 6
---

## LangChain Message Abstractions

The application uses LangChain message abstractions rather than one long prompt string.

``` python
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
)
```

This is important because each node can separate:

* system role
* user task
* model response

For example:

```python
messages = [
    SystemMessage(content="You are a flight booking specialist. Provide concise options."),
    HumanMessage(content=step),
]
result = llm.invoke(messages)
```

### Knowledge Check

How would you define system, human, and AI messages?

{{< details summary="Click here to see the answer" >}}
In LangChain and LangGraph, messages are typically categorized by who is speaking and what role they play in guiding the conversation:

* **System message**: Sets the rules and context for the AI’s behavior. It defines instructions, constraints, tone, and goals that guide how the model should respond throughout the interaction.
* **Human message**: Input from the user. It contains questions, requests, or information that the AI should respond to.
* **AI message**: The model’s response. It represents the assistant’s generated output based on the system instructions and human input.
{{< /details >}}
