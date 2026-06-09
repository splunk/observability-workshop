---
title: 2. Execute Guarded Steps
weight: 2
---

The remediation plan can suggest commands or code blocks, including Kubernetes commands. Copying and running a suggested command is still an operational change. Treat every step like a peer-reviewed runbook action.

{{% notice title="Exercise" style="green" icon="running" %}}

Before running any command:

* Confirm your Kubernetes context and namespace.

```bash
kubectl config current-context
kubectl config view --minify --output 'jsonpath={..namespace}'; echo
```

* Prefer read-only checks first.

```bash
kubectl get pods -n <namespace> -o wide
kubectl describe pod <pod-name> -n <namespace>
kubectl get events -n <namespace> --sort-by=.lastTimestamp
```

* If the plan suggests a state-changing command, pause and answer:
  * What resource will change?
  * Which users or services could be affected?
  * What is the rollback command?
  * Who approved the action?
* Run the approved command in the correct environment.
* Copy the command output back into the remediation plan when prompted.
* Mark the step as completed only after the command or action succeeds.
* If a step has the wrong effect, use the plan's undo capability where appropriate and record the rollback in the incident brief.

{{< tabs >}}
{{% tab title="Question" %}}
**Why does the plan ask you to submit command output?**
{{% /tab %}}
{{% tab title="Answer" %}}
**The output gives the plan current evidence so it can decide whether the hypothesis is confirmed, needs another diagnostic step, or should be abandoned.**
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

{{% notice title="Production Safety" style="info" %}}
Never paste secrets, tokens, customer data, or private keys into the action plan. Redact sensitive output and use normal incident approval processes before executing state-changing remediation in production.
{{% /notice %}}

