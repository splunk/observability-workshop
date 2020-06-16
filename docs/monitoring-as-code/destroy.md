# Destroy Terraform

## 1. Destroy all your hard work

Destroy all Detectors and Dashboards that were previously applied.

=== "Shell Command"

    ```bash
    terraform destroy -var="access_token=$ACCESS_TOKEN" -var="realm=$REALM"
    ```

Validate all the detectors have been removed by navigating to _**ALERTS → Detectors**_

![Destroyed](../images/monitoring-as-code/destroy.png)
