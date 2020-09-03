# Plan and Apply Terraform

## 1. Create an execution plan

Review the execution plan.

=== "Shell Command"

    ```text
    terraform plan -var="access_token=$ACCESS_TOKEN" -var="realm=$REALM" -var="sfx_prefix=[$(hostname)]"
    ```

If the plan executes successfully, we can go ahead and apply:

---

## 2. Apply actions from execution plan

=== "Shell Command"

    ```text
    terraform apply -var="access_token=$ACCESS_TOKEN" -var="realm=$REALM" -var="sfx_prefix=[$(hostname)]"
    ```

Validate that the detectors were created, under the _**Alerts → Detectors**_. They will be prefixed by the hostname of your instance. To check the prefix value run:

=== "Shell Command"

    ```text
    echo $(hostname)
    ```

 You will see a list of the new detectors and you can search for the prefix that was output from above.

![Detectors](../images/monitoring-as-code/detectors.png)

## 3. Destroy all your hard work

Destroy all Detectors and Dashboards that were previously applied.

=== "Shell Command"

    ```text
    terraform destroy -var="access_token=$ACCESS_TOKEN" -var="realm=$REALM"
    ```

Validate all the detectors have been removed by navigating to _**Alerts → Detectors**_

![Destroyed](../images/monitoring-as-code/destroy.png)
