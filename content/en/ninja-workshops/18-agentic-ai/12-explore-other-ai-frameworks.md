---
title: Explore Other Agentic AI Frameworks
linkTitle: 12. Explore Other Agentic AI Frameworks
weight: 12
time: 15 minutes
---

In earlier sections of this workshop, we focused on instrumenting Agentic AI applications 
built with **LangChain** and **LangGraph** using OpenTelemetry.

In this section, we broaden the scope to cover **other popular Agentic AI frameworks** 
and outline the available instrumentation approaches.

At a high level, there are **two primary options** for instrumenting Agentic AI 
applications with OpenTelemetry. The best approach depends on the framework used 
and whether the application already includes existing instrumentation.

## Choosing the Right Instrumentation Approach

### Option 1: Splunk OpenTelemetry Instrumentation (Recommended When Available)

Splunk provides OpenTelemetry instrumentation packages for several widely
used Agentic AI frameworks, including:

* CrewAI
* LangChain/LangGraph
* LlamaIndex
* OpenAI SDK
* OpenAI Agents SDK

#### When to use this option

Choose this approach when:

* Your application uses one of the frameworks listed above.
* You want **OpenTelemetry instrumentation** optimized for Splunk Observability Cloud with minimal configuration.
* You prefer a **zero-code** instrumentation experience.

#### How it works 

Follow the steps in [Zero-code instrumentation integrations](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-agent-monitoring/set-up-ai-agent-monitoring/zero-code-instrumentation#zero-code-instrumentation-integrations-0)
to instrument your application.

Depending on the framework, you may need to:

* Install additional Splunk OpenTelemetry packages
* Set specific environment variables to enable optional features such as:
  * Capturing LLM prompts and completions 
  * Evaluating semantic quality of LLM responses 
  * Integrating with Cisco AI Defense 

**Note**: This is the same approach used earlier in the workshop for 
LangChain and LangGraph, including optional prompt and completion capture.

### Option 2: Third-Party Instrumentation Libraries 

If your framework is **not directly supported** by Splunk OpenTelemetry instrumentation, 
you can use a third-party library that provides broader framework coverage.

Commonly used third-party instrumentation libraries include:

* [LangSmith](https://docs.langchain.com/langsmith/observability): 
* [OpenLIT](https://docs.openlit.io/latest/sdk/overview)
* [Traceloop / OpenLLMetry](https://www.traceloop.com/docs/openllmetry/introduction)

#### When to use this option

This approach is well suited when:

* Your application uses an Agentic AI framework not listed in Option 1 
* The application is **already instrumented** with a third-party instrumentation library 
* You want to avoid re-instrumenting existing code

#### How it works 

Third-party libraries typically emit telemetry in their own formats or earlier OpenTelemetry schemas. 
To integrate this data with Splunk Observability Cloud:

1. Enable a **translation layer** that converts the emitted telemetry into the latest OpenTelemetry semantic conventions.
2. Configure the OpenTelemetry Collector to:
* Receive the translated data
* Export it to Splunk Observability Cloud

For step-by-step instructions, see:
[Translate and collect data from AI applications instrumented with third-party libraries](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-agent-monitoring/set-up-ai-agent-monitoring/translate-data-from-third-party-instrumentation-libraries).

### Summary 

| Scenario                             | Recommended Option                      | 
|--------------------------------------|-----------------------------------------|
| Supported framework, minimal setup   | Splunk OpenTelemetry Instrumentation    |
| Unsupported framework                | Third-party instrumentation library     |
| Existing third-party instrumentation | Third-party + OpenTelemetry translation |

