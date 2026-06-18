---
title: まとめ
linkTitle: 6. まとめ
weight: 6
time: 2 minutes
---

このワークショップでは、以下の概念についてハンズオン体験を行いました

* Helm を使用して **Splunk Distribution of the OpenTelemetry Collector** をデプロイする方法。
* [**OpenTelemetry**](https://opentelemetry.io) でアプリケーションを計装する方法。
* OpenTelemetry SDK を使用してアプリケーションから関心のあるタグをキャプチャする方法。
* **Troubleshooting MetricSets** を使用して **Splunk Observability Cloud** でタグをインデックス化する方法。
* **Tag Spotlight** と **Dynamic Service Map** 機能を使用して、**Splunk Observability Cloud** でタグを活用し「未知の未知」を発見する方法。

このワークショップで共有したベストプラクティスに沿ってタグを収集することで、**Splunk Observability Cloud** に送信しているデータからさらに多くの価値を引き出すことができます。このワークショップを完了した今、ご自身のアプリケーションからタグの収集を開始するために必要な知識を身につけました！

今日からタグのキャプチャを始めるには、[サポートされている各言語でタグを追加する方法](https://docs.splunk.com/observability/en/apm/span-tags/add-context-trace-span.html#instrument-your-application-code-to-add-tags-to-spans)を確認し、次に [Troubleshooting MetricSets を作成してタグを使用する方法](https://docs.splunk.com/observability/en/apm/span-tags/index-span-tags.html#apm-index-span-tags)を参照して、Tag Spotlight で分析できるようにしてください。さらにサポートが必要な場合は、お気軽に [Splunk エキスパートにお問い合わせ](https://www.splunk.com/en_us/about-splunk/contact-us.html)ください。

また、他の言語や環境が OpenTelemetry でどのように計装されているかについては、[Splunk OpenTelemetry Examples GitHub リポジトリ](https://github.com/signalfx/splunk-opentelemetry-examples)をご覧ください。

{{% notice title="ワークショップファシリテーターへのヒント" style="primary"  icon="lightbulb" %}}
ワークショップが完了したら、`credit.score.category` タグ用に先ほど作成した APM MetricSet を削除することを忘れないでください。
{{% /notice %}}
