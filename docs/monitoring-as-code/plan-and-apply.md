# Plan and Apply Terraform

## 1. Create an execution plan

Review the execution plan.

=== "Shell Command"

    ``` bash
    terraform plan -var="access_token=$ACCESS_TOKEN" -var="realm=$REALM" -var="sfx_prefix=$PREFIX"
    ```

If the plan executes successfully, we can go ahead and apply:

---

## 2. Apply actions from execution plan

=== "Shell Command"

    ``` bash
    terraform apply -var="access_token=$ACCESS_TOKEN" -var="realm=$REALM" -var="sfx_prefix=$PREFIX"
    ```

Validate that the detectors were created, under the _**ALERTS → Detectors**_, you should see a list of new detectors with the a prefix of your initials:

![Detectors](../images/monitoring-as-code/detectors.png)
