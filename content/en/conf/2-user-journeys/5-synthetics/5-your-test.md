---
title: 5. Test your own site!
weight: 5
---

{{% exercise title="Start testing in your own Playground" %}}
Go to the [Splunk website](https://www.splunk.com/en_us/download/observability-cloud-free-edition.html) and register to get the Splunk Observability Cloud Free Edition. 

Follow the link from your email, and sign in at least once a month to keep the Free Edition as long as you need it!

1. Go to Digital Experience > Synthetics, click `Create` and add a new **Uptime test**. 
1. Point it to a public URL owned by your organization, set a frequency, and set the public locations to test it from. 
1. Click `Try Now` to validate that the test configuration works as expected.
1. (Optional) Create a detector for uptime <95% or downtime >1%, split by location so you get location-level insights. Add your own email address first to evaluate alert noise before connecting to a team or webhook.
1. Save the test to start getting eyes on that endpoint health!
1. (Optional) Repeat the process, this time with a **Browser test** running every five or 15 minutes. What do you learn from the results?

{{% notice title="Keep in mind" style="primary"  icon="lightbulb" %}}Your organization might bot-block the Synthetic testing agent - this is a good thing for security! Allowlist our [public testing locations](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/synthetic-monitoring/advanced-test-configurations/public-locations) based on your realm, or consider running tests from a [private location](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/synthetic-monitoring/advanced-test-configurations/private-locations) wherever you have a dedicated host. Private locations can also be used to test endpoints behind a firewall.{{% /notice %}}

{{% /exercise %}}
