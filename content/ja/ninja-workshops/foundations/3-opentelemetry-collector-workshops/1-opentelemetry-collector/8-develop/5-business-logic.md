---
title: OpenTelemetry Collector Development
linkTitle: 8.5 Building Business Logic 
weight: 13
---

## ビジネスロジックの構築

現時点では、まだ何も処理を行わないカスタムコンポーネントがあるだけなので、Jenkins からデータを取得するために必要なロジックを追加する必要があります。

ここから先に行う手順は次のとおりです。

1. Jenkins に接続するクライアントを作成する
1. 設定されているすべてのジョブを取得する
1. 設定されたジョブの直近のビルドのステータスをレポートする
1. コミットのタイムスタンプとジョブ完了時刻の差を計算する

変更は `scraper.go` に対して行います。

{{% tabs %}}
{{% tab title="1. Add Jenkins client" %}}

Jenkins サーバーに接続するために、Jenkins サーバーからデータを読み取るのに必要な機能を提供するパッケージ ["github.com/yosida95/golang-jenkins"](https://pkg.go.dev/github.com/yosida95/golang-jenkins) を使用します。

さらに、["go.opentelemetry.io/collector/receiver/scraperhelper"](https://pkg.go.dev/go.opentelemetry.io/collector/receiver/scraperhelper) ライブラリのヘルパー関数を活用して、コンポーネントの起動が完了した時点で Jenkins サーバーに接続できるよう、start 関数を作成します。

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

これで Jenkins receiver の初期化に必要なセットアップコードはすべて完了です。
{{% /tab%}}
{{% tab title="2. Capture all configured jobs" %}}

ここからは、これまで未実装のままになっていた `scrape` メソッドに焦点を当てていきます。このメソッドは、設定で指定された間隔（デフォルトでは1分ごと）で実行されます。

設定済みのジョブ数を取得したい理由は、Jenkins サーバーの成長を可視化し、どれだけのプロジェクトがオンボーディングされたかを測定するためです。これを実現するために、jenkins クライアントを呼び出してすべてのジョブを一覧表示します。エラーが返された場合はメトリクスを返さずにそのエラーを返し、それ以外の場合は metric builder からデータを発行します。

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
    
    // To be filled in

    return s.mb.Emit(), nil
}
```

{{% /tab%}}
{{% tab title="3. Report the status of each job" %}}

前のステップでは、すべてのジョブを取得して、その個数をレポートできるようにしました。このステップでは、各ジョブを調査し、レポートされた値からメトリクスを取得します。

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

最後のステップでは、コミットからジョブ完了までにかかった時間を計算し、DORA メトリクスを推定するのに役立てます。

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

これらの手順をすべて完了すると、カスタムの Jenkins CI receiver の構築が完了です！

## 次は何でしょうか？

このコンポーネントに対して、他にも欲しい機能が思い浮かぶかもしれません。たとえば次のようなものです。

- ジョブで使用されたブランチ名を含めることはできますか？
- ジョブのプロジェクト名を含めることはできますか？
- プロジェクト全体のジョブ実行時間を合計するにはどうすればよいでしょうか？
- 変更が動作することをどのように検証すればよいでしょうか？

ぜひこの時間を使って、いろいろ試したり、あえて壊してみたり、設定を変更してみたり、さらにはビルドからログを取得することにも挑戦してみてください。
