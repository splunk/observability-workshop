---
title: OpenTelemetry Collector Development
linkTitle: 8.5 ビジネスロジックの構築
weight: 13
---

## ビジネスロジックの構築

この時点では、カスタムコンポーネントは何も行わない状態です。Jenkinsからデータを取得するために必要なロジックを追加する必要があります。

ここから実施する手順は以下の通りです。

1. Jenkinsに接続するクライアントを作成する
1. 設定されたすべてのジョブを取得する
1. 設定されたジョブの最後のビルドのステータスを報告する
1. コミットのタイムスタンプとジョブ完了の時間差を計算する

変更は `scraper.go` に対して行います。

{{% tabs %}}
{{% tab title="1. Jenkinsクライアントの追加" %}}

Jenkinsサーバーに接続するために、パッケージ
["github.com/yosida95/golang-jenkins"](https://pkg.go.dev/github.com/yosida95/golang-jenkins)
を使用します。このパッケージはJenkinsサーバーからデータを読み取るために必要な機能を提供します。

次に、
["go.opentelemetry.io/collector/receiver/scraperhelper"](https://pkg.go.dev/go.opentelemetry.io/collector/receiver/scraperhelper)
ライブラリのヘルパー関数を利用して、コンポーネントの起動完了後にJenkinsサーバーへ接続するためのstart関数を作成します。

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

これでJenkins Receiverを初期化するために必要なセットアップコードはすべて完了です。
{{% /tab%}}
{{% tab title="2. 設定済みジョブの取得" %}}

ここからは、まだ中身が空の `scrape` メソッドに注目します。
このメソッドは設定で指定された間隔（デフォルトでは毎分）ごとに実行されます。

設定されたジョブ数を取得する理由は、Jenkinsサーバーの成長を確認し、どれだけのプロジェクトがオンボードしたかを測定するためです。これを実現するために、Jenkinsクライアントを呼び出してすべてのジョブを一覧取得し、エラーが報告された場合はメトリクスなしでエラーを返し、そうでなければmetric builderからデータを出力します。

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
{{% tab title="3. 各ジョブのステータス報告" %}}

前のステップでは、すべてのジョブを取得してジョブ数を報告しました。このステップでは、各ジョブを調べてレポートされた値を使用してメトリクスを取得します。

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
{{% tab title="4. 差分の報告" %}}

最後のステップでは、コミットからジョブ完了までにかかった時間を計算し、DORAメトリクスを推測できるようにします。

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

これらのステップがすべて完了すると、カスタムJenkins CI Receiverの構築が完了です。

## 次のステップ

コンポーネントに追加したい機能がまだあるかもしれません。例えば以下のようなものです。

- ジョブが使用したブランチ名を含めることはできるか？
- ジョブのプロジェクト名を含めることはできるか？
- プロジェクトの累積ジョブ実行時間を計算するには？
- 変更が正しく動作することをどのように検証するか？

この時間を使って、自由に試してみてください。壊したり、変更を加えたり、ビルドからログを取得してみたりしましょう。
