---
title: Workshop Setup
linkTitle: Workshop Setup
hidden: true
---

## Workshop Setup Steps

### Available Workshop Orgs

The following Orgs are used for running Observability Workshops. They have all the features enabled to successfully run any of the available workshops.

- CoE Workshop EMEA [EU0]
- Observability Workshop EMEA [EU0]
- Observability Workshop AMER [US1]
- APAC-O11y-Workshop [US1]

### Step 1: Configure Your Org Using SWiPE

SWiPE is an online tool to help configure a workshop environment in Splunk Observability Cloud and is available [here](https://swipe.splunk.show). Please note, SWiPE does not provision EC2 instances - these are provisioned using Splunk Show (see step 2 below). SWiPE will configure the following:

- Create and invite users to the Org. Create a `.csv` file containing the e-mail addresses (one per line) **or** copy and paste e-mail addresses (one per line).
- Create a team and add users.
- Create an Access Token, API Token and a RUM token. You will need to make a copy of these in order to provision the EC2 instances in Splunk Show.

Post-workshop, you can use SWIPE to clean up the Org. SWiPE will complete the following:

- Delete all the users associated with the workshop
- Delete the team
- Delete the tokens
- Delete user dashboards

SWiPE does also provide some advanced features for deleting tokens and detectors, but this must be used with caution.

### Step 2: Provision the EC2 Instances Using Splunk Show

Please visit [Splunk Show](https://show.splunk.com) to provision your EC2 environment. Under the **Workshops** section create a **Splunk4Rookies - Observability** workshop. Select the desired **Content Type** as follows:

- _Default (for interactive workshop)_ select this if your audience is technical and want a hands-on experience installing OpenTelemetry and deploying applications.
- _Pre-configured Instances_ - select this if you need OpenTelemetry and all apps pre-deployed for a less technical audience. Attendees will only require a browser to complete the workshop.

Select your Splunk Observability Cloud Realm and enter the Access Token, API Token and RUM Token that SWiPE generated for you.

For further guidance on using Splunk Show please see the [Splunk Show User Guide](http://go/show/user-guide).

### Workshop Cleanup

Once you have completed your workshop session please remember to go back and clean up the environment using SWiPE. Also ensure your EC2 instances are spun down in order to save costs.

Happy Workshopping!
