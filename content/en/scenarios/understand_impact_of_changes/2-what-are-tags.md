---
title: What are Tags?
linkTitle: 2 What are Tags? 
weight: 2
time: 3 minutes
---

To understand why some requests have errors or slow performance, we'll need to add context to our traces. We'll do this by adding tags. But first, let's take a moment to discuss what tags are, and why they're so important for observability.

## What are tags?

Tags are key-value pairs that provide additional metadata about spans in a trace, allowing you to enrich the context of the spans you send to Splunk APM.

For example, a payment processing application would find it helpful to track:

* The payment type used (i.e. credit card, gift card, etc.)
* The ID of the customer that requested the payment

This way, if errors or performance issues occur while processing the payment, we have the context we need for troubleshooting.

While some tags can be added with the OpenTelemetry collector, the ones we’ll be working with in this workshop are more granular, and are added by application developers using the OpenTelemetry API.

## Attributes vs. Tags

A note about terminology before we proceed. While this workshop is about **tags**, and this is the terminology we use in **Splunk Observability Cloud**, OpenTelemetry uses the term **attributes** instead. So when you see tags mentioned throughout this workshop, you can treat them as synonymous with attributes.

## Why are tags so important?

Tags are essential for an application to be truly observable. As we saw with our credit check service, some users are having a great experience: fast with no errors. But other users get a slow experience or encounter errors.  

Tags add the context to the traces to help us understand why some users get a great experience and others don't.  And powerful features in **Splunk Observability Cloud** utilize tags to help you jump quickly to root cause.

## Sneak Peak: Tag Spotlight

**Tag Spotlight** uses tags to discover trends that contribute to high latency or error rates: 

![Tag Spotlight Preview](../images/tag_spotlight_preview.png)

The screenshot above provides an example of Tag Spotlight from another application.

Splunk has analyzed all of the tags included as part of traces that involve the payment service.

It tells us very quickly whether some tag values have more errors than others.

If we look at the version tag, we can see that version 350.10 of the service has a 100% error rate, whereas version 350.9 of the service has no errors at all: 

![Tag Spotlight Preview](../images/tag_spotlight_preview_details.png)

We’ll be using Tag Spotlight with the credit check service later on in the workshop, once we’ve captured some tags of our own.
