# Agentic AI Workshop Load Test

## Prerequisites

Ensure `sshpass` is installed on the host where the test will be run: 

``` bash
brew install sshpass
```

## Run the Load Test

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

Build the application: 

``` bash
./loadtest-build-app.sh \
  --csv "<path to workshop csv file>" \
  --max-parallel 10 \
  --insecure-hostkey
```

Install the LLM application:

``` bash
./loadtest-install-app.sh \
  --csv "<path to workshop csv file>" \
  --azure-openai-key "$AZURE_OPENAI_KEY" \
  --ai-defense-url "$AI_DEFENSE_URL" \
  --max-parallel 10 \
  --insecure-hostkey
```

Load test the LLM application:

``` bash
./loadtest-llm-app.sh \
  --csv "<path to workshop csv file>" \
  --max-parallel 10 \
  --insecure-hostkey
```

## Cleanup

Uninstall the application:

``` bash
./loadtest-uninstall-llm-app.sh \
  --csv "<path to workshop csv file>" \
  --max-parallel 10 \
  --insecure-hostkey
```

Uninstall the collector: 

``` bash
./loadtest-uninstall-collector.sh \
  --csv "<path to workshop csv file>" \
  --max-parallel 10 \
  --insecure-hostkey
```