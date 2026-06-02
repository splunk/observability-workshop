---
title: Summary
linkTitle: 6. まとめ
weight: 6
time: 2 minutes
---

このワークショップでは、以下の概念をハンズオンで体験しました。

* Helm を使用した **Splunk Distribution of the OpenTelemetry Collector** のデプロイ方法。
* [**OpenTelemetry**](https://opentelemetry.io) を使用したアプリケーションのインストルメンテーション方法。
* OpenTelemetry SDK を使用して、アプリケーションから関心のあるタグを取得する方法。
* **Troubleshooting MetricSets** を使用して、**Splunk Observability Cloud** でタグをインデックスする方法。
* **Tag Spotlight** および **Dynamic Service Map** 機能を使用して、**Splunk Observability Cloud** でタグを活用し「unknown unknowns（未知の未知）」を発見する方法。

このワークショップで紹介したベストプラクティスに沿ってタグを収集することで、**Splunk Observability Cloud** に送信するデータからさらに大きな価値を引き出すことができます。このワークショップを完了した今、ご自身のアプリケーションからタグを収集し始めるために必要な知識を身につけました！

今すぐタグの取得を始めるには、[サポートされている各種言語でタグを追加する方法](https://docs.splunk.com/observability/en/apm/span-tags/add-context-trace-span.html#instrument-your-application-code-to-add-tags-to-spans)を参照し、続いて [Tag Spotlight で分析できるよう Troubleshooting MetricSets を作成する方法](https://docs.splunk.com/observability/en/apm/span-tags/index-span-tags.html#apm-index-span-tags) を確認してください。さらにサポートが必要な場合は、お気軽に [Splunk のエキスパートにお問い合わせください](https://www.splunk.com/en_us/about-splunk/contact-us.html)。

また、他の言語や環境で OpenTelemetry がどのようにインストルメントされているかを確認するには、
[Splunk OpenTelemetry Examples GitHub リポジトリ](https://github.com/signalfx/splunk-opentelemetry-examples) をご覧ください。

{{% notice title="ワークショップ運営者へのヒント" style="primary"  icon="lightbulb" %}}
ワークショップが完了したら、先ほど `credit.score.category` タグ用に作成した APM MetricSet を忘れずに削除してください。
{{% /notice %}}
