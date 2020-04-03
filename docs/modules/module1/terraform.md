## Lab Summary
* Install Terraform and initialise the SignalFx Provider.
* Run Terraform to create SignalFx detectors and dashboards from code using our Terraform provider.
* See how Terraform can also delete detectors and dashboards.
* (Optional) Upgrade the SignalFx Provider.
***
### 1. Initial setup
Download and install Terraform for your platform - https://www.terraform.io/downloads.html (min. requirement v. 0.12.18)

Download the SignalFx Jumpstart Terraform master zip file, unzip the file and change into the `signalfx-jumpstart-master` directory

``` bash
curl -LO https://github.com/signalfx/signalfx-jumpstart/archive/master.zip
unzip master.zip
cd signalfx-jumpstart-master
```

Initialise Terraform. **Note:** You will need to run this command each time a new version of the Terraform Provider is released. You can track the releases on [GitHub](https://github.com/terraform-providers/terraform-provider-signalfx/releases).

```bash
terraform init -upgrade
```

Create a new workspace, replace `{WORKSPACE_NAME}` with what you want your workspace to be called:

``` bash
terraform workspace new {WORKSPACE_NAME}
```

---

### 2. Plan and apply the Terraform
Review the execution plan. Replace `{YOUR_INITIALS}` e.g. `-var=”sfx_prefix=RWC”`

``` bash
terraform plan -var="access_token=abc123" -var="realm=us1" -var="sfx_prefix={YOUR_INITIALS}"
```

Where `access_token` is the SignalFx Access Token and realm is either `eu0`, `us1` or `ap0`. If the plan executes successfully, we can go ahead and apply:

``` bash
terraform apply -var="access_token=abc123" -var="realm=us1" -var="sfx_prefix={YOUR_INITIALS}"
```

To deploy only a subset (by module see `main.tf`) e.g.
``` bash
terraform apply -var="access_token=abc123" -var="realm=us1" -var="sfx_prefix={YOUR_INITIALS}" -target=module.aws
terraform apply -var="access_token=abc123" -var="realm=us1" -var="sfx_prefix={YOUR_INITIALS}" - target=module.usage_dashboard
terraform apply -var="access_token=abc123" -var="realm=us1" -var="sfx_prefix={YOUR_INITIALS}" -target=module.gcp
```

Validate that the detectors were created, under the _**Alerts tab → Detectors**_, you should see a list of new detectors with the a prefix of your initials:

![](../images/m1_l3-detectors.png)

---
### 3. Destroy all your hard work
You will first need to ensure you are in the correct workspace, replace `{WORKSPACE_NAME}` with the name created in the initial setup)

```bash
terraform workspace select {WORKSPACE_NAME}
```

Destroy all Detectors and Dashboards that were previously applied. **Note:** The `var=”sfx_prefix={YOUR_INITIALS}”` is not required!

```bash
terraform destroy -var="access_token=abc123" -var="realm=us1"
```