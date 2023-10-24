---
title: Creating a Detector
linkTitle: Detectors
weight: 3
draft: true
---

## Aim

We need to create a new Detector within SignalFx which will use VictorOps as the target to send alerts to.

We will use Terraform installed within the VM to create the Detector, but first we need to obtain some values required for Terraform to run.

---

## 1. Preparation

The presenter will typically share these values with you at the start of the module to save time, but the following instructions explain how to get them for yourself.

### 1.1 Create a variables document

We suggest you create a variables document using your preferred text editor as you will be gathering three different values in the next few steps which you need to use in the last step of this module.

Add the following lines to your variables document, then as you gather the values you can add them to the appropriate lines:

=== "variables.txt"

    ``` text
    export ACCESS_TOKEN=
    export REALM=
    export SFXVOPSID=
    ```

### 1.2 Obtain SignalFx Access Token

In the Splunk UI you can find your **Access Token** by clicking on the **Settings** icon on the top right of the Splunk UI, select **Organization Settings → Access Tokens**, expand the **Default** token, then click on **Show Token** to expose your token.

![Access Token](../../../images/m7-access-token.png)

Click the **Copy**{: .label-button .sfx-ui-button-blue} button to copy it you your clipboard, then paste it into the `ACCESS_TOKEN` line of your variables document.

=== "variables.txt"

    ```text
    export ACCESS_TOKEN={==xxxx==}
    export REALM=
    export SFXVOPSID=
    ```

### 1.3 Obtain SignalFx Realm

Still in the Splunk UI, click on the **Settings** icon again, but this time select **My Profile**.

The Realm can be found in the middle of the page within the Organizations section. In this example it is **us1**, but yours may be **eu0** or one of the many other SignalFx Realms.

![Realm](../../../images/m7-realm.png)

Copy it to the `REALM` line of your variables document.

=== "variables.txt"

    ```text
    export ACCESS_TOKEN={==xxxx==}
    export REALM={==xxxx==}
    export SFXVOPSID=
    ```

### 1.4. Obtain VictorOps Integration ID

In Splunk UI navigate to **Integrations** and use the search feature to find the VictorOps Integration.

Expand the **VictorOps-xxxx** configuration; if there are more than one you will be informed which one to copy by the presenter.

![VictorOps Integration](../../../images/m7-sfx-vo-integration-id.png)

Copy it to the `SFXVOPSID` line of your variables document.

=== "variables.txt"

    ```text
    export ACCESS_TOKEN={==xxxx==}
    export REALM={==xxxx==}
    export SFXVOPSID={==xxxx==}
    ```

---

## 2. Create environment variables

### 2.1 Copy variables to VM

With all the required values now safely copied into your variables document you can use them to compile the commands which we will run in your VM in the next step.

=== "Example"

    ```text
    export SFXVOPSID=EYierbGA4AA
    export ACCESS_TOKEN=by78voyt7b.....
    export REALM=us1
    ```

Switch back to your shell session connected to the VM you created in the **Getting Started/Create a Test Environment** module, all of the following commands will be executed within this instance:

Past the three commands from your variables document into the shell session of your VM.

## 3. Initialize and apply Terraform

Still within your VM, switch to the victorops folder where the Terraform config files are located (you should still be logged in as Ubuntu and should not have elevated to root)

=== "Change Directory"

    ```text
    cd ~/workshop/victorops
    ```

Now we can initialize Terraform:

=== "Shell Command"

    ```text
    terraform init -upgrade
    ```

=== "Example Output"

    ```text
    Initializing the backend...

    Initializing provider plugins...
    - Checking for available provider plugins...
    - Downloading plugin for provider "signalfx" (terraform-providers/signalfx) 4.21.0...

    The following providers do not have any version constraints in configuration,
    so the latest version was installed.

    To prevent automatic upgrades to new major versions that may contain breaking
    changes, it is recommended to add version = "..." constraints to the
    corresponding provider blocks in configuration, with the constraint strings
    suggested below.

    * provider.signalfx: version = "~> 4.21"

    Terraform has been successfully initialized!

    You may now begin working with Terraform. Try running "terraform plan" to see
    any changes that are required for your infrastructure. All Terraform commands
    should now work.

    If you ever set or change modules or backend configuration for Terraform,
    rerun this command to reinitialize your working directory. If you forget, other
    commands will detect it and remind you to do so if necessary.
    ```

You can now copy and the paste the following code block to run Terraform using the Variables you created in the VM.  Check the plan output for errors before typing _**yes**_ to commit the apply.

=== "Shell Command"

    ```text
    terraform apply \
    -var="access_token=$ACCESS_TOKEN" \
    -var="realm=$REALM" \
    -var="sfx_prefix=${HOSTNAME}" \
    -var="sfx_vo_id=$SFXVOPSID" \
    -var="routing_key=${HOSTNAME}_PRI"
    ```

=== "Example Output"

    ```
    An execution plan has been generated and is shown below.
    Resource actions are indicated with the following symbols:
      + create

    Terraform will perform the following actions:

      # signalfx_detector.cpu_greater_90 will be created
      + resource "signalfx_detector" "cpu_greater_90" {
          + description       = "Alerts when CPU usage is greater than 90%"
          + id                = (known after apply)
          + max_delay         = 0
          + name              = "vmpe CPU greater than 90%"
          + program_text      = <<~EOT
                from signalfx.detectors.against_recent import against_recent
                A = data('cpu.utilization', filter=filter('host', 'vmpe*')).publish(label='A')
                detect(when(A > threshold(90))).publish('CPU utilization is greater than 90%')
            EOT
          + show_data_markers = true
          + time_range        = 3600
          + url               = (known after apply)

          + rule {
              + detect_label          = "CPU utilization is greater than 90%"
              + disabled              = false
              + notifications         = [
                  + "VictorOps,xxx,vmpe_pri",
                ]
              + parameterized_body    = <<~EOT
                    {{#if anomalous}}
                        Rule "{{{ruleName}}}" in detector "{{{detectorName}}}" triggered at {{timestamp}}.
                    {{else}}
                        Rule "{{{ruleName}}}" in detector "{{{detectorName}}}" cleared at {{timestamp}}.
                    {{/if}}
                    
                    {{#if anomalous}}
                      Triggering condition: {{{readableRule}}}
                    {{/if}}
                    
                    {{#if anomalous}}
                      Signal value: {{inputs.A.value}}
                    {{else}}
                      Current signal value: {{inputs.A.value}}
                    {{/if}}
                    
                    {{#notEmpty dimensions}}
                      Signal details: {{{dimensions}}}
                    {{/notEmpty}}
                    
                    {{#if anomalous}}
                      {{#if runbookUrl}}
                        Runbook: {{{runbookUrl}}}
                      {{/if}}
                      {{#if tip}}
                        Tip: {{{tip}}}
                      {{/if}}
                    {{/if}}
                EOT
              + parameterized_subject = "{{ruleSeverity}} Alert: {{{ruleName}}} ({{{detectorName}}})"
              + severity              = "Critical"
            }
        }

    Plan: 1 to add, 0 to change, 0 to destroy.
    
    Do you want to perform these actions in workspace "Workshop"?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.
    
      Enter a value: yes
    
    signalfx_detector.cpu_greater_90: Creating...
    signalfx_detector.cpu_greater_90: Creation complete after 2s [id=EWHU-YAAAAA]
    
    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
    ```

---

## 4. Summary

By running Terraform within the VM you have just created a new Detector within SignalFx which will send alerts to VictorOps if the CPU utilization of your specific VM goes above 90%.

In the Splunk UI go to **Alerts → Detectors** to show all the Detectors and find the one matching your `INSTANCE` value (the first four letters of the name of your VM).

Optionally - Click on **CPU Utilization is greater than 90%** to open the Alert Rule Editor to view its settings.

![Detector](../../../images/detector.png)

A filter has been used to specifically monitor your VM using the 1st 4 characters of its name, which were randomly assigned when you created the VM.

![Detector Filter](../../../images/detector-filter.png)

A **Recipient** has been configured using the VictorOps Integration and your **Routing Key** has been specified.  This is how a monitoring system such as SignalFx knows to route Alerts into VictorOps, and ensure they get routed to the correct team.

![Detector Recipients](../../../images/detector-recipients.png)

---

You have now configured the Integrations between VictorOps and SignalFx!

The final part of this module is to test the flow of alerts from SignalFx into VictorOps and see how you can manage the incident with both the VictorOps UI and Mobile App.
