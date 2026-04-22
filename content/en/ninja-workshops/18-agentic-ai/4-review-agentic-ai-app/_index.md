---
title: Agentic AI Application Architecture
linkTitle: 4. Agentic AI Application Architecture
weight: 4
time: 15 minutes
---

## Application Overview

This workshop utilizes an **Agentic AI** application for booking travel. 
Before we instrument the application with **OpenTelemetry**, it helps to 
understand how the application works.

![Application Architecture](../images/travel-planner-app-architecture.jpg)

The application is a **Flask API** that accepts a travel planning request and runs it through 
a **LangGraph** workflow made up of several LangChain-powered LLM nodes. Each node plays a specific 
role, updates shared state, and hands off to the next step.

In this part of the workshop, we will review:

* the request lifecycle 
* the shared state model 
* how LangGraph nodes work 
* the LangChain abstractions used in the code 
* where observability will matter later

Navigate to the subsections to learn more about the application architecture and implementation.