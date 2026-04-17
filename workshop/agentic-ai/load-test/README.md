# Agentic AI Workshop Load Test

Ensure `sshpass` is installed on the host where the test will be run: 

``` bash
brew install sshpass
```

Load test the collector installation:

``` bash
./loadtest-install-collector.sh \
  --csv "<path to workshop csv file>" \
  --access-token "$ACCESS_TOKEN" \
  --realm us1 \
  --hec-url "https://<hec-host>:8088/services/collector" \
  --hec-token "<token>" \
  --splunk-index "splunk4rookies-workshop" \
  --max-parallel 10 \
  --insecure-hostkey
```

Load test the LLM application:

``` bash
./loadtest-llm-app.sh \
  --cluster-api "https://api.<cluster>:443" \
  --password '<password>' \
  --users 30 \
  --max-parallel 10
```