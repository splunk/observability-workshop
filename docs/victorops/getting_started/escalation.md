# Configure Escalation Policies

Navigate to the Escalation Polices tab on the Teams sub menu, you should have no existing Polices so we need to create some.  We are going to create three different Polices to cover off three typical use cases.

## 24/7

* Click `Add Escalation Policy`
* Policy Name: "*24/7*"
* Step 1
  * `Immediately`
    * `Notify the on-duty user(s) in rotation` → `Senior SRE Escalation`
* Click `Save`

## Primary

* Click `Add Escalation Policy`
* Policy Name: "*Primary*"
* Step 1
  * `Immediately`
    * `Notify the on-duty user(s) in rotation` → `Follow the Sun Support - Business Hours`
    * Click `Add Step`
* Step 2
  * `If still unacked after 15 minutes`
    * `Notify the next user(s) in the current on-duty shift` → `Follow the Sun Support - Business Hours`
    * Click `Add Step`
* Step 3
  * `If still unacked after 15 more minutes`
    * `Execute Policy` → `[Your Team Name] : 24/7`
* Click `Save`

## Waiting Room

* Click `Add Escalation Policy`
* Policy Name: "*Waiting Room*"
* Step 1
  * `If still unacked after 10 more minutes`
    * `Execute Policy` → `[Your Team Name] : Primary`
* Click `Save`

You may have noticed that when we created each policy there was the warning message `

!!! warning
    There are no routing keys for this policy - it will only receive incidents via manual reroute or when on another escalation policy

This is because there are no Routing Keys linked to these Escalation Polices, so now that we have these polices configured we can go and create the Routing Keys.
