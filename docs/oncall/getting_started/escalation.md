# Configure Escalation Policies

Navigate to the Escalation Polices tab on the Teams sub menu, you should have no existing Polices so we need to create some.

![No Escalation Policies](../../images/victorops/no-escalation.png){: .center}

We are going to create the following Polices to cover off three typical use cases.

![Escalation Policies](../../images/victorops/escalation-policies.png){: .zoom}

## 1. 24/7 Policy

Click **Add Escalation Policy**

* Policy Name: 24/7
* Step 1
* Immediately
  * Notify the on-duty user(s) in rotation → Senior SRE Escalation
  * Click **Save**

![24/7 Escalation Policy ](../../images/victorops/24-7-escalation-policy.png){: .zoom}

## 2. Primary Policy

Click **Add Escalation Policy**

* Policy Name: Primary
* Step 1
* Immediately
* Notify the on-duty user(s) in rotation → Follow the Sun Support - Business Hours
* Click **Add Step**

![Pri Escalation Policy Step 1](../../images/victorops/pri-escalation-policy-step-1.png){: .zoom}

* Step 2
* If still unacked after 15 minutes
* Notify the next user(s) in the current on-duty shift → Follow the Sun Support - Business Hours
* Click **Add Step**

![Pri Escalation Policy Step 2](../../images/victorops/pri-escalation-policy-step-2.png){: .zoom}

* Step 3
* If still unacked after 15 more minutes
* Execute Policy → [Your Team Name] : 24/7
* Click **Save**

![Pri Escalation Policy Step 3](../../images/victorops/pri-escalation-policy-step-3.png){: .zoom}

## 3. Waiting Room Policy

Click **Add Escalation Policy**

* Policy Name: Waiting Room
* Step 1
* If still unacked after 10 more minutes
* Execute Policy → [Your Team Name] : Primary
* Click **Save**

![WR Escalation Policy](../../images/victorops/wr-escalation-policy.png){: .zoom}

You should now have the following three escalation polices:

![Escalation Policies](../../images/victorops/escalation-policies.png){: .zoom}

You may have noticed that when we created each policy there was the following warning message:

!!! warning
    There are no routing keys for this policy - it will only receive incidents via manual reroute or when on another escalation policy

This is because there are no Routing Keys linked to these Escalation Polices, so now that we have these polices configured we can go and create the Routing Keys.
