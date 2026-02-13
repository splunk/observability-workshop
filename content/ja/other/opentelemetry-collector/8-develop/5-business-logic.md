---
title: OpenTelemetry Collector を開発する
linkTitle: 8.5 ビジネスロジックを作る
weight: 13
---

## ビジネスロジックを作る

この時点では、何も行っていないカスタムコンポーネントが作成されています。ここから、Jenkinsからデータを取得するための必要なロジックを追加していきましょう。

ここからのステップは以下の通りです：

1. Jenkinsに接続するクライアントを作成する
1. 設定されたすべてのジョブをキャプチャする
1. 設定されたジョブの最後のビルドのステータスを報告する
1. コミットタイムスタンプとジョブ完了の時間差を計算する

変更を `scraper.go` に加えていきます。

{{% tabs %}}
{{% tab title="1. Jenkinsクライアントを追加する" %}}

Jenkinsサーバーに接続するために、パッケージ ["github.com/yosida95/golang-jenkins"](https://pkg.go.dev/github.com/yosida95/golang-jenkins) を使用します。これには、Jenkinsサーバーからデータを読み取るために必要な機能が提供されています。

次に、["go.opentelemetry.io/collector/receiver/scraperhelper"](https://pkg.go.dev/go.opentelemetry.io/collector/receiver/scraperhelper) ライブラリのいくつかのヘルパー関数を利用して、コンポーネントの起動が完了したらJenkinsサーバーに接続できるようにするスタート関数を作成します。

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
これで、Jenkinsレシーバーを初期化するために必要なすべてのコードが完成しました。

{{% /tab%}}
{{% tab title="2. ジョブをキャプチャする" %}}

ここから先は、実装が必要な `scrape` メソッドに焦点を当てます。このメソッドは、設定された間隔（デフォルトでは1分）ごとに実行されます。

Jenkinsサーバーの負荷状況や、どの程度のプロジェクトが実行されているかを測定するために、Jenkinsで設定されているジョブの数をキャプチャしたいと考えています。これを行うために、Jenkinsクライアントを呼び出してすべてのジョブをリスト化し、エラーが報告された場合はメトリクスなしでそれを返し、そうでなければメトリクスビルダーからのデータを発行します。

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
{{% tab title="3. ジョブの状態を報告する" %}}

前のステップにより、すべてのジョブをキャプチャしてジョブの数をレポートできるようになりました。
このステップでは、それぞれのジョブを調査し、レポートされた値を使用してメトリクスをキャプチャしていきます。

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
{{% tab title="4. 差分を報告する" %}}

最後のステップでは、コミットからジョブ完了までにかかった時間を計算して、[DORA メトリクス](https://cloud.google.com/blog/products/devops-sre/using-the-four-keys-to-measure-your-devops-performance) を推測するのに役立てていきます。

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

これらのステップがすべて完了すると、Jenkins CIレシーバーが完成します！

## 次は何をするの？

コンポーネントに必要な機能は、おそらく他にもたくさん思いつくでしょう。例えば：

- ジョブで使用されたブランチ名を含めることはできますか？
- ジョブのプロジェクト名を含めることはできますか？
- プロジェクトのジョブの総持続時間をどのように計算しますか？
- 変更が機能するかどうかをどのように検証しますか？

この時間を使って遊んでみたり、壊してみたり、変更してみたり、ビルドからのログをキャプチャしてみるなどしてください。
