---
title: Connect to EC2 Instance
linkTitle: 1. Connect to EC2 Instance
weight: 1
time: 5 minutes
---

## Connect to your EC2 Instance

We’ve prepared an Ubuntu Linux instance in AWS/EC2 for each attendee. To connect to your EC2 instance:

* Copy the `Web SSH` URL from your instance information in Splunk Show.
* Paste the URL in your browser.
* When prompted, input `splunk` as the user name.
* For the password, copy the `SSH Password` value from Splunk Show.

## Retrieve your Instance Name

Once you've logged into your EC2 instance via ssh, use the following command to
get your instance name:

```bash
echo $INSTANCE
```

Make a note of this, as your instance name is unique to you and will be
used later in the workshop to find your data in Splunk Observability Cloud.
