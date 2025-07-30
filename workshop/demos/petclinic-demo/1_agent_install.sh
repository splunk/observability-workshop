export INSTANCE=petclinic-us
export REALM=us1
export ACCESS_TOKEN=XXX

helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart

helm repo update

helm install splunk-otel-collector --version 0.130.0 \
--set="operatorcrds.install=true", \
--set="operator.enabled=true", \
--set="splunkObservability.realm=$REALM" \
--set="splunkObservability.accessToken=$ACCESS_TOKEN" \
--set="clusterName=$INSTANCE-k3s-cluster" \
--set="splunkObservability.profilingEnabled=true" \
--set="agent.service.enabled=true"  \
--set="environment=$INSTANCE" \
splunk-otel-collector-chart/splunk-otel-collector \
-f ./otel-collector.yaml
