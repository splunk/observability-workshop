# Destroy Terraform

## 1. Destroy all your hard work

You will first need to ensure you are in the the workspace you created in **Step #1**:

=== "Shell Command"

    ```text
    terraform workspace select workshop
    ```

Destroy all Detectors and Dashboards that were previously applied.

=== "Shell Command"

    ```bash
    terraform destroy -var="access_token=$ACCESS_TOKEN" -var="realm=$REALM"
    ```

Validate all the detectors have been removed by navigating to _**ALERTS → Detectors**_

![Destroyed](../images/monitoring-as-code/destroy.png)
