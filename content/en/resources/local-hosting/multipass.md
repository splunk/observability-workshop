---
title: Local Hosting with Multipass
weight: 1
description: Learn how to create a local hosting environment with Multipass - Windows/Linux/Mac(Intel)
---

Install [Multipass](https://multipass.run/) and Terraform for your operating system. On a Mac (Intel), you can also install via [Homebrew](https://brew.sh/) e.g.

```text
brew install multipass
brew install terraform
```

Clone workshop repository:

```bash
git clone https://github.com/splunk/observability-workshop
```

Change into multipass directory:

```bash
cd observability-workshop/local-hosting/multipass
```

Log Observer Connect:

If you plan to use your own Splunk Observability Cloud Suite Org and or Splunk instance, you may need to create a new **Log Observer Connect** connection:
Follow the instructions found in the [documentation](https://docs.splunk.com/observability/en/logs/lo-connect-landing.html) for [Splunk Cloud](https://docs.splunk.com/observability/en/logs/scp.html#logs-scp) or [Splunk Enterprize](https://docs.splunk.com/observability/en/logs/set-up-logconnect.html).

Additional requirements for running your own **Log Observer Connect** connection are:

- Create an index called **splunk4rookies-workshop**
- Make sure the Service account user used in the **Log observer Connect** connection has access to the **splunk4rookies-workshop** index (you can remove all other indexes, as all workshop log data should go to this index).

Initialise Terraform:

{{< tabs >}}
{{% tab title="Command" %}}

```bash
terraform init -upgrade
```

{{< /tab >}}
{{< tab title="Example Output" >}}

```text
Initializing the backend...

Initializing provider plugins...
- Finding latest version of hashicorp/random...
- Finding latest version of hashicorp/local...
- Finding larstobi/multipass versions matching "~> 1.4.1"...
- Installing hashicorp/random v3.5.1...
- Installed hashicorp/random v3.5.1 (signed by HashiCorp)
- Installing hashicorp/local v2.4.0...
- Installed hashicorp/local v2.4.0 (signed by HashiCorp)
- Installing larstobi/multipass v1.4.2...
- Installed larstobi/multipass v1.4.2 (self-signed, key ID 797707331BF3549C)
```

{{< /tab >}}
{{< /tabs >}}

Create Terraform variables file. Variables are kept in file `terrform.tfvars` and we provide a template, `terraform.tfvars.template`, to copy and edit:

```bash
cp terraform.tfvars.template terraform.tfvars
```

The following Terraform variables are required:

- `splunk_access_token`: Observability Cloud Access Token
- `splunk_api_token`: Observability Cloud API Token
- `splunk_rum_token`: Observability Cloud RUM Token
- `splunk_realm`: Observability Cloud Realm e.g. `eu0`
- `splunk_hec_url`: Splunk HEC URL. Do not use a `raw` endpoint, use the `event` endpoint so logs process correctly.
- `splunk_hec_token`: Splunk HEC Token
- `splunk_index`: Splunk Index to send logs to. Defaults to `splunk4rookies-workshop`.

Instance type variables:

- `splunk_presetup`: Provide a preconfigured instance (OTel Collector and Online Boutique deployed with RUM enabled). The default is `false`.
- `splunk_diab`: Install and run Demo-in-a-Box. The default is `false`.
- `tagging_workshop`: Install and configure the Tagging Workshop. The default is `false`.
- `otel_demo` : Install and configure the OpenTelemetry Astronomy Shop Demo. This requires that `splunk_presetup` is set to `false`. The default is `false`.

Optional advanced variables:

- `wsversion`: Set this to `main` if working on the development of the workshop, otherwise this can be omitted.
- `architecture`: Set this to `arm64` if you are running on Apple Silicon. Defaults to `amd64`.

Run `terraform plan` to check that all configuration is OK. Once happy run `terraform apply` to create the instance.

{{< tabs >}}
{{% tab title="Command" %}}

```bash
terraform apply
```

{{< /tab >}}
{{% tab title="Example Output" %}}


``` text
random_string.hostname: Creating...
random_string.hostname: Creation complete after 0s [id=cynu]
local_file.user_data: Creating...
local_file.user_data: Creation complete after 0s [id=46a5c50e396a1a7820c3999c131a09214db903dd]
multipass_instance.ubuntu: Creating...
multipass_instance.ubuntu: Still creating... [10s elapsed]
multipass_instance.ubuntu: Still creating... [20s elapsed]
...
multipass_instance.ubuntu: Still creating... [1m30s elapsed]
multipass_instance.ubuntu: Creation complete after 1m38s [name=cynu]
data.multipass_instance.ubuntu: Reading...
data.multipass_instance.ubuntu: Read complete after 1s [name=cynu]

Apply complete! Resources: 3 added, 0 changed, 0 destroyed.

Outputs:

instance_details = [
  {
    "image" = "Ubuntu 22.04.2 LTS"
    "image_hash" = "345fbbb6ec82 (Ubuntu 22.04 LTS)"
    "ipv4" = "192.168.205.185"
    "name" = "cynu"
    "state" = "Running"
  },
]
```

{{% /tab %}}
{{< /tabs >}}

Once the instance has been successfully created (this can take several minutes), shell into it using the `name` from the output above e.g.

{{< tabs >}}
{{% tab title="Command" %}}

```bash
multipass shell cynu
```

{{< /tab >}}
{{% tab title="Example Output" %}}

```text
███████╗██████╗ ██╗     ██╗   ██╗███╗   ██╗██╗  ██╗    ██╗
██╔════╝██╔══██╗██║     ██║   ██║████╗  ██║██║ ██╔╝    ╚██╗
███████╗██████╔╝██║     ██║   ██║██╔██╗ ██║█████╔╝      ╚██╗
╚════██║██╔═══╝ ██║     ██║   ██║██║╚██╗██║██╔═██╗      ██╔╝
███████║██║     ███████╗╚██████╔╝██║ ╚████║██║  ██╗    ██╔╝
╚══════╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝    ╚═╝

To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details

Waiting for cloud-init status...
Your instance is ready!

ubuntu@cynu ~ $
```

{{% /tab %}}
{{< /tabs >}}

Change user to `splunk` (the password is `Splunk123!`):

```bash
su -l splunk
```

Validate the instance:

```bash
kubectl version --output=yaml
```

To delete the instance, run the following command:

```bash
terraform destroy
```
