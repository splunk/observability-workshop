---
title: Conclusion
linkTitle: 7. Conclusion
weight: 7
---

Congratulations on finishing the Lambda Tracing Workshop! You have seen how we can complement auto-instrumentation with manual steps to have the `producer-lambda` function's context be sent to the `consumer-lambda` function via a record in a Kinesis stream. This allowed us to build the expected Distributed Trace, and to contextualize the relationship between both functions in Splunk APM.

![Lambda application, fully instrumented](../images/13-Architecture_Instrumented.png)

You can now build out a trace manually by linking two different functions together. This comes in handy when your auto-instrumentation, or 3rd-party systems, do not support context propagation out of the box, or when you wish to add custom attributes to a trace for more relevant trace analaysis.
