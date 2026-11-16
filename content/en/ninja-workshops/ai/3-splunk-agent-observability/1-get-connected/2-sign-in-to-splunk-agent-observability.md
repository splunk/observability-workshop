---
title: Sign In to Splunk Agent Observability
linkTitle: 2. Sign In to Splunk Agent Observability
weight: 2
time: 5 minutes
---

## Sign In to Splunk Agent Observability 

To access Splunk Agent Observability, navigate to 
[https://console.multitenant.sao.splunkcloud.com`](https://console.multitenant.sao.splunkcloud.com) using your browser. 

The credentials are stored as environment variables on your EC2 instance: 

```bash
echo $SPLUNK_AO_USER
echo $SPLUNK_AO_PASSWORD
```

Use these credentials to sign in to Splunk Agent Observability. 

After signing in, ensure that the `workshop` org is selected.  Then, you should see a screen 
similar to the following example: 

![Splunk Agent Observability Initial Screen](../../images/SplunkAgentObservability.png)

