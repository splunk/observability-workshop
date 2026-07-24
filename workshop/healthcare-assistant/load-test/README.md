# Agentic AI Workshop Load Test

## Prerequisites

Ensure `sshpass` is installed on the host where the test will be run: 

``` bash
brew install sshpass
```

Provision an "AI Workshop" using SWiPE, then provision the desired number of EC2 instances using 
Splunk Show with the Splunk Observability 4 Ninjas template. Each EC2 instance will include an 
`OPENAI_API_KEY` and `OPENAI_BASE_URL`, which will be used by the application to connect to 
OpenAI models running in Azure. 

## Build and Install the Application

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
  --galileo-api-key "$GALILEO_API_KEY" \
  --max-parallel 10 \
  --insecure-hostkey
```

## Run the Load Test

Create the virtual environment: 

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

Run the load test: 

```bash
python loadtest_browser.py --csv <path to workshop csv file>
```

## Cleanup

Uninstall the application:

``` bash
./loadtest-uninstall-llm-app.sh \
  --csv "<path to workshop csv file>" \
  --max-parallel 10 \
  --insecure-hostkey
```
