# Cheatsheet

## SMART AGENT and OTEL COLLECTOR COMMANDS

### CONNECTIVITY CHECK

```bash
curl https://ingest.us1.signalfx.com/healthz
```

### INGEST CHECK

```bash
curl -qs -H'X-SF-Token:XXXXXX' https://ingest.us1.signalfx.com/v2/datapoint -X POST -v -d '{}' -H "Content-Type: application/json"
```

### SMART AGENT TO OTEL COLLECTOR MIGRATION REFERENCE

https://github.com/signalfx/splunk-otel-collector/blob/main/docs/signalfx-smart-agent-migration.md

### SMART AGENT CHECK AGENT STATUS

```bash
sudo signalfx-agent status
service signalfx-agent status
systemctl signalfx-agent status
```

### SMART AGENT CHECK AGENT LOGS

```bash
journalctl -u signalfx-agent | tail -f
tail -f /var/log/signalfx-agent.log
```

### SPLK-OTEL-COLL CHECK AGENT LOGS

```bash
journalctl -u splunk-otel-collector -f
tail -100 /var/log/messages
```

### SMART AGENT START/STOP/RESTART

```bash
sudo systemctl restart signalfx-agent
sudo systemctl start signalfx-agent
sudo systemctl stop signalfx-agent
```

### SPLK-OTEL-COLL START/STOP/RESTART

```bash
sudo systemctl restart splunk-otel-collector
sudo systemctl start splunk-otel-collector
sudo systemctl stop splunk-otel-collector
```

### SPLK-OTEL-COLL FLUENTD START/STOP/RESTART

```bash
sudo systemctl restart td-agent
sudo systemctl start td-agent
sudo systemctl stop td-agent
```

### SMART AGENT DEFAULT CONFIG

```bash
/etc/signalfx/agent.yaml
```

### SPLK-OTEL-COLL DEFAULT CONFIG

```bash
/etc/otel/collector/agent_config.yaml
```

### SPLK-OTEL-COLL ENVIRONMENT FILE WITH REQUIRED VARIABLES/VALUES FOR SERVICE

```bash
/etc/otel/collector/splunk-otel-collector.conf
```

### SPLK-OTEL-COLL FLUENTD CONFIG

```bash
/etc/otel/collector/fluentd/fluent.conf
```

### SPLK-OTEL-COLL FLUENTD CONFIG DIRECTORY FOR ADDING FILES WITH .CONF EXT

```bash
/etc/otel/collector/fluentd/conf.d
```

### SMART AGENT TAIL METRIC DATAPOINTS BEING SENT

```bash
signalfx-agent tap-dps -h
signalfx-agent tap-dps -metric 'jenkins_*’
```

### SMART AGENT ENDPOINTS SET

```bash
signalfx-agent status endpoints
```

### SELINUX SETTING

```bash
chcon -t bin_t /usr/lib/signalfx-agent/bin/signalfx-agent
```

SMART AGENT STANDARD PORTS ARE 9080 and 8095

## KUBERNETES

### SMART AGENT CHECK AGENT STATUS

```bash
kubectl get pods
kubectl exec <signalfx-agent-PODNAME> -- signalfx-agent status
```

### OTEL AGENT CHECK AGENT STATUS

```bash
kubectl exec -it YOURAGENTPODHERE -- curl localhost:55679/debug/tracez | lynx -stdin
kubectl exec -it splunk-otel-collector-agent-f4gwg -- curl localhost:55679/debug/tracez | lynx -stdin
```

### OTEL INITIAL CONFIG

```bash
kubectl exec -it my-splunk-otel-collector-agent-hg4gk -- curl http://localhost:55554/debug/configz/initial
```

### OTEL effective CONFIG

```bash
kubectl exec -it my-splunk-otel-collector-agent-hg4gk -- curl http://localhost:55554/debug/effective
```

### SMART AGENT CHECK AGENT LOGS

```bash
kubectl logs -l app=signalfx-agent -f
```

### SPLK-OTEL-COLL CHECK AGENT LOGS

```bash
sudo kubectl logs -l app=splunk-otel-collector -f
sudo kubectl logs -l app=splunk-otel-collector -f -c otel-collector
```

### MODIFY EITHER AGENT CONFIGMAP

```bash
kubectl get configmap
kubectl edit cm splunk-otel-collector-otel-agent
sudo kubectl create configmap <nginxconfig> --from-file=workshop/k3s/nginx/nginx.conf
```

### SMART AGENT CONFIGMAP REFERENCE

https://github.com/signalfx/signalfx-agent/blob/main/deployments/k8s/configmap.yaml

### MODIFY EITHER AGENT DAEMONSET

```bash
kubectl get ds
kubectl edit ds splunk-otel-collector-agent
```

### SMART AGENT DAEMONSET REFERENCE

https://github.com/signalfx/signalfx-agent/blob/main/deployments/k8s/daemonset.yaml

### SMART AGENT HELM

```bash
helm repo add signalfx https://dl.signalfx.com/helm-repo && helm repo update
helm delete signalfx-agent
helm install \
--set signalFxAccessToken=$ACCESS_TOKEN \
--set clusterName=<MY-CLUSTER> \
--set kubeletAPI.url=https://localhost:10250 \
--set signalFxRealm=$REALM  \
--set traceEndpointUrl=https://ingest.$REALM.signalfx.com/v2/trace \
--set gatherDockerMetrics=false \
signalfx-agent signalfx/signalfx-agent \
-f ~/workshop/k3s/values.yaml
```

### SPLK-OTEL-COLL HELM

```bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart && helm repo update
helm delete splunk-otel-collector
helm uninstall splunk-otel-collector
helm install splunk-otel-collector \
--set="splunkRealm=$REALM" \
--set="splunkAccessToken=$ACCESS_TOKEN" \
--set="clusterName=<MY-CLUSTER>" \
--set="logsEnabled=false" \
--set="environment=$<MY-ENV>" \
splunk-otel-collector-chart/splunk-otel-collector \
-f ~/workshop/k3s/otel-collector.yaml
kubectl get pods
kubectl get pods -n kube-system
kubectl get svc
kubectl describe pod signalfx-agent-86zg4
kubectl delete pod,service baz foo
```

### CREATE/DELETE DEPLOYMENT FROM FILE

```bash
sudo kubectl create -f nginx-deployment.yaml
sudo kubectl delete -f nginx-deployment.yaml
```

### CHECK SYSTEM CONFIGS

```bash
kubectl describe -n kube-system pod <metrics-server-6d684c7b5-gm778>
```

### SHOW KUBECONFIG SETTINGS

```bash
kubectl config view
```

### SAVE NAMESPACE FOR ALL SUBSEQUENT KUBECTL COMMANDS IN CONTEXT

```bash
kubectl config set-context --current --namespace=ggckad-s2
```

### USE MULTIPLE KUBECONFIG FILES

```bash
KUBECONFIG=~/.kube/config:~/.kube/kubconfig2
```

### get the password for the e2e user

```bash
kubectl config view -o jsonpath='{.users[?(@.name == "e2e")].user.password}'
kubectl config view -o jsonpath='{.users[].name}'    # display the first user
kubectl config view -o jsonpath='{.users[*].name}'   # get a list of users
kubectl config get-contexts                          # display list of contexts
kubectl config current-context                       # display the current-context
kubectl config use-context my-cluster-name           # set the default context to my-cluster-name
```

### add a new user to your kubeconf that supports basic auth

```bash
kubectl config set-credentials kubeuser/foo.kubernetes.com --username=kubeuser --password=kubepassword
```

### set a context utilizing a specific username and namespace

```bash
kubectl config set-context gce --user=cluster-admin --namespace=foo \
  && kubectl config use-context gce
```

### Return snapshot logs from pod nginx with only one container

```bash
kubectl logs nginx
```

### Return snapshot logs from pod nginx with multi containers

```bash
kubectl logs nginx --all-containers=true
```

### Return snapshot logs from all containers in pods defined by label app=nginx

```bash
kubectl logs -l app=nginx --all-containers=true
```

### Return snapshot of previous terminated ruby container logs from pod web-1

```bash
kubectl logs -p -c ruby web-1
```

### Begin streaming the logs of the ruby container in pod web-1

```bash
kubectl logs -f -c ruby web-1
```

### Begin streaming the logs from all containers in pods defined by label app=nginx

```bash
kubectl logs -f -lapp=nginx --all-containers=true
```

### Display only the most recent 20 lines of output in pod nginx

```bash
kubectl logs --tail=20 nginx
```

### Show all logs from pod nginx written in the last hour

```bash
kubectl logs --since=1h nginx
```

### Show logs from a kubelet with an expired serving certificate

```bash
kubectl logs --insecure-skip-tls-verify-backend nginx
```

### Return snapshot logs from first container of a job named hello

```bash
kubectl logs job/hello
```

### Return snapshot logs from container nginx-1 of a deployment named nginx

```bash
kubectl logs deployment/nginx -c nginx-1
```

## LOGS

### log ingest test

```bash
curl -v -X POST -H "Content-Type: application/json" -H "Authorization: Splunk {INGEST_TOKEN}" https://ingest.us1.signalfx.com/v1/log -d '{"event": "hello world", "fields": {"foo": "bar"}}'
```

```bash
curl -H "Authorization: Splunk <ACCESS_TOKEN>" -H "Content-Type: application/json" https://ingest.eu0.signalfx.com/v1/log -d '{"sourcetype": "iracing", "event": "Cory into the Pits, lap 12"}'
```
