# Cisco AI POD Workshop Load Test

``` bash
./loadtest-install-collector.sh \
  --access-token "$ACCESS_TOKEN" \
  --realm us1 \
  --hec-url "https://<hec-host>:8088/services/collector" \
  --hec-token "<token>" \
  --splunk-index "splunk4rookies-workshop" \
  --cluster-api "https://api.<cluster>:443" \
  --password '<password>' \
  --users 30 \
  --max-parallel 10
```