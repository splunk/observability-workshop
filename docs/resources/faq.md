# Frequently Asked Questions

A collection of the common questions and their answers associated with Observability, DevOps, Incident Response, SignalFx and VictorOps.

## Q: Alerts v. Incident Response v. Incident Management

A: Alerts, Incident Response and Incident Management are related functions. Together they comprise the incident response and resolution process.

Monitoring and Observability tools send alerts to incident response platforms. Those platforms take a collection of alerts and correlate them into incidents.

Those incidents are recorded into incident management (ITSM) platforms for record. Alerts are the trigger that something has happened, and provide context to an incident.

Incidents consist of the alert payload, all activity associated with the incident from the time it was created, and the on-call policies to be followed. ITSM is the system of record for incidents that are active and after they have been resolved.

All these components are necessary for successful incident response and management practices.

**VictorOps**{: .label-button .victorops}

## Q: Is Observability Monitoring

A: The key difference between Monitoring and Observability is the difference between “known knowns” and “unknown knowns” respectively.

In monitoring the operator generally has prior knowledge of the architecture and elements in their system. They can reliably predict the relationship between elements, and their associated metadata. Monitoring is good for stateful infrastructure that is not frequently changed.

Observability is for systems where the operators ability to predict and trace all elements in the system and their relationships is limited.

Observability is a set of practices and technology, which include traditional monitoring metrics.

These practices and technologies combined give the operator the ability to understand ephemeral and highly complex environments without prior knowledge of all elements of a system. Observability technology can also account for fluctuations in the environment, and variation in metadata (cardinality) better than traditional monitoring which is more static.

**SignalFx**{: .label-button .signalfx}
