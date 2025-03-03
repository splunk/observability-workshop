---
title: OpenTelemetry Collector Development
linkTitle: 8. Develop
weight: 8
---

## Developing a custom component

Building a component for the Open Telemetry Collector requires three key parts:

1. The Configuration - _What values are exposed to the user to configure_
1. The Factory - _Make the component using the provided values_
1. The Business Logic - _What the component needs to do_

For this, we will use the example of building a component that works with Jenkins so that we can track important DevOps metrics of our project(s).

The metrics we are looking to measure are:

1. Lead time for changes - _"How long it takes for a commit to get into production"_
1. Change failure rate   - _"The percentage of deployments causing a failure in production"_
1. Deployment frequency  - _"How often a [team] successfully releases to production"_
1. Mean time to recover  - _"How long does it take for a [team] to recover from a failure in production"_

These indicators were identified Google's DevOps Research and Assesment (DORA)[^1] team to help
show performance of a software development team. The reason for choosing _Jenkins CI_ is that we remain in the same Open Source Software ecosystem which we can serve as the example for the vendor managed CI tools to adopt in future.

## Instrument Vs Component

There is something to consider when improving level of Observability within your organisation
since there are some trade offs that get made.

| | Pros | Cons |
| ----- | ----- | ----- |
| **(Auto) Instrumented** | Does not require an external API to be monitored in order to observe the system. | Changing instrumentation requires changes to the project. |
| | Gives system owners/developers to make changes in their observability. | Requires additional runtime dependancies. |
| | Understands system context and can corrolate captured data with _Exemplars_. | Can impact performance of the system. |
| **Component** | - Changes to data names or semantics can be rolled out independently of the system's release cycle. | Breaking API changes require a coordinated release between system and collector. |
| | Updating/extending data collected is a seemless user facing change. | Captured data semantics can unexpectedly break that does not align with a new system release. |
| | Does not require the supporting teams to have a deep understanding of observability practice. | Strictly external / exposed information can be surfaced from the system. |
