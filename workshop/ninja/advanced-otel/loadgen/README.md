# .conf26 Advanced Collector load generator

This workshop-specific version preserves the existing trace and log generation
behavior and adds `-preview`, which prints the original OTLP JSON payload
without sending it to a Collector.

The workshop includes three prebuilt binaries because attendees aren't
required to install Go. They cover Apple silicon, Linux AMD64, and Linux ARM64.
Intel-based Macs use a Splunk Show instance.

From this `loadgen` directory, build the supported workshop targets with:

```bash
GOCACHE=/tmp/obs1184-go-build-cache ./build.sh
```

Attendee download links use the matching platform binary in `build/`.
