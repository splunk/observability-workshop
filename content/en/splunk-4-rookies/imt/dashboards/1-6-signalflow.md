---
title: 1.6 SignalFlow
weight: 6
---

## 1. Introduction

Let's take a look at SignalFlow - the analytics language of Observability Cloud that can be used to setup monitoring as code.

The heart of Splunk Infrastructure Monitoring is the SignalFlow analytics engine that runs computations written in a Python-like language. SignalFlow programs accept streaming input and produce output in real time. SignalFlow provides built-in analytical functions that take metric time series (MTS) as input, perform computations, and output a resulting MTS.

- Comparisons with historical norms, e.g. on a week-over-week basis
- Population overviews using a distributed percentile chart
- Detecting if the rate of change (or other metric expressed as a ratio, such as a service level objective) has exceeded a critical threshold
- Finding correlated dimensions, e.g. to determine which service is most correlated with alerts for low disk space

Infrastructure Monitoring creates these computations in the Chart Builder user interface, which lets you specify the input MTS to use and the analytical functions you want to apply to them. You can also run SignalFlow programs directly by using the [SignalFlow API](https://dev.splunk.com/observability/docs/).

SignalFlow includes a large library of built-in analytical functions that take a metric time series as an input, performs computations on its datapoints, and outputs time series that are the result of the computation.

{{% notice title="Info" style="info" %}}
For more information on SignalFlow see [Analyze incoming data using SignalFlow.](https://docs.splunk.com/Observability/infrastructure/analytics/signalflow.html)
{{% /notice %}}

## 2. View SignalFlow

In your dashboard edit the chart called **Active Latency**. Once in the edit mode, click on the **View SignalFlow** link as highlighted below.

![SignalFlow](../../images/view-signalflow.png)

You will see the SignalFlow code that composes the chart we were working on. You can now edit the SignalFlow directly within the UI. Our documentation has the [full list](https://dev.splunk.com/observability/docs/signalflow/function_method_list) of SignalFlow functions and methods.

Also, you can copy the SignalFlow and use it when interacting with the API or with Terraform to being **Monitoring as Code**.

---
{{% expand title="{{% badge style=primary icon=user-ninja %}}**Ninja Mode:** Monitoring as Code{{% /badge %}}" %}}

## 1. Monitoring as Code

Monitoring as code adopts the same approach as infrastructure as code. You can manage monitoring the same way you do applications, servers, or other infrastructure components. You can use monitoring as code to build out your visualisations, what to monitor, and when to alert, among other things. This means your monitoring setup, processes, and rules can be versioned, shared, and reused. Full documentation for the Splunk Terraform Provider is available [here](https://registry.terraform.io/providers/splunk-terraform/signalfx/latest).

Open your terminal that is connected to your AWS/EC2 instance, change into the `o11y-cloud-jumpstart` directory

``` bash
cd observability-content-contrib/integration-examples/terraform-jumpstart
```

Initialize Terraform and upgrade to the latest version of the Splunk Terraform Provider

{{< tabs >}}
{{% tab title="Initialise Terraform" %}}

``` bash
terraform init -upgrade
```

{{% /tab %}}
{{% tab title="Initialise Output" %}}

``` text
Initializing the backend...
Upgrading modules...
- aws in modules/aws
- azure in modules/azure
- docker in modules/docker
- executive-dashboards in modules/dashboards/executive-dashboards
- gcp in modules/gcp
- host in modules/host
- kafka in modules/kafka
- kubernetes in modules/kubernetes
- parent_child_dashboard in modules/dashboards/parent
- pivotal in modules/pivotal
- rum_and_synthetics_dashboard in modules/dashboards/rum_and_synthetics
- usage_dashboard in modules/dashboards/usage

Initializing provider plugins...
- Finding splunk-terraform/signalfx versions matching ">= 6.13.1"...
- Installing splunk-terraform/signalfx v6.24.0...
- Installed splunk-terraform/signalfx v6.24.0 (self-signed, key ID CE97B6074989F138)

Partner and community providers are signed by their developers.
If you'd like to know more about provider signing, you can read about it here:
https://www.terraform.io/docs/cli/plugins/signing.html

Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
```

{{% /tab %}}
{{< /tabs >}}

{{% notice title="Upgrading the SignalFx Terraform Provider" style="tip" %}}
You will need to run the command above each time a new version of the Splunk Terraform Provider is released. You can track the releases on [GitHub.](https://github.com/splunk-terraform/terraform-provider-signalfx/releases)
{{% /notice %}}

### 1.1 Terraform Plan

The `terraform plan` command creates an execution plan. By default, creating a plan consists of:

- Reading the current state of any already-existing remote objects to make sure that the Terraform state is up-to-date.
- Comparing the current configuration to the prior state and noting any differences.
- Proposing a set of change actions that should, if applied, make the remote objects match the configuration.

The plan command alone will not actually carry out the proposed changes, and so you can use this command to check whether the proposed changes match what you expected before you apply the changes

{{< tabs >}}
{{% tab title="Execution Plan" %}}

```bash
terraform plan -var="access_token=$ACCESS_TOKEN" -var="realm=$REALM" -var="o11y_prefix=[$(hostname)]"
```

{{% /tab %}}
{{% tab title="Execution Plan Output" %}}

``` text
Plan: 202 to add, 0 to change, 0 to destroy.
```

{{% /tab %}}
{{< /tabs >}}

If the plan executes successfully, we can go ahead and apply:

---

### 1.2 Terraform Apply

The `terraform apply` command executes the actions proposed in the Terraform plan above.

The most straightforward way to use `terraform apply` is to run it without any arguments at all, in which case it will automatically create a new execution plan (as if you had run terraform plan) and then prompt you to provide the Access Token, Realm and prefix (the prefix defaults to `Splunk`) and approve the plan, before taking the indicated actions.

Due to this being a workshop it is required that the prefix is to be unique to you so you need to run the `terraform apply` below.

{{< tabs >}}
{{% tab title="Apply Plan" %}}

``` bash
terraform apply -var="access_token=$ACCESS_TOKEN" -var="realm=$REALM" -var="o11y_prefix=[$(hostname)]"
```

{{% /tab %}}
{{% tab title="Apply Plan Output" %}}

When prompted, "Do you want to perform these actions?", type `yes` and press `Enter`.

``` text
Apply complete! Resources: 202 added, 0 changed, 0 destroyed.
```

{{% /tab %}}
{{< /tabs >}}

Once the apply has completed, validate that the dashboards and detectors have been created. From the left hand menu, click on **Dashboards** and navigate down to **Custom Dashboard Groups**. Your custom dashboards will be prefixed with the hostname of your instance. Again, from the left hand manu click on **Alerts & Detectors** and then click on the **Detectors** tab. You can search for your detectors using the prefixed hostname of your instance.

To check the prefix value run:

``` bash
echo $(hostname)
```

{{% /expand %}}

---

![Code](../../images/show-signalflow.png)

{{< tabs >}}
{{% tab title="SignalFlow" %}}

```python
A = data('demo.trans.latency', filter=filter('demo_datacenter', 'Paris')).percentile(pct=95).publish(label='A', enable=False)
B = data('demo.trans.latency', filter=filter('demo_datacenter', 'Paris')).percentile(pct=95).timeshift('1w').publish(label='B', enable=False)
C = (A-B).publish(label='C')
```

{{% /tab %}}
{{< /tabs >}}

Click on **View Builder** to go back to the Chart **Builder** UI.

![View Builder](../../images/view-builder.png)

Let's save this new chart to our Dashboard!
