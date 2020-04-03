## Summary of this lab
* Install Terraform and initialise the SignalFx Provider.
* Run Terraform to create SignalFx detectors and dashboards from code using our Terraform provider.
* See how Terraform can also delete detectors and dashboards.
* (Optional) Upgrade the SignalFx Provider.
***
## Step 1: Initial setup
1. Download and install Terraform for your platform - https://www.terraform.io/downloads.html (min. requirement v. 0.12.18)

2. Download the SignalFx Jumpstart Terraform master zip file, unzip the file and change into the `signalfx-jumpstart-master` directory
   ```bash
   curl -LO https://github.com/signalfx/signalfx-jumpstart/archive/master.zip
   unzip master.zip
   cd signalfx-jumpstart-master
   ```

3. Initialise Terraform. **Note:** You will need to run this command each time a new version of the Terraform Provider is released. You can track the releases on [GitHub](https://github.com/terraform-providers/terraform-provider-signalfx/releases).
   ```bash
   terraform init -upgrade
   ```

4. Create a new workspace (replace `WORKSPACE_NAME` with what you want your workspace to be called)
   ```bash
   terraform workspace new WORKSPACE_NAME
   ```
---
## Step 2: Plan and apply the Terraform
1. Review the execution plan. Replace `[YOUR-INITIALS]` e.g. `-var=”sfx_prefix=RWC”`
   ```bash
   terraform plan -var="access_token=abc123" -var="realm=us1" -var="sfx_prefix=[YOUR-INITIALS]"
   ```

   Where `access_token` is the SignalFx Access Token and realm is either `eu0`, `us1` or `ap0`

3. If the plan executes successfully, we can go ahead and apply
   ```bash
   terraform apply -var="access_token=abc123" -var="realm=us1" -var="sfx_prefix=[YOUR-INITIALS]"
   ```

4. To deploy only a subset (by module see `main.tf`) e.g.
   ```bash
   terraform apply -var="access_token=abc123" -var="realm=us1" -var="sfx_prefix=[YOUR-INITIALS]" -target=module.aws
   terraform apply -var="access_token=abc123" -var="realm=us1" -var="sfx_prefix=[YOUR-INITIALS]" - target=module.usage_dashboard
   terraform apply -var="access_token=abc123" -var="realm=us1" -var="sfx_prefix=[YOUR-INITIALS]" -target=module.gcp
   ```

5. Validate that the detectors were created, under the _**Alerts tab → Detectors**_, you should see a list of new detectors with the a prefix of your initials:

   ![](../images/m1_l3-detectors.png)

---
## Step 3: Destroy all your hard work
1. You will first need to ensure you are in the correct workspace (replace `WORKSPACE_NAME` with the name created in _**Step #1.4**_)
   ```
   terraform workspace select WORKSPACE_NAME
   ```

2. Destroy all Detectors and Dashboards that were previously applied. NOTE: The `var=”sfx_prefix=[YOUR-INITIALS]”` is not required!
   ```bash
   terraform destroy -var="access_token=abc123" -var="realm=us1"
   ```
