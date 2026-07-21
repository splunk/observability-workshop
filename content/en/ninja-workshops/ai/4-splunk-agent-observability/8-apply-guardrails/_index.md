---
title: Apply Guardrails at Runtime
linkTitle: 8. Apply Guardrails at Runtime
weight: 8
time: 15 minutes
---

Observing, measuring, and testing are essential, but when an answer could harm a patient,
you need to *act in the moment*. **Guardrails** (agent controls) evaluate each step at runtime
and either **block** it or **steer** the agent toward a safe response.

{{% notice title="Persona" style="orange" icon="user" %}}

As Careful Health Provider's **AI engineer**, you've now seen the assistant produce ungrounded
medical advice and call a sensitive deletion tool. Detection isn't enough; you need to *stop*
the dangerous deletion and *redirect* the unsafe answer, in production, without taking the
agent offline.

{{% /notice %}}

> [!splunk] **Agent Control is your single watchtower across every agent.** Enforce control
> policies with runtime **blocking and steering**, and push policy changes that stop unwanted
> behavior in **seconds**, without redeploying or taking agents offline.

{{% notice title="Block vs. steer" style="info" %}}

* **Block**: the step is rejected outright. In the app this surfaces as a
  `ControlViolationError`, and the user receives a safe "this action was blocked" message.
  *Use it for the irreversible patient-record deletion.*
* **Steer**: the step is sent back for revision with guidance. In the app this surfaces as a
  `ControlSteerError`; the agent retries using the steering guidance before giving up. *Use it
  to redirect an unsafe medical answer into a safe one rather than refusing the user
  entirely.*

{{% /notice %}}

{{% notice title="Where to work" style="info" %}}

This chapter works in `~/workshop/healthcare-assistant/4-app-with-controls`. It builds on the
instrumented app and adds the Agent Control SDK, configuration, and the `@control`-decorated
steps. The folder ships complete, so it doubles as the reference for this chapter.

{{% /notice %}}

Continue to the subsections to add Agent Control, define controls, and test block and steer.
