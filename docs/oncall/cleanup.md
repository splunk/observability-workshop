# Post Workshop Clean Up

Once you have finished with this workshop can you please perform the following steps to clean up the environment.

---

## Delete Detector

Copy and the paste the following code block into the command shell for your VM. This will use Terraform to destroy your detector. Check the plan output for errors before typing yes to commit the destroy.

=== "Shell Command"

    ```text
    terraform destroy \
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
    - destroy

    Terraform will perform the following actions:

    # signalfx_detector.cpu_greater_90 will be destroyed
    - resource "signalfx_detector" "cpu_greater_90" {
        - description       = "Alerts when CPU usage is greater than 90%" -> null
        - disable_sampling  = false -> null
        - end_time          = 0 -> null
        - id                = "EcUFGGJAAAE" -> null
        - max_delay         = 0 -> null
        - name              = "zevn CPU greater than 90%" -> null
        - program_text      = <<~EOT
                from signalfx.detectors.against_recent import against_recent
                A = data('cpu.utilization', filter=filter('host', 'zevn*')).publish(label='A')
                detect(when(A > threshold(90))).publish('CPU utilization is greater than 90%')
            EOT -> null
        - show_data_markers = true -> null
        - show_event_lines  = false -> null
        - start_time        = 0 -> null
        - teams             = [] -> null
        - time_range        = 3600 -> null
        - url               = "https://app.signalfx.com/#/detector/EcUFGGJAAAE" -> null

        - rule {
            - detect_label          = "CPU utilization is greater than 90%" -> null
            - disabled              = false -> null
            - notifications         = [
                - "VictorOps,EaS2mowAIAA,zevn_PRI",
                ] -> null
            - parameterized_body    = <<~EOT
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
                EOT -> null
            - parameterized_subject = "{{ruleSeverity}} Alert: {{{ruleName}}} ({{{detectorName}}})" -> null
            - severity              = "Critical" -> null
            }
        }

    Plan: 0 to add, 0 to change, 1 to destroy.

    Do you really want to destroy all resources?
    Terraform will destroy all your managed infrastructure, as shown above.
    There is no undo. Only 'yes' will be accepted to confirm.

    Enter a value: yes
    ```
---

## Optional - Mulitpass VMs Only

If you are using a Multipass VM instead of an Splunk provided EC2 Instance you can now delete this instance. You will need to `exit` from the Multipass instance you are in to get back to your system command prompt.

You can use `multipass list` to get the names of any current running instances:

=== "Shell Command"

    ```text
    multipass list
    ```

=== "Example Output"

    ```
    Name                State             IPv4             Image
    zevn            Running           192.168.64.13    Ubuntu 18.04 LTS
    ```

If the `INSTANCE` environment variable is still set you can use this to delete the Multipass VM, to check run the following command:

=== "Shell Command"

    ```text
    echo ${INSTANCE}
    ```

If the environment variable is not set, then you will have to replace `${INSTANCE}` below with the prefix of the instance name from the `multipass list` above.

Run the following command to delete the Multipass instance:

=== "Shell Command"

    ```text
    multipass delete --purge ${INSTANCE}
    ```
