---
title: まとめ
linkTitle: 6. まとめ
weight: 6
time: 2 minutes
---

このワークショップでは、以下の概念についてハンズオン形式で学びました：

* Helm を使用して **Splunk Distribution of the OpenTelemetry Collector** をデプロイする方法
* [**OpenTelemetry**](https://opentelemetry.io) でアプリケーションを計装する方法
* OpenTelemetry SDK を使用してアプリケーションから関心のあるタグをキャプチャする方法
* **Troubleshooting MetricSets** を使用して **Splunk Observability Cloud** でタグをインデックスする方法
* **Tag Spotlight** と **Dynamic Service Map** 機能を使用して **Splunk Observability Cloud** でタグを活用し、「未知の未知」を発見する方法

このワークショップで共有したベストプラクティスに沿ってタグを収集することで、**Splunk Observability Cloud** に送信するデータからさらに多くの価値を得ることができます。このワークショップを完了した今、自分のアプリケーションからタグの収集を開始するために必要な知識を身につけました！

今日からタグのキャプチャを始めるには、[サポートされている各言語でタグを追加する方法](https://docs.splunk.com/observability/en/apm/span-tags/add-context-trace-span.html#instrument-your-application-code-to-add-tags-to-spans)を確認し、次に Tag Spotlight で分析できるように [Troubleshooting MetricSets を作成する方法](https://docs.splunk.com/observability/en/apm/span-tags/index-span-tags.html#apm-index-span-tags)を確認してください。さらにヘルプが必要な場合は、[Splunk エキスパートに問い合わせ](https://www.splunk.com/en_us/about-splunk/contact-us.html)てください。

また、他の言語や環境が OpenTelemetry でどのように計装されているかを確認するには、
[Splunk OpenTelemetry Examples GitHub リポジトリ](https://github.com/signalfx/splunk-opentelemetry-examples)を参照してください。

{{% notice title="Tip for Workshop Facilitator(s)" style="primary"  icon="lightbulb" %}}
ワークショップが完了したら、以前に `credit.score.category` タグ用に作成した APM MetricSet を削除することを忘れないでください。
{{% /notice %}}
