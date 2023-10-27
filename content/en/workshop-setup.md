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
- Create an INGEST, API and RUM tokens. You will need to make a copy of these in order to provision the EC2 instances in Splunk Show.

Post-workshop, you can use SWIPE to clean up the Org. SWiPE will complete the following:

- Delete all the users associated with the workshop
- Delete the team
- Delete the tokens
- Delete user dashboards

SWiPE does also provide some advanced features for deleting tokens and detectors, but this must be used with caution.

### Step 2: Provision the EC2 Instances Using Splunk Show

Please visit [Splunk Show](https://show.splunk.com/template/262/?type=workshop) to provision your EC2 environment(s). Select the desired **Content Type** as follows:

- _Default (for interactive workshop)_ select this if your audience is technical and want a hands-on experience installing OpenTelemetry and deploying applications.
  - Select either Normal Workshop, Private Event or Public Event. Change **Estimated Participants** to the number of attendees you expect and set the same value in **O11y Shop Quantity**. This will provision the correct number of EC2 instances. It is recommended that you over-provision by 10% - 20% to allow for any last minute attendees.
- _Pre-configured Instances_ - select this if you need the OpenTelemetry Collector and the application pre-deployed for a less technical audience. Attendees will only require a browser to complete the workshop.
  - Select Normal Workshop only! Ensure that **Estimated Participants** is set to **1** and **O11y Shop Quantity** is set to **1** also as only a single instance is required by the workshop instructor.

Select your Splunk Observability Cloud Realm and enter the INGEST, API and RUM tokens that SWiPE generated for you.

For further guidance on using Splunk Show please see the [Splunk Show User Guide](http://go/show/user-guide).

### Workshop Clean-up

Once you have completed your workshop session please remember to go back and clean up the environment using SWiPE. Also ensure your EC2 instances are spun down in order to save costs.

Happy Workshopping!
