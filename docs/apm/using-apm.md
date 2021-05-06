# TBD

!!! info "OpenTelemetry Collector Only"
    To debug the traces being sent you can use the `zpages` extension. In order to view this first find the pod name of the OpenTelemetry
    Collector agent:

    ```
    sudo kubectl get pods
    ```

    === "Output"

        ```   
        NAME                                                          READY   STATUS    RESTARTS   AGE
        splunk-otel-collector-agent-gdr48                             1/1     Running   0          33m
        splunk-otel-collector-k8s-cluster-receiver-56585564cc-wghdn   1/1     Running   0          33m
        ```

    Copy the agent pod name and then run e.g.:

    ```
    sudo kubectl port-forward <replace_with_agent_pod_name> --address 0.0.0.0 :55679
    ```

    === "Output"
        ```
        Forwarding from 0.0.0.0:36143 -> 55679
        ```

    This command will create a new port that you can use to view `zpages` e.g.
        
    Use the port reported to connect from desktop e.g. `http://node_ip:36143/debug/tracez`

    ![zpages](../images/apm/zpages.png)
