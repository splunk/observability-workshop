---
title: OpenTelemetry Collector Development
linkTitle: 8.5 Building Business Logic 
weight: 13
---

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
    mb     *metadata.MetricsBuilder
    client *jenkins.Jenkins
}

func newScraper(cfg *Config, set receiver.CreateSettings) (scraperhelper.Scraper, error) {
    s := &scraper{
        mb : metadata.NewMetricsBuilder(cfg.MetricsBuilderConfig, set),
    }
    
    return scraperhelper.NewScraper(
        metadata.Type,
        s.scrape,
        scraperhelper.WithStart(func(ctx context.Context, h component.Host) error {
            client, err := cfg.ToClient(h, set.TelemetrySettings)
            if err != nil {
                return err
            }
            // The collector provides a means of injecting authentication
            // on our behalf, so this will ignore the libraries approach
            // and use the configured http client with authentication.
            s.client = jenkins.NewJenkins(nil, cfg.Endpoint)
            s.client.SetHTTPClient(client)
            return nil
        }),
    )
}

func (s scraper) scrape(ctx context.Context) (pmetric.Metrics, error) {
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
func (s scraper) scrape(ctx context.Context) (pmetric.Metrics, error) {
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
func (s scraper) scrape(ctx context.Context) (pmetric.Metrics, error) {
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

Once all of these steps have been completed, you now have built a custom Jenkins CI receiver!

## Whats next?

There are more than likely features that would be desired from component that you can think of, like:

- Can I include the branch name that the job used?
- Can I include the project name for the job?
- How I calculate the collective job durations for project?
- How do I validate the changes work?

Please take this time to play around, break it, change things around, or even try to capture logs from the builds.


[^1]: [DORA Metrics](https://cloud.google.com/blog/products/devops-sre/using-the-four-keys-to-measure-your-devops-performance)
