---
title: Configuration
weight: 2
---

## Configure the Infrastructure Add-on and the Observability Content Pack

Now that we have access to our instances, have the Infrastructure Monitoring Add-On and the Observability Content Pack pre-installed, we need to configure them by following the steps below.

### Configuration of the Infrastructure Monitoring Add-on

After you accessed your instance, navigate to the **Splunk Infrastructure Monitoring Add-On** listed on the left under **Apps**. We want to set up an account, and we can do so by navigating to the **Configuration Tab** and clicking on the '**Connect an Account**'-Button.

![Connect Account](../../images/im_configure/account.png)

Once you clicked the 'Connect an Account'-Button, a dialogue appears, prompting you for the user credentials of your Observability Cloud account. These are the **Access Token** and the **Realm**, with which the Add-On can access the Oberservability Cloud. In the next steps, we are going to locate our Realm inside our individual Observability Cloud account and create a new Access Token.

Locate your **Realm**: Log in to your Splunk Observability account. In the menu on the left on the bottom click on the little gear icon (Settings). On the very top of this menu, you should see your **username** right next to a profile picture. Click on it. You are now in the Account Settings, where you can find the Realm *(see screenshot below)*.

![Account Settings](../../images/im_configure/account_settings.png)

Copy and paste the Realm into the input field of of the dialogue in the IM Add-On.

Locate your **Access Token**: Being still in your Account Settings, click on **Generate User API Access Token** to generate an access token, and subsequently on **Show User API Access Token** to show the associated string. Copy and paste that string into the input field of of the dialogue in the IM Add-On.

Once the Realm and Access Token have been inserted into the input dialogue, make sure to verify whether or not a connection to the Observability Cloud could be established by clicking on the **Check Connection**-button. If so, click submit. You can enable data collection for the account by selecting the *Data Collection* toggle.

*For additional information on this topic, see [Configure the Splunk Infrastructure Monitoring Add-on](https://docs.splunk.com/Documentation/SIMAddon/1.2.1/Install/Configure).*

*Watch this video introducing the content pack concepts.

<iframe class="vidyard_iframe" src="//play.vidyard.com/cB6Wq1dEy7hZGm7CjdSZm6.html?" width="640" height="360" scrolling="no" frameborder="0" allowtransparency="true" allowfullscreen></iframe>

### Configure the Content Pack for Observability

As soon as we have successfully configured the Infrastructure Monitoring Add-On, we will continue by installing and configuring the Content Pack for Observability. The first step to accomplish that is to select the **IT Service Intelligence** app. Inside the app, click on the **Configuration** tab and select **Data Integrations** from the dopdown menu.

![Data Integrations](../../images/im_configure/data_integrations.png)

On the next screen, select *Add content packs* and choose *Splunk Observability Cloud*.

![Add](../../images/cp_configure/add.png)

Upon clicking on the *Splunk Observability Cloud*-tile, you are presented with an overview of what is included in the Content Pack. Review it, and finally click on

![Proceed Button](../../images/cp_configure/proceed_button.png)

Next, you are presented with a settings menu to configure the content pack. **The following is important:** Please disable the *Import as enable*-option, leave the *Enter a prefix* input field blank, and disable the *Backfill service KPIs* option.

![Settings](../../images/cp_configure/settings.png)

Finally, click on the [Install selected] button.

The *Splunk Observability Cloud* tile on the *Data Integrations* page should now have a little green checkmark on the upper right corner. This means that we are all set. Perfect!

![Checkmark](../../images/cp_configure/checkmark.png)

*For additional information on this topic, see [Install the Content Pack for Splunk Observability Cloud](https://docs.splunk.com/Documentation/CPObservability/1.0.0/CP/Install#Install_the_Content_Pack_for_Splunk_Observability_Cloud).*
