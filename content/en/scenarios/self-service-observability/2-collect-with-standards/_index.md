---
title: Collect Data with Standards
linkTitle: 2 Collect Data with Standards
weight: 2
time: 10 minutes
---

## Introduction

For this workshop, we'll be doing things that only a central tools or administration would do.

The workshop uses scripts to help with steps that aren't part of the focus of this workshop -- like how to change a kubernetes app, or start an application from a host.

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}
It can be useful to review what the scripts are doing.

So along the way it is advised to run `cat <filename>` from time to time to see what that step just did.

The workshop won't call this out, so do it when you are curious.
{{% /notice %}}

We'll also be running some scripts to simulate data that we want to deal with.

A simplified version of the architecture (leaving aside the specifics of kubernetes) will look something like the following:

![Architecture](images/arch.png)

* The **App** sends metrics and traces to the **Otel Collector**
* The **Otel Collector** also collects metrics of its own
* The **Otel Collector** adds metadata to its own metrics and data that passes through it
* The **OTel Gateway** offers another opportunity to add metadata

Let's start by deploying the gateway.