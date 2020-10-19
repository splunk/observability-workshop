# Open Telemetry Collector

The collector is an optional component between the smart agent and SaaS ingest. In this configuration we are using the `sapm` endpoint to receive traces.

To use it:

1. Install with helm:

    Add the repository with
    ```
    cd $HOME
    helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
    ```

    Then

    ```
    helm install \
    --set standaloneCollector.configOverride.exporters.signalfx.realm=$REALM \
    --set standaloneCollector.configOverride.exporters.signalfx.access_token=$ACCESS_TOKEN \
    --set standaloneCollector.configOverride.exporters.sapm.access_token=$ACCESS_TOKEN \
    --set standaloneCollector.configOverride.exporters.sapm.endpoint=https://ingest.$REALM.signalfx.com/v2/trace \
    opentelemetry-collector open-telemetry/opentelemetry-collector -f ~/workshop/otel/collector.yaml
    ```

1. Check that it is running and ready.

    ```
    kc logs -l app.kubernetes.io/name=opentelemetry-collector
    ```

    Look for a log entry with
    ```
    ... "msg":"Everything is ready. Begin running and processing data."}
    ```

    Validate that it's running as a service and has a sapm endpoint on port 7276.

    ```
    kubectl get svc opentelemetry-collector
    ```

    Sample output:

    ```
    NAME                      TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                                           AGE
    opentelemetry-collector   ClusterIP   10.43.119.140   <none>        14250/TCP,14268/TCP,55680/TCP,7276/TCP,9411/TCP   13m
    ```

    TODO: use health check!

1. Reconfigure the agent to send traces in `sapm` format and point it to ingest.

    Add to the top of `~/workshop/k3s/values.yaml`:
    ```
    writer:
      traceExportFormat: sapm
    ```

    Uninstall the agent:

    ```
    helm uninstall signalfx-agent
    ```

    Reinstall with `traceEndpointUrl` set to point to OpenTelemetry Collector:

    ```
    helm install \
    --set signalFxAccessToken=$ACCESS_TOKEN \
    --set clusterName=$(hostname)-k3s-cluster \
    --set kubeletAPI.url=https://localhost:10250 \
    --set signalFxRealm=$REALM \
    --set traceEndpointUrl=http://opentelemetry-collector:7276/v2/trace \
    --set gatherDockerMetrics=false \
    signalfx-agent signalfx/signalfx-agent \
    -f ~/workshop/k3s/values.yaml
    ```

1. Check the OpenTelemetry Collector dashboards and validate metrics and spans are being sent.
