---
title: まとめ
linkTitle: 5. まとめ
weight: 1
---

このワークショップでは、**Splunk Ingest Pipelines** を使用して詳細なログイベントを実用的なメトリクスに変換することで、Kubernetesログ管理を最適化するプロセス全体を学びました。まず、Kubernetes監査ログを効率的にメトリクスに変換するパイプラインを定義し、重要な情報を保持しながらデータ量を大幅に削減しました。次に、生のログイベントを長期保存とより深い分析のためにS3に安全に保存することを確認しました。

![Kubernetes Audit Event](../images/audit_event.png?width=40vw)

続いて、生のイベントから主要なディメンションを追加してメトリクスを強化し、特定のアクションやリソースにドリルダウンできるようにする方法を示しました。エラーに焦点を当てたメトリクスをフィルタリングし、リソースとアクションごとに分類するチャートを作成しました。これにより、リアルタイムで問題が発生している箇所を正確に特定できるようになりました。

![Ingest Pipeline](../images/ingest_pipeline_dimensions.png?width=40vw)

**Splunk Observability Cloud** のリアルタイムアーキテクチャにより、問題が検出された瞬間にこれらのメトリクスがアラートをトリガーでき、平均検出時間（MTTD）を大幅に短縮します。さらに、このチャートを新規または既存のダッシュボードに簡単に保存でき、重要なメトリクスの継続的な可視性とモニタリングを確保できることを示しました。

![Audit Dashboard](../images/audit_dashboard.png?width=40vw)

このアプローチの価値は明確です。**Ingest Processor** を使用してログをメトリクスに変換することで、データ処理の効率化とストレージコストの削減だけでなく、**Splunk Observability Cloud** を使用したリアルタイムでの問題のモニタリングと対応が可能になります。これにより、問題解決の迅速化、システム信頼性の向上、リソース利用の効率化が実現され、同時にコンプライアンスやより深い分析のために元のログを保持・アクセスする能力も維持されます。

<center><h1>Happy Splunking!</h1></center>

![Dancing Buttercup](../images/Splunk-dancing-buttercup-GIF-103.gif?width=30vw)
