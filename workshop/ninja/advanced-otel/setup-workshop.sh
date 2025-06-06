#!/bin/bash

# Splunk Workshop Setup Script
# This script displays the Splunk ASCII art and creates workshop directories
echo ""
echo "███████╗██████╗ ██╗     ██╗   ██╗███╗   ██╗██╗  ██╗    ██╗"
echo "██╔════╝██╔══██╗██║     ██║   ██║████╗  ██║██║ ██╔╝    ╚██╗"
echo "███████╗██████╔╝██║     ██║   ██║██╔██╗ ██║█████╔╝      ╚██╗"
echo "╚════██║██╔═══╝ ██║     ██║   ██║██║╚██╗██║██╔═██╗      ██╔╝"
echo "███████║██║     ███████╗╚██████╔╝██║ ╚████║██║  ██╗    ██╔╝"
echo "╚══════╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝    ╚═╝"
echo ""
echo "Welcome to the Splunk Advanced OpenTelemetry Workshop!"
echo "======================================================"
echo ""

# Create workshop directories
echo "Creating workshop directories..."

# Common workshop subdirectories
mkdir -p 1-agent-gateway
mkdir -p 2-reslience
mkdir -p 3-dropping-spans
mkdir -p 4-senstive-data
mkdir -p 5-transform-data
mkdir -p 6-routing


echo "✓ Created subdirectories:"
echo "  ├── 1-agent-gateway"
echo "  ├── 2-building-resilience"
echo "  ├── 3-dropping-spans"
echo "  ├── 4-sensitive-data"
echo "  ├── 5-transform-data"
echo "  └── 6-routing-data"
echo ""

# Set default filename if not provided as argument
AGENT_CONFIG_FILE="1-agent-gateway/agent.yaml"

echo "Creating OpenTelemetry Collector agent configuration file: ${AGENT_CONFIG_FILE}"

# Write the configuration to the file
cat > "${AGENT_CONFIG_FILE}" << 'EOF'
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
  otlphttp:                       # Exporter Type
    endpoint: "http://localhost:5318"  # Gateway OTLP endpoint  
  file:                           # Exporter Type
    path: "./agent.out"           # Save path (OTLP JSON)
    append: false                 # Overwrite the file each time
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
      - otlp
      processors:
      - memory_limiter            # Memory Limiter processor
      - resourcedetection         # Adds system attributes to the data
      - resource/add_mode         # Adds collector mode metadata
      exporters:
      - debug
      - file
      - otlphttp
    metrics:
      receivers:
      - hostmetrics.              # Hostmetric reciever (cpu only)
      - otlp
      processors:
      - memory_limiter            # Memory Limiter processor
      - resourcedetection         # Adds system attributes to the data
      - resource/add_mode         # Adds collector mode metadata
      exporters:
      - debug
      - file
      - otlphttp
    logs:
      receivers:
      - otlp
      processors:
      - memory_limiter            # Memory Limiter processor
      - resourcedetection         # Adds system attributes to the data
      - resource/add_mode         # Adds collector mode metadata
      exporters:
      - debug
      - file
      - otlphttp
EOF

# Check if the file was created successfully
if [ $? -eq 0 ]; then
    echo "✓ Configuration file created successfully: ${AGENT_CONFIG_FILE}"
    echo "✓ File size: $(wc -c < "${AGENT_CONFIG_FILE}") bytes"
    echo ""
else
    echo "✗ Error: Failed to create configuration file"
    exit 1
fi

# Set default filename if not provided as argument
GATEWAY_CONFIG_FILE="1-agent-gateway/gateway.yaml"

echo "Creating OpenTelemetry Collector gateway configuration file: ${GATEWAY_CONFIG_FILE}"

# Write the configuration to the file
cat > "${GATEWAY_CONFIG_FILE}" << 'EOF'
###########################         This section holds all the
## Configuration section ##         configurations that can be 
###########################         used in this OpenTelemetry Collector
extensions:                       # List of extensions
  health_check:                   # Health check extension
    endpoint: 0.0.0.0:14133       # Custom port to avoid conflicts

receivers:
  otlp:                           # OTLP receiver
    protocols:
      http:                       # HTTP protocol
        endpoint: "0.0.0.0:5318"  # Custom port to avoid conflicts
        include_metadata: true    # Required for token pass-through

exporters:                        # List of exporters
  debug:                          # Debug exporter
    verbosity: detailed           # Enable detailed debug output
  file/traces:                    # Exporter Type/Name
    path: "./gateway-traces.out"  # Path for OTLP JSON output
    append: false                 # Overwrite the file each time
  file/metrics:                   # Exporter Type/Name
    path: "./gateway-metrics.out" # Path for OTLP JSON output
    append: false                 # Overwrite the file each time
  file/logs:                      # Exporter Type/Name
    path: "./gateway-logs.out"    # Path for OTLP JSON output
    append: false                 # Overwrite the file each time

processors:                       # List of processors
  memory_limiter:                 # Limits memory usage
    check_interval: 2s            # Memory check interval
    limit_mib: 512                # Memory limit in MiB
  batch:                          # Batches data before exporting
    metadata_keys:                # Groups data by token
    - X-SF-Token
  resource/add_mode:              # Adds metadata
    attributes:
    - action: upsert              # Inserts or updates a key
      key: otelcol.service.mode   # Key name
      value: "gateway"            # Key value

# Connectors
#connectors:                      # leave this commented out; we will uncomment in an upcoming exercise

###########################
### Activation Section  ###
###########################
service:                          # Service configuration
  telemetry:
    metrics:
      level: none                 # Disable metrics
  extensions: [health_check]      # Enabled extensions
  pipelines:                      # Configured pipelines
    traces:                       # Traces pipeline
      receivers:
      - otlp                      # OTLP receiver
      processors:                 # Processors for traces
      - memory_limiter
      - resource/add_mode
      - batch
      exporters:
      - debug                     # Debug exporter
      - file/traces
    metrics:                      # Metrics pipeline
      receivers:
      - otlp                      # OTLP receiver
      processors:                 # Processors for metrics
      - memory_limiter
      - resource/add_mode
      - batch
      exporters:
      - debug                     # Debug exporter
      - file/metrics
    logs:                         # Logs pipeline
      receivers:
      - otlp                      # OTLP receiver
      processors:                 # Processors for logs
      - memory_limiter
      - resource/add_mode
      - batch
      exporters:
      - debug                     # Debug exporter
      - file/logs
EOF

# Check if the file was created successfully
if [ $? -eq 0 ]; then
    echo "✓ Configuration file created successfully: ${GATEWAY_CONFIG_FILE}"
    echo "✓ File size: $(wc -c < "${GATEWAY_CONFIG_FILE}") bytes"
    echo ""
else
    echo "✗ Error: Failed to create configuration file"
    exit 1
fi

echo "Workshop environment setup complete!"