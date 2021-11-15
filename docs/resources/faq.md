# Frequently Asked Questions

A collection of the common questions and their answers associated with Observability, DevOps, Incident Response and Splunk On-Call.

## Q: Alerts v. Incident Response v. Incident Management

A: Alerts, Incident Response and Incident Management are related functions. Together they comprise the incident response and resolution process.

Monitoring and Observability tools send alerts to incident response platforms. Those platforms take a collection of alerts and correlate them into incidents.

Those incidents are recorded into incident management (ITSM) platforms for record. Alerts are the trigger that something has happened, and provide context to an incident.

Incidents consist of the alert payload, all activity associated with the incident from the time it was created, and the on-call policies to be followed. ITSM is the system of record for incidents that are active and after they have been resolved.

All these components are necessary for successful incident response and management practices.

**On-Call**{: .label-button .oncall}

## Q: Is Observability Monitoring

A: The key difference between Monitoring and Observability is the difference between “known knowns” and “unknown knowns” respectively.

In monitoring the operator generally has prior knowledge of the architecture and elements in their system. They can reliably predict the relationship between elements, and their associated metadata. Monitoring is good for stateful infrastructure that is not frequently changed.

Observability is for systems where the operators ability to predict and trace all elements in the system and their relationships is limited.

Observability is a set of practices and technology, which include traditional monitoring metrics.

These practices and technologies combined give the operator the ability to understand ephemeral and highly complex environments without prior knowledge of all elements of a system. Observability technology can also account for fluctuations in the environment, and variation in metadata (cardinality) better than traditional monitoring which is more static.

**Observability**{: .label-button .observability}

## Q: What are Traces and Spans

A: Traces and spans, combined with metrics and logs, make up the core types of data that feed modern Observability tools. They all have specific elements and functions, but work well together.

Because microservices based architectures are distributed, transactions in the system touch multiple services before completing. This makes accurately pinpointing the location of an issue difficult. Traces are a method for tracking the full path of a request through all the services in a distributed system. Spans are the timed operations in each service. Traces are the connective tissue for the spans and together they give more detail on individual service processes. While metrics give a good snapshot of the health of a system, and logs give depth when investigating issues, traces and spans help navigate operators to the source of issues with greater context. This saves time when investigating incidents, and supports the increasing complexity of modern architectures.

**APM**{: .label-button .apm}

## Q: What is the Sidecar Pattern

A: The sidecar pattern is a design pattern for having related services contected directly by infrastructure. Related services can be adding functionality or supporting the application logic they are connected to. It is used heavily as a method for deploying agents associated with the management plan along with the application service they support.

In Observability the sidecar services are the application logic, and the agent collecting data from that service. The setup requires two containers one with the application service, and one running the agent. The containers share a pod, and resources such as disk, network, and namespace. They are also deployed together and share the same lifecycle.

**Observability**{: .label-button .observability}
