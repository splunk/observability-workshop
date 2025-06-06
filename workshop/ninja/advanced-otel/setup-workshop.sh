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
echo "Workshop environment setup complete!"
