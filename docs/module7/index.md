## Victor Ops Getting Started

### Lab Summary
* Activate your login
* Configure your Profile
* Create your Team
* Configure Rotations
* Configure Escalation Policies
* Create a Routing Key
* Launch test VMs & Monitor with SignalFx

---

### 1. Activate your login
You will have received an invitation to Activate your VictorOps aaccount via e-mail, click the 'Activate Account' link and follow the prompts.

---

### 2. Configure Your Profile
Once you are logged in to VictorOps you now need to setup your profile.  Click on your login name in the top right hand corner and chose 'Your Profile' from the drop down.

#### Contact Methods
Confirm your contant methods are listed correctly and add any addiontal phone numbers and e-mail address you wish to use.

#### Devices
Install the VictorOps app for your smartphone.  Search your phones App Store for VictorOps to find the appropriate version of the app.  The publisher should be listed as VictorOps Inc.

Configuration help guides are available here:

* [Apple](https://help.victorops.com/knowledge-base/ios-application/) 

* [Android](https://help.victorops.com/knowledge-base/android-devices-victorops/)

Install the App and login, then refresh the Profile page and your device should now be listed under the devices section.  Click the "Test push notification" button and confirm you recieve the test message.

#### Personal Calendar
This link will enable you to sync your VictorOps on-call schedule with your calendar, however as you do not have any allocated shifts yet this will currently be empty. You can add it to you celendar by copying the link into your preferred appliction and seting it up as a new subscritpion.

#### Paging Polices
Paging Polices specify how you will be contacted by VictorOps when on-call. The Primary Paging Policy will have defaulted to sending you an SMS assuming you added your phone number when activating your account. We will now configure this policy into a three tier multi-stage policy.

Click the edit policy button for the Primary Paging Policy.  

* Step 1
    - Every 5 minutes until we have reached you
    - Send a push notification to all my devices
    - Execute the next step if I have not responded within 5 minutes

Then add an new step

* Step 2
    - Send an email to &lt;your email address&gt;
    - Execute the next step if I have not responded within 5 minutes

Then add a new step

* Step 3
    - Every 5 minutes until we have reached you
    - Make a phone call to &lt;your phone number&gt;

Then save the policy

Reviewing what we have just created, you will initally get paged using your smart phone, if you have not acknowledged within 5 minutes the policy will move on to the next step. Step 2 will send you an e-mail, but will also repeat Step 1 so you will get another push notification to your smart phone, then wait for 5 minutes for an acknowledgement before again escalating to the next step. Step 3 will phone you every 5 minutes until acknowledged, and will also send a push notification and email.

Custom paging polices enable you to overide the primary policy based on the time and day of the week. A good example would be get the system to immediately phone you whenever you get a page during the evening or weekends as this is more likely to get your attention than a push notification.

Create a new Custom Policy by clicking Add a Policy and configure with the following settings:

Policy Name: Evening

* Step 1
    * Every 5 minutes until we have reached you
    * Make a phone call to &lt;your phone number&gt;
    * Time Period: All 7 Days
    * Timezone
        *  &lt;your time zone&gt;
        *  Between 7pm and 9am

Save the policy then add one more

Policy Name: Weekend

* Step 1
    * Every 5 minutes until we have reached you
    * Make a phone call to &lt;your phone number&gt;
    * Time Period: Sat & Sun
    * Timezone
        *  &lt;your time zone&gt;
        *  Between 9am and 7pm

These custom paging policies will be used during the specified times in place of the Primary Policy, however admins do have the abiltiy to ignore these custom policies, and we will highlight how this is achieved in a later module.

The final option here is the setting for Recovery Notifications.  As these are typically low priority simply sending you an email is the typical setting used.

Your profile is now fully configured using these example configurations. Organisations will have different views on how profiles should be configured and will typically issue guidelines for paging policies and times between escallations etc.

---

### 3. Create Your Team
Navigate to the Teams Tab on the main toolbar, select 'Add Team', then enter your team name using the format '&lt;Your Initals&gt; Workshop' and then save by clicking the 'Add Team' button.

INSERT SCREEN SHOT HERE

You now need to add other users to your team.  If you are running this workshop using the Splunk provided envrionment, the following accounts are available for testing.  If you are running this lab in your own environment, you will have been provided a list of usernames you can use in place of the table below.

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

Add the users to your team, using either the above list or the alternate one provided to you. The value in the Shift column can be ignored for now, but will be required for a later step.

Click the Invite User button then either start typing the usernames (this will filter the list), or copy and paste them into the dialogue box. Once all users are added click the 'Add User' button.

To make a team member a Team Admin, simply click the Pencil icon in the right hand column, pick any user and make them an Admin.

!!!tip
For large team managment you could use the API to streamline this process, and we will look at that in a later module

---

### 3. Configure Rotations 
Navigate to the Rotations tab on the Teams sub menu, you should have no existing Rotations so we need to create some. The 1st Rotation you will create is for a follow the sun support pattern where the members of each shift provide cover during their normal working hours within their time zone.  The 2nd will be a Rotation used to provide escalation support by more experienced senior members of the team, based on a 24/7, 1 week shift pattern.

* Follow the Sun Support - Business Hours
    * Click 'Add Rotation'
    * Enter a name of Follow the Sun Support - Business Hours
    * Select 'Partial day' from the three available shift templates
        * Enter a Shift name of Asia
        * Time Zone set to Asia/Tokyo
        * Each user is on duty from 'Monday through Friday from 9.00am to 5.00pm'
        * Handoff happens every 1 days
        * The next handoff happens &lt;the next Monday will have been automatically selected&gt;
        * Save Rotation
    * Now add an 2nd shft for Asia by clicking '+Add a shift'
        * Enter a Shift name of Europe
        * Time Zone set to Europe/London
        * The remaining settings will have been copied from the 1st shift
        * Save Shift
    * Now add a 3rd shft for West Coast USA by clicking '+Add a shift'
        * Enter a Shift name of West Coast
        * Time Zone set to US/Pacific
        * The remaining settings will have been copied from the 1st shift
        * Save Shift
    * You new need to add the users into their allocated shift patterns using either the table above, or the list of users provided to you separately
        * For each Shift, click on the 'Manage Members' icon which is the left of the three icons and resembles the image of three heads
        * Add the users to each Shift (note how you have to use their Username and not their real names)
        * The first user added will the 'current' user for that shift
        * You can re-order the shifts by simply dragging the users up and down, and you can change the current user by clicking 'Set Current' on an alternate user

You will now have three different Shift patterns, that provide cover 24hr hours, Mon - Fri, but with no cover at weekends.

We will now add the 2nd Rotation for our Senior SRE Escalation cover.

* Senior SRE Escalation
    * Click 'Add Rotation'
    * Enter a name of Senior SRE Escalation
    * Select '24/7 from the three available shift templates
        * Enter a Shift name of Senior SRE Escalation
        * Time Zone set to Asia/Tokyo
        * andoff happens every 7 days at 9.00am
        * The next handoff happens &lt;select the next Monday from the date picker&gt;
        * Save Rotation
    * Add the users who are allocated the 24/7 shift


