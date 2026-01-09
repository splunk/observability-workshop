---
title: OpenTelemetry Collector 開発
linkTitle: 8.5 Building Business Logic
weight: 13
---

## ビジネスロジックの構築

この時点で、現在何もしないカスタムコンポーネントがあるため、Jenkins からこのデータをキャプチャするために必要なロジックを追加する必要があります。

ここから、実行する必要があるステップは以下の通りです：

1. Jenkins に接続するクライアントを作成する
1. 設定されたすべてのジョブをキャプチャする
1. 設定されたジョブの最後のビルドのステータスを報告する
1. コミットのタイムスタンプとジョブ完了の時間差を計算する

変更は `scraper.go` に対して行われます。

{{% tabs %}}
{{% tab title="1. Add Jenkins client" %}}

Jenkins サーバーに接続できるようにするために、["github.com/yosida95/golang-jenkins"](https://pkg.go.dev/github.com/yosida95/golang-jenkins) パッケージを使用します。このパッケージは、Jenkins サーバーからデータを読み取るために必要な機能を提供します。

次に、["go.opentelemetry.io/collector/receiver/scraperhelper"](https://pkg.go.dev/go.opentelemetry.io/collector/receiver/scraperhelper) ライブラリのヘルパー関数を利用して、コンポーネントの起動が完了した後に Jenkins サーバーに接続できるように start 関数を作成します。

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

これで Jenkins レシーバーを初期化するために必要なすべてのセットアップコードが完了しました。
{{% /tab%}}
{{% tab title="2. Capture all configured jobs" %}}

ここからは、入力を待っていた `scrape` メソッドに焦点を当てます。このメソッドは、設定で構成された間隔（デフォルトでは毎分）で実行されます。

設定されたジョブの数をキャプチャしたい理由は、Jenkins サーバーの成長を確認し、オンボードしたプロジェクトの数を測定できるようにするためです。これを行うために、Jenkins クライアントを呼び出してすべてのジョブをリストし、エラーが報告された場合はメトリクスなしでそれを返し、そうでなければメトリクスビルダーからデータを出力します。

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

前のステップでは、すべてのジョブをキャプチャし、ジョブの数を報告することができました。このステップでは、各ジョブを調べ、報告された値を使用してメトリクスをキャプチャします。

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

最後のステップは、コミットからジョブ完了までにかかった時間を計算し、DORA メトリクスを推測するのに役立てることです。

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

これらのステップがすべて完了すると、カスタム Jenkins CI レシーバーの構築が完了です！

## 次のステップ

コンポーネントから欲しい機能がおそらくもっとあるでしょう。例えば：

- ジョブが使用したブランチ名を含めることはできますか？
- ジョブのプロジェクト名を含めることはできますか？
- プロジェクトの累積ジョブ期間をどのように計算しますか？
- 変更が機能することをどのように検証しますか？

この時間を使って、遊んでみたり、壊してみたり、変更したり、ビルドからログをキャプチャしてみたりしてください。

[^1]: [DORA Metrics](https://cloud.google.com/blog/products/devops-sre/using-the-four-keys-to-measure-your-devops-performance)
