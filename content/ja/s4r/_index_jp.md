---
title: Splunk4Rookies - Observability Cloud
weight: 1
---

{{% badge icon="clock" style="primary" %}}2分{{% /badge %}} {{% badge style="blue" title="著者" %}}Robert Castley & Pieter Hagen{{% /badge %}}

このワークショップでは、**Splunk Observability Cloud**がユーザーエクスペリエンスの即時の可視化を提供する方法を紹介します。これは、フロントエンドアプリケーションからバックエンドサービスまでの視点からのものであり、**Splunk Observability Cloud**の最も魅力的な製品機能と差別化要因のいくつかを体験できます。

* インフラモニタリング
* **完全な忠実度**のリアルユーザーモニタリング（RUM）
* アプリケーションパフォーマンスモニタリング（APM）との**エンドツーエンドのNoSample™完全な忠実度**のトレースの可視性
* **コードなし**のログクエリ
* シンセティックモニタリング
* タグ分析とエラースタックを使用したルート原因の特定
* 関連するコンテンツ

Splunk Observability Cloudを構築する際の重要な要素は、テレメトリデータを統一してエンドユーザーエクスペリエンスとアプリケーションスタックの完全なイメージを作成することです。

このワークショップでは、AWS EC2インスタンスに展開されたマイクロサービスベースのアプリケーションを使用します。このアプリケーションは、ユーザーが製品を閲覧し、カートに追加し、チェックアウトすることができるシンプルなeコマースアプリケーションです。このアプリケーションはOpenTelemetryで計装されています。

---

**[OpenTelemetry](https://opentelemetry.io)**は、テレメトリデータ（メトリクス、トレース、およびログ）を計装し、生成し、収集し、エクスポートするためのツール、API、およびソフトウェア開発キット（SDK）のコレクションです。これにより、ソフトウェアのパフォーマンスと動作を分析できます。

OpenTelemetryコミュニティは拡大しています。Splunk、Google、Microsoft、Amazonなど多くの組織が協力したプロジェクトで、現在、Kubernetesの次に多くの貢献者を有するプロジェクトとなっています。

![Full Stack](images/splunk-full-stack.png)
