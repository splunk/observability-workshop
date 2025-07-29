sudo systemctl stop petclinic_owners_loadgen.service

kubectl delete -f petclinic-deploy.yaml

helm uninstall splunk-otel-collector