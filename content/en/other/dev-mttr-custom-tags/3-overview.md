---
title: Overview of the Workshop
linkTitle: 3. Overview
weight: 3
---

## Users and Workflows

As we go through this workshop we will be switching roles from SRE to Developer. First we will start with alert responders or SREs who will identify an issue in Splunk Observability UI. Next, we will jump to a Developer Role to see how a Developer will debug and repair/fix a software problem using trace data provided by our SRE.

Of course, we are not requiring 2 people for this workshop as each participant will play both roles.

## Today we will learn

Today we will learn how Splunk APM with Full Fidelity tracing can accelerate the time to repair for Development teams. We will focus on the full fidelity data ( In the form of traces ) that an SRE or alert responder would send to a developer to then repair/fix software. We will do this with both Auto-Instrumentation data and Custom attributes or Custom Tags, via Manual Instrumentation data.

While we will be spending time Debugging code, .... Don't worry, ...there is no programming experience necessary, as our goal here is for every participant to understand how using Custom Attributes/Tags in Splunk APM @ Full Fidelity accelerates Mean Time to Repair Software problems for Development Teams.

## Important Definitions

Let's define a few terms for those new to APM / Software Development or Java

* What Are Custom Attributes / Custom Tags in Splunk APM ?

First, you will hear poeple refer to Custom Attributes in the context of Splunk Enterprise, however in Splunk APM Custom Attributes are called Custom Tags as defined in Opentelemetry and shown in Splunk APM Tag Splotlight.

* What is a Function or a method in Java?

A Function in most languages, including Java, is a logical chunk of code that -- when executed -- solves a repeatable task. This is basically what development teams spend thier time building and where software issues will most commonly be.

* What is an Exception in Java?

An exception is an exceptional error condition that indicates abonormal behavior, or an unhandled condition, that interrupts program execution abnormally.
