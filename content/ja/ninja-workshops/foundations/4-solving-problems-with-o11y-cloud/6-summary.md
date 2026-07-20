---
title: まとめ
linkTitle: 6. まとめ
weight: 6
time: 2 minutes
---

このワークショップでは、以下の概念についてハンズオン形式で学びました。

* Helmを使用して **Splunk Distribution of the OpenTelemetry Collector** をデプロイする方法
* [**OpenTelemetry**](https://opentelemetry.io) でアプリケーションを計装する方法
* OpenTelemetry SDKを使用してアプリケーションから関心のあるタグをキャプチャする方法
* **Splunk Observability Cloud** で **Troubleshooting MetricSets** を使用してタグをインデックス化する方法
* **Splunk Observability Cloud** で **Tag Spotlight** と **Dynamic Service Map** 機能を使用して「未知の未知」を発見する方法

このワークショップで共有したベストプラクティスに沿ってタグを収集することで、**Splunk Observability Cloud** に送信するデータからさらに多くの価値を引き出すことができます。このワークショップを完了した今、自分のアプリケーションからタグの収集を開始するために必要な知識を身につけています。

今すぐタグのキャプチャを始めるには、[さまざまなサポート言語でタグを追加する方法](https://docs.splunk.com/observability/en/apm/span-tags/add-context-trace-span.html#instrument-your-application-code-to-add-tags-to-spans)を確認し、次にTag Spotlightで分析できるように[Troubleshooting MetricSetsを作成する方法](https://docs.splunk.com/observability/en/apm/span-tags/index-span-tags.html#apm-index-span-tags)を確認してください。さらにサポートが必要な場合は、[Splunkエキスパートに相談](https://www.splunk.com/en_us/about-splunk/contact-us.html)してください。

他の言語や環境でOpenTelemetryを使用した計装の例については、[Splunk OpenTelemetry Examples GitHubリポジトリ](https://github.com/signalfx/splunk-opentelemetry-examples)をご覧ください。

{{% notice title="ワークショップファシリテーターへのヒント" style="primary"  icon="lightbulb" %}}
ワークショップが完了したら、先ほど `credit.score.category` タグ用に作成したAPM MetricSetを削除することを忘れないでください。
{{% /notice %}}
