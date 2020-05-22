# Create a SignalFx Detector

We now need to create a new Detector within SignalFx which will use VictorOps as the target to send alerts to.

Shell into your 1st Multipass instance you created in the **Getting Started** module:

=== "Input"

    ```
    multipass shell ${INSTANCE}
    ```

The three required variables should be stored in your `values.txt` if you have been populating it as you have worked through this module.

=== "Variables"

    ```bash
    export SFXVOPSID=[VictorOps Integration ID from Step 2]
    export ACCESS_TOKEN=[SignalFx Access Token from Step 2]
    export REALM=[SignalFx Realm from Step 2]
    ```

=== "Example"

    ```bash
    export SFXVOPSID=xxxxxxxxxxxx
    export ACCESS_TOKEN=xxxxxxxxxxxxxxx
    export REALM=us1
    ```

Next you need to export an environment vairable for your Routing Key, as this uses the hostname of the VM, run the following command:

=== "Input"

    ```bash
    export ROUTINGKEY=${HOSTNAME:0:4}_PRI
    ```

# Initialize Terraform

=== "Input"

    ```bash
    terraform init -upgrade
    ```

=== "Output"

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

Create a new Terraform workspace[^1] which will track the state for this environment.

=== "Input"

    ```text
    terraform workspace new VictorOps
    ```

=== "Output"

    ```text
    Created and switched to workspace "VictorOps"!

    You're now on a new, empty workspace. Workspaces isolate their state,
    so if you run "terraform plan" Terraform will not see any existing state
    for this configuration.
    ```

It is considered best practice to run a `terraform plan` to see what changes may get made and check for potential errors before running an apply as we did in [Monitoring as Code](../../mac/terraform/).

However, as the first stage of apply is to plan we can safely skip that step and just run apply.

Check the plan output for errors before typing _**yes**_ to commit the apply.

=== "Input"

    ```text
    terraform apply \
    -var="access_token=$ACCESS_TOKEN" \
    -var="realm=$REALM" \
    -var="sfx_prefix=${HOSTNAME:0:4}" \
    -var="sfx_vo_id=$SFXVOPSID" \
    -var="routing_key=$ROUTINGKEY"
    ```

=== "Output"

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
          + name              = "ixmy CPU greater than 90%"
          + program_text      = <<~EOT
                from signalfx.detectors.against_recent import against_recent
                A = data('cpu.utilization', filter=filter('host', 'ixmy*')).publish(label='A')
                detect(when(A > threshold(90))).publish('CPU utilization is greater than 90%')
            EOT
          + show_data_markers = true
          + time_range        = 3600
          + url               = (known after apply)

          + rule {
              + detect_label          = "CPU utilization is greater than 90%"
              + disabled              = false
              + notifications         = [
                  + "VictorOps,xxx,ixmy_pri",
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

You have now configured the Integrations between VictorOps and SignalFx!

The final part of this module is to test the flow of alerts from SignalFx into VictorOps and see how you can manage the incident with both the VictorOps UI and Mobile App.

[^1]:Workspaces allow you to run Terraform against different environments each with their own state data stored in the workspace.
