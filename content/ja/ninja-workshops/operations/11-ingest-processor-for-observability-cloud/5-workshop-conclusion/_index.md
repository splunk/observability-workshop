---
title: Conclusion
linkTitle: 5. Conclusion
weight: 1
---

このワークショップでは、**Splunk Ingest Pipelines** を使用して詳細なログイベントを実用的なメトリクスに変換することで、Kubernetes のログ管理を最適化するプロセス全体を体験しました。まず、Kubernetes 監査ログを効率的にメトリクスに変換するパイプラインを定義し、重要な情報を保持しつつデータ量を大幅に削減しました。その後、生のログイベントを長期保存と詳細分析のために S3 へ安全に保存することを確認しました。

![Kubernetes Audit Event](../images/audit_event.png?width=40vw)

次に、生のイベントから主要なディメンションを追加してこれらのメトリクスを強化し、特定のアクションやリソースをドリルダウンできるようにする方法を示しました。エラーに焦点を当てるためにメトリクスをフィルタリングし、リソースとアクションごとに分割するチャートを作成しました。これにより、問題が発生している箇所をリアルタイムで正確に特定できるようになりました。

![Ingest Pipeline](../images/ingest_pipeline_dimensions.png?width=40vw)

**Splunk Observability Cloud** のリアルタイムアーキテクチャにより、問題が検出された瞬間にこれらのメトリクスでアラートをトリガーできるため、検出までの平均時間 (MTTD) が大幅に短縮されます。さらに、このチャートを新規または既存のダッシュボードに簡単に保存できることも示し、重要なメトリクスを継続的に可視化・監視できるようにしました。

![Audit Dashboard](../images/audit_dashboard.png?width=40vw)

このアプローチの価値は明確です。**Ingest Processor** を使用してログをメトリクスに変換することで、データ処理を効率化しストレージコストを削減できるだけでなく、**Splunk Observability Cloud** を使ってリアルタイムに問題を監視・対応できるようになります。これにより、問題解決の高速化、システム信頼性の向上、リソースのより効率的な利用が実現されます。同時に、コンプライアンスや詳細分析のために元のログを保持しアクセスできる状態も維持できます。

<center><h1>Happy Splunking!</h1></center>

![Dancing Buttercup](../images/Splunk-dancing-buttercup-GIF-103.gif?width=30vw)
