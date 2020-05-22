# Create Routing Keys

Routing Keys map the incoming alert messages from your monitoring system to an Escalation Policy which in turn sends the notifications to the appropriate team.

In order to get your unique Routing Key run the following command:

=== "Input"

    ```bash
    echo $INSTANCE
    ```

=== "Example Output"

    ```text
    rnje
    ```

Copy this 4 character string to your clipboard.

Navigate to Settings on the main menu bar. You'll be dropped into the Routing Key configuration by default.

There will probably already be a number of Routing Keys configured, but to add a new one simply click **Add Key**

Next, enter the name for the key in the empty box in the **Routing Key** column.

Then select the appropriate policy from the drop down in the **Escalation Polices** column.

Replace {==INSTANCE==} with the 4 characters from above and replace {==TEAM_NAME==} with the team you created earlier.

Create the following two Routing Keys:

| Routing Key | Escalation Policies |
| --- | --- |
| {==INSTANCE==}_PRI | {==TEAM_NAME==} : Primary |
| {==INSTANCE==}_WR | {==TEAM_NAME==} : Waiting Room |

!!! note
    You can assign a Routing Key to multiple Escalation Policies if required by simply selecting more from the list

If you now navigate back to **Teams → [Your Team Name] → Escalation Policies** and look at the settings for your **Primary** and **Waiting Room** polices.

You will see that these now have **Routes** assigned to them.

The **24/7** policy does not have a Route assigned as this will only be triggered via an **Execute Policy** escalation from the **Primary** policy.

---

This completes the initial getting started steps for VictorOps, the next step will be to configure the Integration between VictorOps and SignalFx.
