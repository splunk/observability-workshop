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

Validate that the detectors were created, under the _**ALERTS → Detectors**_. They will be prefixed by a unique string that was initialized in the setup. To check the prefix value run:

=== "Shell Command"

    ```bash
    echo ${PREFIX}
    ```

 You will see a list of the new detectors and you can search for the prefix that was output from above.

![Detectors](../images/monitoring-as-code/detectors.png)

## 3. Destroy all your hard work

Destroy all Detectors and Dashboards that were previously applied.

=== "Shell Command"

    ```bash
    terraform destroy -var="access_token=$ACCESS_TOKEN" -var="realm=$REALM"
    ```

Validate all the detectors have been removed by navigating to _**ALERTS → Detectors**_

![Destroyed](../images/monitoring-as-code/destroy.png)
