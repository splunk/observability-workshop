## Victor Ops Getting Started

### Lab Summary
* Activate your login
* Configure your profile
* Create routing key

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

### 3. Create Routing Key
