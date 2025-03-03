---
title: Preparation of the Workshop instance
linkTitle: 2. Preparation
weight: 3
archetype: chapter
time: 15 minutes
---

The instructor will provide you with the login information for the instance that we will be using during the workshop.

When you first log into your instance, you will be greeted by the Splunk Logo as shown below. If you have any issues connecting to your workshop instance then please reach out to your Instructor.

``` text
$ ssh -p 2222 splunk@<ip-address>

███████╗██████╗ ██╗     ██╗   ██╗███╗   ██╗██╗  ██╗    ██╗  
██╔════╝██╔══██╗██║     ██║   ██║████╗  ██║██║ ██╔╝    ╚██╗ 
███████╗██████╔╝██║     ██║   ██║██╔██╗ ██║█████╔╝      ╚██╗
╚════██║██╔═══╝ ██║     ██║   ██║██║╚██╗██║██╔═██╗      ██╔╝
███████║██║     ███████╗╚██████╔╝██║ ╚████║██║  ██╗    ██╔╝ 
╚══════╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝    ╚═╝  
Last login: Mon Feb  5 11:04:54 2024 from [Redacted]
Waiting for cloud-init status...
Your instance is ready!
splunk@show-no-config-i-0d1b29d967cb2e6ff:~$ 
```

To ensure your instance is configured correctly, we need to confirm that the required environment variables for this workshop are set correctly. In your terminal run the following script and check that the environment variables are present and set with actual valid values:

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
. ~/workshop/petclinic/scripts/check_env.sh
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
ACCESS_TOKEN = <redacted>
REALM = <e.g. eu0, us1, us2, jp0, au0 etc.>
RUM_TOKEN = <redacted>
HEC_TOKEN = <redacted>
HEC_URL = https://<...>/services/collector/event
INSTANCE = <instance_name>
```

{{% /tab %}}
{{< /tabs >}}

Please make a note of the `INSTANCE` environment variable value as this will be used later to filter data in **Splunk Observability Cloud**.

For this workshop, **all** the above are required. If any have values missing, please contact your Instructor.

> [!SPLUNK] Delete any existing OpenTelemetry Collectors
>If you have previously completed a Splunk Observability workshop using this EC2 instance, you
>need to ensure that any existing installation of the Splunk OpenTelemetry Collector is
>deleted. This can be achieved by running the following command:
>
>``` bash
>helm delete splunk-otel-collector
>```
