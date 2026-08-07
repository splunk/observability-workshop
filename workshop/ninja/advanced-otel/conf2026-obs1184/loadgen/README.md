# .conf26 Advanced Collector load generator

This workshop-specific version preserves the existing trace and log generation
behavior and adds `-preview`, which prints the original OTLP JSON payload
without sending it to a Collector.

Build all workshop targets with:

```bash
GOCACHE=/tmp/obs1184-go-build-cache ./build.sh
```

Attendee download links use the platform binaries in `build/`.
