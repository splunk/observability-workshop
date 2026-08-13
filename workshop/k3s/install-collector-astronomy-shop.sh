helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart && helm repo update
helm upgrade --install splunk-otel-collector \
--set="splunkObservability.realm=$REALM" \
--set="splunkObservability.accessToken=$ACCESS_TOKEN" \
--set="clusterName=$INSTANCE-k3d-cluster" \
--set="splunkObservability.profilingEnabled=true" \
--set="splunkObservability.secureAppEnabled=true" \
--set="agent.service.enabled=true"  \
--set="environment=$INSTANCE" \
--set="splunkPlatform.endpoint=$HEC_URL" \
--set="splunkPlatform.token=$HEC_TOKEN" \
--set="splunkPlatform.index=splunk4rookies-workshop" \
--set="agent.featureGates=splunk.opamp.enabled" \
--set="clusterReceiver.featureGates=splunk.opamp.enabled" \
splunk-otel-collector-chart/splunk-otel-collector \
-f ~/workshop/apm/splunk-astronomy-shop/splunk-astronomy-shop-latest.yaml
