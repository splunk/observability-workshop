---
title: 4. Human-in-the-Loop Operations
weight: 4
---

AI-assisted remediation should reduce toil and shorten MTTR, but it should not bypass accountability. Advanced teams define where AI can suggest, where humans must approve, and how learning feeds back into future incidents.

{{% notice title="Exercise" style="green" icon="running" %}}

Design a human-in-the-loop policy for the alert scenario you investigated.

* Define who owns each decision:

| Decision | Owner |
|----------|-------|
| Incident severity | |
| Root cause accepted | |
| Diagnostic command approved | |
| Production change approved | |
| Rollback approved | |
| Alert resolved | |
| Follow-up work created | |

* Decide which plan steps can be executed by any responder and which require service-owner approval.
* Add policy language to your incident brief:

```text
AI-generated recommendations are hypotheses until validated by telemetry and approved by the responsible owner. State-changing remediation requires explicit approval and a rollback plan.
```

* Use feedback controls on the AI investigation when the result is helpful or unhelpful.
* Capture at least one runbook improvement that would make the next incident faster.

{{< tabs >}}
{{% tab title="Question" %}}
**Where does AI add the most value in a mature incident process?**
{{% /tab %}}
{{% tab title="Answer" %}}
**It accelerates correlation, hypothesis generation, and guided diagnostics while humans retain ownership of risk decisions and production changes.**
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

## Operating Model

| AI can accelerate | Humans must own |
|-------------------|-----------------|
| Finding related evidence | Severity and communication decisions |
| Ranking suspected root causes | Acceptance or rejection of a root cause |
| Generating diagnostic steps | Production access and command execution |
| Summarizing completed actions | Rollback, closure, and post-incident commitments |

