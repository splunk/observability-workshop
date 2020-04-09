### 1. Removing the Multipass instance

Once you have finished with this workshop `exit` from the Multipass instance you are in and get back to your system command prompt and enter the following to delete the Multipass instance, replace `{YOUR_INITIALS}` with the ones you used in [4. Running the Smart Agent in Kubernetes (K3s)](https://signalfx.github.io/app-dev-workshop/module1/k3s/):

```
multipass delete --purge {YOUR_INITIALS}-k3s
```

!!! note
    If you are using a workshop instance on EC2 please ignore this and just terminate your instance.

=== "Input"
    ``` bash
    kubectl get pods
    ```

=== "Output"
    ```
    NAME                   READY   STATUS    RESTARTS   AGE
    signalfx-agent-66tvr   1/1     Running   0          7s
    ```
