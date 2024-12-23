#!/bin/sh
# Read in the file of environment settings
. /$HOME/.splunk-otel-dotnet/instrument.sh

# Then run the CMD
exec "$@"