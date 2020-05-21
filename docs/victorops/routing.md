# Create Routing Keys

Routing Keys map the incoming alert messages from your monitoring system to an Escalation Policy which in turn sends the notifications to the appropriate team.

Navigate to Settings on the main menu bar. You'll be dropped into the Routing Key configuration by default.

There will probably already be a number of Routing Keys configured, but to add a new one simply click `Add Key` then enter the name for the key in the empty box in the `Routing Key` column, and then select the appropriate policy from the drop down in the `Escalation Polices` column. Create the following two Routing Keys:

| Routing Key | Escalation Policies |
| --- | --- |
| [Your Initials]_PRI | [Your Team Name] : Primary |
| [Your Initials]_WR | [Your Team Name] : Waiting Room |

!!! note
    You can assign a Routing Key to multiple Escalation Policies if required by simply selecting more from the list

If you now navigate back to `Teams` → `[Your Team Name]` → `Escalation Policies` and look at the settings for your `Primary` and `Waiting Room` polices you will see that these now have `Routes` assigned to them.  The `24/7` policy does not have a Route assigned as this will only be triggered via an `Execute Policy` escalation from the `Primary` policy.

---

This completes the initial getting started steps for VictorOps, the next step will be to configure the Integration between VictorOps and SignalFx.
