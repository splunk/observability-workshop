---
title: 主なポイント
linkTitle: 1. 主なポイント
weight: 1
---

ワークショップでは、Splunk Observability CloudとOpenTelemetryシグナル（**メトリクス**、**トレース**、**ログ**）の組み合わせが、平均検出時間（**MTTD**）を短縮し、平均解決時間（**MTTR**）も短縮するのにどれほど役立つかを見てきました。

* メインユーザーインターフェースとそのコンポーネント、*ランディング、インフラストラクチャ、APM、RUM、Synthetics、ダッシュボード*ページ、および*設定*ページの理解を深めました。
* 時間の許す限り、*インフラストラクチャ*の演習を行い、Kubernetesナビゲーターで使用される*メトリクス*を見て、Kubernetesクラスターで見つかった関連するサービスを確認しました：

![Kubernetes](../images/infra.png)

* ユーザーが経験していることを理解し、RUMおよびAPMを使用して特に長いページの読み込みをトラブルシュートし、そのトレースをフロントエンドからバックエンドまで追跡し、ログエントリまで確認しました。
  RUM *セッションリプレイ*およびAPM *Dependency map*とBreakdownなどのツールを使用して、問題の原因を発見しました：

![rum and apm](../images/rum-apm.png)

* RUMおよびAPMの両方で*Tag Spotlight*を使用して、パフォーマンスの問題とエラーのためのトレンドとコンテキストを理解しました。 APM *Trace waterfall*の*Span*を掘り下げて、サービスがどのように相互作用し、エラーを見つけました：

![tag and waterfall](../images/tag-spotlight-waterfall.png)

* *Related content*機能を使用して、*Trace*と直接関連する*Logs*へのリンクを辿り、フィルターを使用して問題の正確な原因まで掘り下げました。

![logs](../images/log.png)

* 次に、Syntheticsを見て、ウェブおよびモバイルトラフィックをシミュレートでき、RUM / APMおよびログオブザーバーからの結果を確認し、実行時間がSLAを超えた場合に警告を受けるように*Detector*を作成しました。

* 最後の演習では、開発者とSREがTVスクリーンで実行中のダッシュボードを作成しました：

![synth and TV](../images/synth-tv.png)
