# VictorOps Getting Started - Lab Summary

1. Activate your login
2. Configure your Profile
3. Create your Team
4. Configure Rotations
5. Configure Escalation Policies
6. Create Routing Keys

---

## 1. Activate your login

You will have received an invitation to Activate your VictorOps account via e-mail, click the 'Activate Account' link and follow the prompts.

---

## 2. Configure Your Profile

Once you are logged in to VictorOps you now need to set up your profile.  Click on your login name in the top right hand corner and chose `Profile` from the drop down.

### 2.1. Contact Methods

Confirm your contact methods are listed correctly and add any additional phone numbers and e-mail address you wish to use.

### 2.2. Devices

Install the VictorOps app for your smartphone.  Search your phones App Store for VictorOps to find the appropriate version of the app.  The publisher should be listed as VictorOps Inc.

[![iPhone](../images/victorops/app-store.svg){: .appstore}](ttps://apps.apple.com/us/app/victorops/id696974262) [![Android](../images/victorops/play-store.svg){: .appstore}](https://play.google.com/store/apps/details?id=com.victorops.androidclient&hl=en)

Configuration help guides are available here:

* [Apple](https://help.victorops.com/knowledge-base/ios-application/)

* [Android](https://help.victorops.com/knowledge-base/android-devices-victorops/)

Install the App and login, then refresh the Profile page and your device should now be listed under the devices section.  Click the `Test push notification` button and confirm you receive the test message.

### 2.3. Personal Calendar

This link will enable you to sync your VictorOps on-call schedule with your calendar, however as you do not have any allocated shifts yet this will currently be empty. You can add it to you calendar by copying the link into your preferred application and setting it up as a new subscription.

### 2.4. Paging Polices

Paging Polices specify how you will be contacted by VictorOps when on-call. The Primary Paging Policy will have defaulted to sending you an SMS assuming you added your phone number when activating your account. We will now configure this policy into a three tier multi-stage policy.

Click the edit policy button for the Primary Paging Policy.  

* Step 1
  * Send a push notification to all my devices
  * Execute the next step if I have not responded within 5 minutes

Then add an new step

* Step 2
  * Send an email to [your email address]
  * Execute the next step if I have not responded within 5 minutes

Then add a new step

* Step 3
  * Every 5 minutes until we have reached you
  * Make a phone call to [your phone number]

Then save the policy.

When you are on-call or in the escalation path of an incident, you will receive notifications in this order following these time delays. To cease the paging you must acknowledge the incident. Acknowledgements can occur in one of the following ways:

* Expanding the Push Notification on your device and selecting Acknowledge
* Responding to the SMS with the 5 digit code included
* Pressing 4 during the Phone Call
* Slack Button

For more information on Notification Types, see [here](https://help.victorops.com/knowledge-base/notification-types/).

Custom paging polices enable you to override the primary policy based on the time and day of the week. A good example would be get the system to immediately phone you whenever you get a page during the evening or weekends as this is more likely to get your attention than a push notification.

Create a new Custom Policy by clicking `Add a Policy` and configure with the following settings:

Policy Name: Evening

* Step 1
  * Every 5 minutes until we have reached you
    * Make a phone call to [your phone number]
    * Time Period: All 7 Days
    * Timezone
      * [your time zone]
        * Between 7pm and 9am

Save the policy then add one more

Policy Name: Weekend

* Step 1
  * Every 5 minutes until we have reached you
    * Make a phone call to [your phone number]
    * Time Period: Sat & Sun
    * Timezone
      * [your time zone]
        * Between 9am and 7pm

These custom paging policies will be used during the specified times in place of the Primary Policy, however admins do have the ability to ignore these custom policies, and we will highlight how this is achieved in a later module.

The final option here is the setting for Recovery Notifications.  As these are typically low priority simply sending you an email is the typical setting used.

Your profile is now fully configured using these example configurations. Organizations will have different views on how profiles should be configured and will typically issue guidelines for paging policies and times between escalations etc.

---

## 3. Create Your Team

Navigate to the Teams Tab on the main toolbar, select `Add Team`, then enter your team name using the format "[Your Initials] Workshop" and then save by clicking the `Add Team` button.

You now need to add other users to your team.  If you are running this workshop using the Splunk provided environment, the following accounts are available for testing.  If you are running this lab in your own environment, you will have been provided a list of usernames you can use in place of the table below.

| Name | Username | Shift |
| --- | --- | --- |
| Duane Chow | duanechow | Europe |
| Steven Gomez | gomez | Europe |
| Walter White | heisenberg | Europe |
| Jim Halpert | jimhalpert | Asia |
| Lydia Rodarte-Quayle | lydia | Asia |
| Marie Schrader | marie | Asia |
| Maximo Arciniega | maximo | West Coast |
| Michael Scott | michaelscott | West Coast |
| Tuco Salamanca | tuco | West Coast |
| Jack Welker | jackwelker | 24/7 |
| Hank Schrader | hankschrader | 24/7 |
| Pam Beesly | pambeesly | 24/7 |

Add the users to your team, using either the above list or the alternate one provided to you. The value in the `Shift` column can be ignored for now, but will be required for a later step.

Click the `Invite User` button then either start typing the usernames (this will filter the list), or copy and paste them into the dialogue box. Once all users are added click the `Add User` button.

To make a team member a Team Admin, simply click the `Pencil` icon in the right hand column, pick any user and make them an Admin.

!!! tip
    For large team management you could use the API to streamline this process, and we will look at that in a later module

---

## 4. Configure Rotations

Navigate to the `Rotations` tab on the `Teams` sub menu, you should have no existing Rotations so we need to create some. The 1st Rotation you will create is for a follow the sun support pattern where the members of each shift provide cover during their normal working hours within their time zone.  The 2nd will be a Rotation used to provide escalation support by more experienced senior members of the team, based on a 24/7, 1 week shift pattern.

### 4.1. Follow the Sun Support - Business Hours

* Click `Add Rotation`
* Enter a name of "*Follow the Sun Support - Business Hours*"
* Select `Partial day` from the three available shift templates
  * Enter a Shift name of "*Asia*"
    * Time Zone set to "*Asia/Tokyo*"
    * Each user is on duty from "*Monday through Friday from 9.00am to 5.00pm*"
    * Handoff happens every "*7 days*"
    * The next handoff happens - Select the next Monday using the calendar
    * Click `Save Rotation`
* Now add an 2nd shift for Europe by clicking `+Add a shift` - `Partial Day`
  * Enter a Shift name of "*Europe*"
    * Time Zone set to "*Europe/London*"
    * Each user is on duty from "*Monday through Friday from 9.00am to 5.00pm*"
    * Handoff happens every "*7 days*"
    * The next handoff happens - Select the next Monday using the calendar
    * Click `Save Shift`
* Now add a 3rd shift for West Coast USA by clicking `+Add a shift` - `Partial Day`
  * Enter a Shift name of "*West Coast*"
    * Time Zone set to "*US/Pacific*"
    * Each user is on duty from "*Monday through Friday from 9.00am to 5.00pm*"
    * Handoff happens every "*7 days*"
    * The next handoff happens - Select the next Monday using the calendar
    * Click `Save Shift`
* You new need to add the users into their allocated shift patterns using either the table above, or the list of users provided to you separately
  * For each Shift, click on the `Manage Members` icon which is the left of the three icons and resembles the image of three heads
    * Add the users to each Shift (note how you have to use their Username and not their real names)
    * The first user added will be the 'current' user for that shift
    * You can re-order the shifts by simply dragging the users up and down, and you can change the current user by clicking `Set Current` on an alternate user

You will now have three different Shift patterns, that provide cover 24hr hours, Mon - Fri, but with no cover at weekends.

We will now add the 2nd Rotation for our Senior SRE Escalation cover.

### 4.2. Senior SRE Escalation

* Click `Add Rotation`
* Enter a name of "*Senior SRE Escalation*"
* Select `24/7` from the three available shift templates
  * Enter a Shift name of "*Senior SRE Escalation*"
    * Time Zone set to "*Asia/Tokyo*"
    * Handoff happens every "*7 days at 9.00am*"
    * The next handoff happens [select the next Monday from the date picker]
    * Click `Save Rotation`
* Add the users who are allocated the 24/7 shift

That completes the configuration of the Rotations, we now need to configure the Escalation Policies and Routing Keys.

---

## 5. Configure Escalation Policies

Navigate to the Escalation Polices tab on the Teams sub menu, you should have no existing Polices so we need to create some.  We are going to create three different Polices to cover off three typical use cases.

### 5.1. 24/7

* Click `Add Escalation Policy`
* Policy Name: "*24/7*"
* Step 1
  * `Immediately`
    * `Notify the on-duty user(s) in rotation` → `Senior SRE Escalation`
* Click `Save`

### 5.2. Primary

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

### 5.3. Waiting Room

* Click `Add Escalation Policy`
* Policy Name: "*Waiting Room*"
* Step 1
  * `If still unacked after 10 more minutes`
    * `Execute Policy` → `[Your Team Name] : Primary`
* Click `Save`

You may have noticed that when we created each policy there was the warning message `There are no routing keys for this policy - it will only receive incidents via manual reroute or when on another escalation policy`

This is because there are no Routing Keys linked to these Escalation Polices, so now that we have these polices configured we can go and create the Routing Keys.

---

## 6. Create Routing Keys

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
