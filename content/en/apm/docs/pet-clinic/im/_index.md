---
title: Install the OpenTelemetry Collector
weight: 2
---

## Install The Open Telemetry Collector

The OpenTelemetry Collector is the core component of instrumenting infrastructure and applications.  Its role is to collect and send:

* Infrastructure metrics (disk, cpu, memory, etc)
* Application Performance Monitoring (APM) traces
* Host and application logs

Splunk Observability Cloud offers wizards to walk you through the setup of the Collector on both your infrastrucutre and applications. To get to the wizard, click in the top left corner icon (the hamburger menu), then click on **Data Setup**

![enter image description here](https://github.com/asomensari-splunk/spring-petclinic/blob/main/src/main/resources/static/resources/images/o11y-landingpage-hamburguer.png?raw=true)

![enter image description here](https://github.com/asomensari-splunk/spring-petclinic/blob/main/src/main/resources/static/resources/images/side-menu-data-setup.png?raw=true)

You'll be taken to a short wizard where you will select some options. The default settings should work, no need to make changes. The wizard will output a few commands that need to be executed in the shell.

Here's an example:

```bash
curl -sSL https://dl.signalfx.com/splunk-otel-collector.sh > /tmp/splunk-otel-collector.sh && \
sudo sh /tmp/splunk-otel-collector.sh --realm us1 -- <API TOKEN REDACTED> --mode agent
```

*(Please do not copy and paste this command verbatim during your exercise as it will not work. You should copy the command from your Splunk Observability Wizard page. The command above has the **API TOKEN REDACTED** and we need the real API TOKEN associated with your account)*

This command will download and setup the OpenTelemetry Collector. Once the install is completed, you can navigate to the Infrastructure page to see the data from your Host

`>> Infrastructure >> My Data Center >> Hosts`

Add Filter >> `host.name` >> (type or select the hostname of your virtual machine)

Once you see data flowing for your host, we are then ready to get started with the APM component
