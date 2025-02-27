## Notes from run through - 7th Feb 2025

- Verify QR code for workshop
- Verify links to documentation or GitHub
- Update to instruction change all terminal windows to current directory
- Add to the introduction if people are struggling, this workshop is designed you can still complete at a later date.

## Notes from 27th Feb 2025

- Mention vscode.dev
- For Mac user run `xattr -dr com.apple.quarantine otelcol`
- Think about sending trace to O11y Cloud to validate
- Do we move resilience to the end of the workshop?
- Agent Config:
  - Fully configured with `debug` exporter
  - Add `otlp` receiver
  - Update pipelines

```yaml
###########################        This section holds all the
## Configuration section ##        configurations that can be 
###########################        used in this OpenTelemetry Collector
extensions:                       # Array of Extensions
  health_check:                   # Configures the health check extension
    endpoint: 0.0.0.0:13133       # Endpoint to collect health check data

receivers:                        # Array of Receivers
  hostmetrics:                    # Receiver Type
    collection_interval: 3600s    # Scrape metrics every hour
    scrapers:                     # Array of hostmetric scrapers
      cpu:                        # Scraper for cpu metrics
  otlp:                           # Receiver Type
    protocols:                    # list of Protocols used 
      http:                       # This wil enable the HTTP Protocol
        endpoint: "0.0.0.0:4318"  # Endpoint for incoming telemetry data

exporters:                        # Array of Exporters
  debug:                          # Exporter Type
    verbosity: detailed           # Enabled detailed debug output

processors:                       # Array of Processors
  memory_limiter:                 # Limits memory usage by Collectors pipeline
    check_interval: 2s            # Interval to check memory usage
    limit_mib: 512                # Memory limit in MiB
  resourcedetection:              # Processor Type
    detectors: [system]           # Detect system resource information
    override: true                # Overwrites existing attributes
  resource/add_mode:              # Processor Type/Name
    attributes:                   # Array of attributes and modifications
    - action: insert              # Action is to insert a key
      key: otelcol.service.mode   # Key name
      value: "agent"              # Key value

###########################         This section controls what
### Activation Section  ###         configurations will be used
###########################         by this OpenTelemetry Collector
service:                          # Services configured for this Collector
  extensions:                     # Enabled extensions
  - health_check
  pipelines:                      # Array of configured pipelines
    traces:
      receivers:
      - otlp                      # OTLP Receiver
      processors:
      - memory_limiter            # Memory Limiter processor
      exporters:
      - debug                     # Debug Exporter
    metrics:
      receivers:
      - otlp                      # OTLP Receiver
      processors:
      - memory_limiter            # Memory Limiter processor
      exporters:
      - debug                     # Debug Exporter
    logs:
      receivers:
      - otlp                      # OTLP Receiver
      processors:
      - memory_limiter            # Memory Limiter processor
      exporters:
      - debug                     # Debug Exporter
```

- 1.3 File Exporter
  - Provide all pipeline configuration
- 1.4 Resource Metadata
  - Update to talk about the processors and what they do
  - Provide full pipeline configuration
- 2.1 Test Gateway
  - Add file/traces to gateway config
  - Update to only update pipelines
  - Rejig to make more sense and easier to follow
- 2.2 Configure Agent
  - Rejig to make more sense and easier to follow
  - Provide full pipeline configuration
- 2.3 Sort out batch processor
  - Reword gateway check
- 2.4 Rewrite for sending new trace to O11y Cloud
- 3.3 Stress that only the logs pipeline is being updated
- 4.1 Stress that only the metrics pipeline is being updated
- 5 Update span generator to include health span already
- 
