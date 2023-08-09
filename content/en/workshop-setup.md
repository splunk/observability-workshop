---
title: Workshop Setup
linkTitle: Workshop Setup
hidden: true
---

## Workshop Setup

### Workshop Orgs

- CoE Workshop EMEA [EU0]
- Observability Workshop EMEA [EU0]
- Observability Workshop AMER [US1]
- APAC-O11y-Workshop [US1]

The following Orgs are used for running Observability Workshops. They have all the features enabled to successfully run any of the available workshops.

### SWIPE

SWIPE is an online tool to help configure the workshop environment in Observability Cloud and is available [here](https://swipe.splunk.com). Please note, the SWIPE does not provision EC2 instances. SWIPE will configure the following:

- Create and invite users to the Org. Create a `csv` file with one e-mail address per line.
- Create a team and add users.
- Create an Access Token and a RUM token. You will need to make a copy of these in order to provision the EC2 instances.

Post workshop, you can use SWIPE to clean up the Org. SWIPE will complete the following:

- Delete all the users in the Org that are in the `csv` file
- Delete the team
- Delete the tokens
- Delete user dashboards

SWIPE does also provide some advanced features for deleting tokens and detectors, but this must be used with caution.

### Provisioning EC2 Instances

TBC

Once you have completed your workshop session please remember to go back and clear up the environment. Also ensure your EC2 instances are spun down in order to save cost.

Happy Workshopping!

