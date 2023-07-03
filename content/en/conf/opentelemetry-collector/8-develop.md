---
title: OpenTelemetry Collector Development
linkTitle: 8. Develop
weight: 8
---

## Developing a custom component

Building a component for the Open Telemetry Collector requires three key parts:

1. The Configuration - _What values are exposed to the user to configure_
1. The Factory - _Make the component using the provided values_
1. The Business Logic - _What the component needs to do_

For this, we will use the example of building a component that works with Jenkins 
so that we can track important DevOps metrics of our project(s).

The metrics we are looking to measure are:

1. Lead time for changes - _"How long it takes for a commit to get into production"_
1. Change failure rate   - _"The percentage of deployments causing a failure in production"_
1. Deployment frequency  - _"How often a [team] successfully releases to production"_
1. Mean time to recover  - _"How long does it take for a [team] to recover from a failure in production"_

These indicators were identified Google's DevOps Research and Assesment (DORA)[^1] team to help
show performance of a software development team. The reason for choosing _Jenkins CI_ 
is that we remain in the same Open Source Software ecosystem which we can serve as the example
for the vendor managed CI tools to adopt in future.

## Instrument Vs Component

There is something to consider when improving level of Observability within your organisation
since there are some trade offs that get made.

<table>
    <thead>
        <th></th>
        <th style="text-align:center">Pros</th>
        <th style="text-align:center">Cons</th>
    </thead>
    <tbody>
        <tr>
            <th>(Auto) Instrumented</th>
            <td>
- Does not require an external API to be monitored in order to observe the system. </br>
- Gives system owners/developers to make changes in their observability. </br>
- Understands system context and can corrolate captured data with <i>Exemplars</i>.
            </td>
            <td>
- Changing instrumentation requires changes to the project.</br>
- Requires additional runtime dependancies. </br>
- Can impact performance of the system.
            </td>
        </tr>
        <tr>
            <th>Component</th>
            <td>
- Changes to data names or semantics can be rolled out independantly of the system's release cycle. </br>
- Updating/extending data collected is a seemless user facing change. </br>
- Does not require the supporting teams to have a deep understanding of observability practice.
            </td>
            <td>
- Breaking API changes require a coordinated release between system and collector. </br>
- Captured data semantics can unexpectedly break that does not align with a new system release. </br> 
- Strictly external / exposed information can be surfaced from the system.
            </td>
        </tr>
    </tbody>
</table>


## Component Review

To recap the type of component we will need to in order to capture metrics from Jenkins:

{{% tabs %}}
{{% tab title="Extension" %}}
The business usecase an extension helps solves for are:

1. Having shared functionality that requires runtime configuration
1. Indirectly helps with observing the runtime of the collector

See [Extensions Overview](/en/conf/opentelemetry-collector/2-extensions) for more details.
{{% /tab %}}
{{% tab title="Receiver" %}}
The business usecase a receiver solves for:

- Fetching data from a remote source
- Receiving data from remote source(s)

This are commonly referred to _pull_ vs _push_ based data collection, 
and you read more about the details in the [Receiver Overview](/en/conf/opentelemetry-collector/3-receivers).
{{% /tab %}}
{{% tab title="Processor" %}}
The business usecase a processor solves for is:

- Adding or removing data, fields, or values
- Observing and making decisions on the data
- Buffering, queueing, and reorodering 

The thing to keep in mind that the data type flowing through a processor needs to use the forward
the same data type to its downstream components. 
Read through [Processor Overview](/en/conf/opentelemetry-collector/4-processors) for the details.
{{% /tab %}}
{{% tab title="Exporter" %}}
The business usecase an exporter solves for:

- Send the data to a tool, service, or storage

The OpenTelemetry collector does not want to be "backend", an all in one observability suite, but rather
keep to the principles that founded OpenTelemetry to begin with; A vendor agnostic Observability for all.
To help revist the details, please read through [Exporter Overview](/en/conf/opentelemetry-collector/5-exporters).

{{% /tab %}}
{{% tab title="{{% badge style=primary icon=user-ninja %}}**Ninja:** Connectors{{% /badge %}}"  %}}

This is a component type that was missed in the workshop since it is a relatively new addition to the collector,
but the best way to think about a connector is that it is like a processor that allows to be used across different 
telemetry types, and pipelines. Meaning that a connector can accept data as logs, and output metrics, or accept 
metrics from one pipeline and provide metrics on the data it has observed.

The business case that a connector solves for:

- Converting from different telemetry types
    - logs to metrics
    - traces to metrics
    - metrics to logs
- Observing incoming data and producing its own data
    - Accepting metrics and generating analytical metrics of the data.

There was a brief overview within the **Ninja** section as part of the [Processor Overview](/en/conf/opentelemetry-collector/4-processors),
and be sure what the project for updates for new connector components.
{{% /tab %}}
{{% /tabs %}}

From the component overviews, it is clear that developing a pull based receiver for Jenkins.


## Project Setup {{% badge style=primary icon=user-ninja %}}**Ninja**{{% /badge %}}

{{% notice style="note" %}}

The time to finish this section of the workshop can vary depending on experience.


A complete solution can be found [here](#create-link-to-src-code) incase you're stuck or want to follow
along with the instructor.

{{% /notice %}}

To get started developing a the new _Jenkins CI_ receiver, we first need to set up a Golang project.
The steps to create your new Golang project is:

1. Create a new directoy named `${HOME}/go/src/jenkinscireceiver` and change into it
    1. The actual directory name or location is not strict, 
    you can choose your own development directory to make it in.
1. Initialise the golang module by going `go mod init splunk.conf/workshop/example/jenkinscireceiver`
    1. This will create a file named `go.mod` which is used to track our direct and indirect dependencies
    1. Eventually there will be a `go.sum` which is the checksum values of the depedancies being imported.

{{% expand title="{{% badge icon=check color=green title=**Check-in** %}}Review your go.mod{{% /badge %}}" %}}

```
module splunk.conf/workshop/example/jenkinscireceiver

go 1.20
```

{{% /expand %}}

## Building The Configuration

The configuration portion of the component is how the user is able to have their inputs over the component,
so the values that is used for the configuration need to be:

1. Intuative for users to understand what that field controls
1. Be explict in what is required and what is optional
1. Reuse common names and fields
1. Keep the options simple

{{% tabs %}}
{{% tab title="bad config" %}}

```yaml
---
jenkins_server_addr: hostname
jenkins_server_api_port: 8089
interval: 10m
fitler_builds_by:
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
```yaml
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
{{% tab title="config.go" %}}
```go
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
{{% /tab %}}
{{% /tabs %}}

The bad configuration highlights how doing the opposite of the recomendations of configuration practices impacts the usability
of the component. It doesn't make it clear what field values should be, it includes features that can be pushed to existing processors,
and the field naming is not consistent with other components that exist in the collector.

The good configuration keeps the required values simple, reuses field names from other components, and ensures the component focuses on
just the interaction between Jenkins and the collector.

The code tab shows how much is required to be added by us and what is already provided for us by shared libraries within the collector.
These will be explained in more detail once we get to the business logic. The configuration should start off small and will change
once the business logic has started to include additional features that is needed.

### Designing The Metrics

To help define and export the metrics captured by our receiver, we will be using, 
[mdatagen](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/cmd/mdatagen),
a tool developed for the collector that turns yaml defined metrics into code.

{{% tabs %}}
{{% tab title="metadata.yaml"%}}
```yaml
---
# Type defines the name to reference the component
# in the configuration file
type: jenkins

# Status defines the component type and the stability level
status:
  class: receiver
  stability:
    development: [metrics]

# Attributes are the expected fields reported
# with the exported values.
attributes:
  job.name:
    description: The name of the associated Jenkins job
    type: string
  job.status:
    description: Shows if the job had passed, or failed
    type: string
    enum:
    - failed
    - success
    - unknown

# Metrics defines all the pontentially exported values from this receiver. 
metrics:
  jenkins.jobs.count:
    enabled: true
    description: Provides a count of the total number of configured jobs
    unit: "{Count}"
    gauge:
      value_type: int
  jenkins.job.duration:
    enabled: true
    description: Show the duration of the job
    unit: "s"
    gauge:
      value_type: int
    attributes:
    - job.name
    - job.status
  jenkins.job.commit_delta:
    enabled: true
    description: The calculation difference of the time job was finished minus commit timestamp
    unit: "s"
    gauge:
      value_type: int
    attributes:
    - job.name
    - job.status
```
{{% /tab %}}
{{% tab title="gen.go" %}}
```go
// To generate the additional code needed to capture metrics, 
// the following command to be run from the shell:
//  go generate -x ./...

//go:generate go run github.com/open-telemetry/opentelemetry-collector-contrib/cmd/mdatagen@v0.80.0 metadata.yaml
package jenkinscireceiver

// There is no code defined within this file.
```
{{% /tab%}}
{{% /tabs %}}

Create these files within the project folder before continuing onto the next section.

## Building The Factory

The Factory is a software design pattern that effectively allows for an object, in this case a `jenkinscireceiver`, to be created
dynamically with the provided configuration. To use a more real world example, it would be going to a phone store, asking for a phone
that matches your exact description, and then provides it to you.

Run the following command `go generate -x ./...` , it will create a new folder, `jenkinscireceiver/internal/metadata`,
that contains all code required to export the defined metrics. The required code is:

{{% tabs %}}
{{% tab title="factory.go" %}}
```go
package jenkinscireceiver

import (
    "errors"

    "go.opentelemetry.io/collector/component"
    "go.opentelemetry.io/collector/config/confighttp"
    "go.opentelemetry.io/collector/receiver"
    "go.opentelemetry.io/collector/receiver/scraperhelper"

    "splunk.conf/workshop/example/jenkinscireceiver/internal/metadata"
)

func NewFactory() receiver.Factory {
    return receiver.NewFactory(
        metadata.Type,
        newDefaultConfig,
        receiver.WithMetrics(newMetricsReceiver, metadata.MetricsStability),
    )
}

func newMetricsReceiver(_ context.Context, set receiver.CreateSettings, cfg component.Config, consumer consumer.Metrics) (receiver.Metrics, error) {
    // Convert the configuration into the expected type
    conf, ok := cfg.(*Config)
    if !ok {
        return nil, errors.New("can not convert config")
    }
    sc, err := newScraper(conf, set)
    if err != nil {
        return nil, err
    }
    return scraperhelper.NewScraperControllerReceiver(
        &conf.ScraperControllerSettings,
        set,
        consumer,
        scraperhelper.AddScraper(sc),
    )
}
```
{{% /tab %}}
{{% tab title="config.go" %}}
```go
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

func newDefaultConfig() component.Config {
    return &Config{
        ScraperControllerSettings: scraperhelper.NewDefaultScraperControllerSettings(metadata.Type),
        HTTPClientSettings:        confighttp.NewDefaultHTTPClientSettings(),
        MetricsBuilderConfig:      metadata.DefaultMetricsBuilderConfig(),
    }
}
```
{{% /tab %}}
{{% tab title="scraper.go" %}}
```go
package jenkinscireceiver

type scraper struct {}

func newScraper(cfg *Config, set receiver.CreateSettings) (scraperhelper.Scraper, error) {
    // Create a our scraper with our values 
    s := scraper{
        // To be filled in later
    }
    return scraperhelper.NewScraper(metadata.Type, s.scrape)
}

func (scraper) scrape(ctx context.Context) (pmetric.Metrics, error) {
    // To be filled in
    return pmetrics.NewMetrics(), nil
}

```
{{% /tab %}}
{{% tab title="build-config.yaml" %}}
```yaml
---
dist:
  name: otelcol
  description: "Conf workshop collector"
  output_path: ./dist
  version: v0.0.0-experimental

extensions:
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/extension/basicauthextension v0.80.0
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/extension/healthcheckextension v0.80.0

receivers:
  - gomod: go.opentelemetry.io/collector/receiver/otlpreceiver v0.80.0
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/jaegerreceiver v0.80.0
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/prometheusreceiver v0.80.0
  - gomod: splunk.conf/workshop/example/jenkinscireceiver v0.0.0
    path: ./jenkinscireceiver

processors:
  - gomod: go.opentelemetry.io/collector/processor/batchprocessor v0.80.0

exporters:
  - gomod: go.opentelemetry.io/collector/exporter/loggingexporter v0.80.0
  - gomod: go.opentelemetry.io/collector/exporter/otlpexporter v0.80.0
  - gomod: go.opentelemetry.io/collector/exporter/otlphttpexporter v0.80.0

# This replace is a go directive that allows for redefine
# where to fetch the code to use since the default would be from a remote project.
replaces:
- splunk.conf/workshop/example/jenkinscireceiver => ./jenkinscireceiver
```
{{% /tab %}}
{{% tab title="project layout" %}}
```
├── build-config.yaml
└── jenkinscireceiver
    ├── go.mod
    ├── config.go
    ├── factory.go
    ├── scraper.go
    └── internal
      └── metadata
```
{{% /tab %}}
{{% /tabs %}}

Once you have written these file into the project with the expected contents then run, `go mod tidy`,
which will fetch all the remote depedancies and update `go.mod` and generate the `go.sum` files.


## Building The Business Logic

At this point, we have a custom component that currently does nothing so we need to add in the required
logic to capture this data from Jenkins.

From this point, the steps that we need to take are:

1. Create a client that connect to Jenkins
1. Capture all the configured jobs
1. Report the status of the last build for the configured job
1. Calculate the time difference between commit timestamp and job completion.

The changes will be made to `scraper.go`.

{{% tabs %}}
{{% tab title="1. Add Jenkins client" %}}

To be able to connect to the Jenkins server, we will be using the package,
["github.com/yosida95/golang-jenkins"](https://pkg.go.dev/github.com/yosida95/golang-jenkins),
which provides the functionality required to read data from the jenkins server.

Then we are going to utilise some of the helper functions from the,
["go.opentelemetry.io/collector/receiver/scraperhelper"](https://pkg.go.dev/go.opentelemetry.io/collector/receiver/scraperhelper) ,
library to create a start function so that we can connect to the Jenkins server once component has finished starting.

```go
package jenkinscireceiver

import (
    "context"

    jenkins "github.com/yosida95/golang-jenkins"
    "go.opentelemetry.io/collector/component"
    "go.opentelemetry.io/collector/pdata/pmetric"
    "go.opentelemetry.io/collector/receiver"
    "go.opentelemetry.io/collector/receiver/scraperhelper"

    "splunk.conf/workshop/example/jenkinscireceiver/internal/metadata"
)

type scraper struct {
    mb     *metadata.Metricsbuilder
    client *jenkins.Jenkins
}

func newScraper(cfg *Config, set receiver.CreateSettings) (scraperhelper.Scraper, error) {
    s := &scraper{
        mb : metadata.NewMetricsBuilder(cfg.MetricsBuilderConfig, set),
    }
    
    return scraperhelper.NewScraper(
        metadata.Type,
        s.scrape,
        scarperhelper.WithStart(func(ctx context.Context, h component.Host) error {
            client, err := cfg.ToClient(h, set)
            if err != nil {
                return err
            }
            // The collector provides a means of injecting authentication
            // on our behalf, so this will ignore the libraries approach
            // and use the configured http client with authentication.
            s.client = jenkins.NewJenkins(nil, cfg.Endpoint)
            s.client.SetHTTPClient(client)
            return nil
        })
    )
}

func (scraper) scrape(ctx context.Context) (pmetric.Metrics, error) {
    // To be filled in
    return pmetric.NewMetrics(), nil
}

```

This finishes all the setup code that is required in order to initialise a Jenkins receiver.
{{% /tab%}}
{{% tab title="2. Capture all configured jobs" %}}

From this point on, we will be focuses on the `scrape` method that has been waiting to be filled in.
This method will be run on each interval that is configured within the configuration (by default, every minute).

The reason we want to capture the number of jobs configured so we can see the growth of our Jenkins server,
and measure of many projects have onboarded. To do this we will call the jenkins client to list all jobs,
and if it reports an error, return that with no metrics, otherwise, emit the data from the metric builder.

```go
func (s scrape) scrape(ctx context.Context) (pmetric.Metrics, error) {
    jobs, err := s.client.GetJobs()
    if err != nil {
        return pmetric.Metrics{}, err
    }

    // Recording the timestamp to ensure
    // all captured data points within this scrape have the same value. 
    now := pcommon.NewTimestampFromTime(time.Now())
    
    // Casting to an int64 to match the expected type
    s.mb.RecordJenkinsJobsCountDataPoint(now, int64(len(jobs)))
    
    // To be filled in

    return s.mb.Emit(), nil
}
```

{{% /tab%}}
{{% tab title="3. Report the status of each job" %}}

In the last step, we were able to capture all jobs ands report the number of jobs
there was. Within this step, we are going to examine each job and use the report values
to capture metrics.

```go
func (s scrape) scrape(ctx context.Context) (pmetric.Metrics, error) {
    jobs, err := s.client.GetJobs()
    if err != nil {
        return pmetric.Metrics{}, err
    }

    // Recording the timestamp to ensure
    // all captured data points within this scrape have the same value. 
    now := pcommon.NewTimestampFromTime(time.Now())
    
    // Casting to an int64 to match the expected type
    s.mb.RecordJenkinsJobsCountDataPoint(now, int64(len(jobs)))
    
    for _, job := range jobs {
        // Ensure we have valid results to start off with
        var (
            build  = job.LastCompletedBuild
            status = metadata.AttributeJobStatusUnknown
        )

        // This will check the result of the job, however,
        // since the only defined attributes are 
        // `success`, `failure`, and `unknown`. 
        // it is assume that anything did not finish 
        // with a success or failure to be an unknown status.

        switch build.Result {
        case "aborted", "not_built", "unstable":
            status = metadata.AttributeJobStatusUnknown
        case "success":
            status = metadata.AttributeJobStatusSuccess
        case "failure":
            status = metadata.AttributeJobStatusFailed
        }

        s.mb.RecordJenkinsJobDurationDataPoint(
            now,
            int64(job.LastCompletedBuild.Duration),
            job.Name,
            status,
        )
    }

    return s.mb.Emit(), nil
}
```
{{% /tab%}}
{{% tab title="4. Report the delta" %}}

The final step is to calculate how long it took from 
commit to job completion to help infer our DORA metrics.

```go
func (s scrape) scrape(ctx context.Context) (pmetric.Metrics, error) {
    jobs, err := s.client.GetJobs()
    if err != nil {
        return pmetric.Metrics{}, err
    }

    // Recording the timestamp to ensure
    // all captured data points within this scrape have the same value. 
    now := pcommon.NewTimestampFromTime(time.Now())
    
    // Casting to an int64 to match the expected type
    s.mb.RecordJenkinsJobsCountDataPoint(now, int64(len(jobs)))
    
    for _, job := range jobs {
        // Ensure we have valid results to start off with
        var (
            build  = job.LastCompletedBuild
            status = metadata.AttributeJobStatusUnknown
        )

        // Previous step here

        // Ensure that the `ChangeSet` has values
        // set so there is a valid value for us to reference
        if len(build.ChangeSet.Items) == 0 {
            continue
        }

        // Making the assumption that the first changeset
        // item is the most recent change.
        change := build.ChangeSet.Items[0]

        // Record the difference from the build time
        // compared against the change timestamp.
        s.mb.RecordJenkinsJobCommitDeltaDataPoint(
            now,
            int64(build.Timestamp-change.Timestamp),
            job.Name,
            status,
        )
    }

    return s.mb.Emit(), nil
}
```

{{% /tab%}}
{{% /tabs %}}

Once all of these steps have been completed, you now have built a custom Jenkins CI reciever!

## Whats next?

There are more than likely features that would be desired from component that you can think of, like:

- Can I include the branch name that the job used?
- Can I include the project name for the job?
- How I calculate the collective job durations for project?
- How do I validate the changes work?

Please take this time to play around, break it, change things around, or even try to capture logs from the builds.


[^1]: [DORA Metrics](https://cloud.google.com/blog/products/devops-sre/using-the-four-keys-to-measure-your-devops-performance)