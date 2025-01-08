#!/bin/sh
export SPLUNK_DEBUG_CONFIG_SERVER_PORT=55555
$HOME/collectors/otelcol_darwin_arm64 --config=gateway.yaml