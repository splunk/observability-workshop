---
title: OpenTelemetry Collector Development
linkTitle: 8.2 Configuration
weight: 10 
---

## Building The Configuration

The configuration portion of the component is how the user is able to have their inputs over the component,
so the values that is used for the configuration need to be:

1. Intuitive for users to understand what that field controls
1. Be explicit in what is required and what is optional
1. Reuse common names and fields
1. Keep the options simple

{{% tabs %}}
{{% tab title="bad config" %}}

```yaml
---
jenkins_server_addr: hostname
jenkins_server_api_port: 8089
interval: 10m
filter_builds_by:
    - name: my-awesome-build
      status: amber
track:
    values:
        example.metric.1: yes
        example.metric.2: yes
        example.metric.3: no
        example.metric.4: no
```

{{% /tab %}}
{{% tab title="good config" %}}

``` yaml
---
# Required Values
endpoint: http://my-jenkins-server:8089
auth:
    authenticator: basicauth/jenkins
# Optional Values
collection_interval: 10m
metrics:
    example.metric.1:
        enabled: true
    example.metric.2:
        enabled: true
    example.metric.3:
        enabled: true
    example.metric.4:
        enabled: true
```

{{% /tab %}}
{{% /tabs %}}

The bad configuration highlights how doing the opposite of the recommendations of configuration practices impacts the usability
of the component. It doesn't make it clear what field values should be, it includes features that can be pushed to existing processors,
and the field naming is not consistent with other components that exist in the collector.

The good configuration keeps the required values simple, reuses field names from other components, and ensures the component focuses on
just the interaction between Jenkins and the collector.

The code tab shows how much is required to be added by us and what is already provided for us by shared libraries within the collector.
These will be explained in more detail once we get to the business logic. The configuration should start off small and will change
once the business logic has started to include additional features that is needed.

## Write the code

In order to implement the code needed for the configuration, we are going to create a new file named `config.go` with the following content:

``` go
package jenkinscireceiver

import (
    "go.opentelemetry.io/collector/config/confighttp"
    "go.opentelemetry.io/collector/receiver/scraperhelper"

    "splunk.conf/workshop/example/jenkinscireceiver/internal/metadata"
)

type Config struct {
    // HTTPClientSettings contains all the values
    // that are commonly shared across all HTTP interactions
    // performed by the collector.
    confighttp.HTTPClientSettings `mapstructure:",squash"`
    // ScraperControllerSettings will allow us to schedule 
    // how often to check for updates to builds.
    scraperhelper.ScraperControllerSettings `mapstructure:",squash"`
    // MetricsBuilderConfig contains all the metrics
    // that can be configured.
    metadata.MetricsBuilderConfig `mapstructure:",squash"`
}
```
