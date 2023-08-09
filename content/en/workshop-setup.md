---
title: Workshop Setup
linkTitle: Workshop Setup
hidden: true
---

## Workshop Setup Steps

### Available Workshop Orgs

- CoE Workshop EMEA [EU0]
- Observability Workshop EMEA [EU0]
- Observability Workshop AMER [US1]
- APAC-O11y-Workshop [US1]

The following Orgs are used for running Observability Workshops. They have all the features enabled to successfully run any of the available workshops.

### Step 1: Configure Your Org Using SWIPE

SWIPE is an online tool to help configure the workshop environment in Observability Cloud and is available [here](https://swipe.splunk.show). Please note, SWIPE does not provision EC2 instances - these are provisioned using Splunk Show (see step 2 below). SWIPE will configure the following:

- Create and invite users to the Org. Create a `csv` file with one e-mail address per line.
- Create a team and add users.
- Create an Access Token and a RUM token. You will need to make a copy of these in order to provision the EC2 instances.

Post-workshop, you can use SWIPE to clean up the Org. SWIPE will complete the following:

- Delete all the users in the Org that are in the `csv` file
- Delete the team
- Delete the tokens
- Delete user dashboards

SWIPE does also provide some advanced features for deleting tokens and detectors, but this must be used with caution.

### Step 2: Provision the EC2 Instances Using Splunk Show

Please visit [Splunk Show](https://show.splunk.com) to provision your EC2 environment. Under the **Workshops** section create a **Splunk4Rookies - Observability** workshop. Select the desired **Content Type** as follows:

- _Default (for interactive workshop)_ select this if your audience is technical and want a hands-on experience installing OpenTelemetry and deploying applications.
- _Pre-configured Instances_ - select this if you need OpenTelemetry and all apps pre-deployed for a less technical audience. Attendees will only require a browser to complete the workshop.

Select your O11y Cloud realm and enter your user access and RUM tokens from your O11y Cloud org.

For further guidance on using Splunk Show please see the [Splunk Show User Guide](http://go/show/user-guide).

### Workshop Cleanup

Once you have completed your workshop session please remember to go back and clear up the environment using SWIPE. Also ensure your EC2 instances are spun down in order to save costs.

Happy Workshopping!

