---
title: Preparation of the Pet Clinic application. 
linkTitle: 2. Preparation
weight: 3
---

## 1. Validate the settings for your workshop

The instructor will provide you with the login information for the instance that we will be using during the workshop.
When you first log into your instance, you will be greeted by the Splunk Logo as shown below:

```text
❯ ssh -p 2222 splunk@[IP-ADDRESS]

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

If this isn't shown, or you see an error, log out and give it a minute or so, then try to log in again as the instance might not have finished the initial boot sequence. If it still does not show the above Welcome page, reach out to your Instructor.

Next, let's ensure your instance is configured correctly, we need to confirm that the required environment variables for this workshop are set correctly. In your terminal run the following command and in the output check the environment variables are present and have actual valid values set:

{{< tabs >}}
{{% tab title="Command" %}}

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
INSTANCE = <your workshop name>
```

{{% /tab %}}
{{< /tabs >}}

Please make a note of the `INSTANCE` environment variable value as this is the reference to your workshop instance and we will need it later to filter data in the **Splunk Observability Cloud** UI.

For this workshop, **all** of the above are required. If any have values missing, please contact your instructor.

{{% notice title="Delete any existing OpenTelemetry Collectors" style="warning" %}}
If you have completed a Splunk Observability workshop using this EC2 instance, please ensure you have deleted the collector running in Kubernetes before continuing with this workshop. This can be done by running the following command:

``` bash
helm delete splunk-otel-collector
```

{{% /notice %}}
