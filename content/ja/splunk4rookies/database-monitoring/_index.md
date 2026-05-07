---
title: Database Monitoring
weight: 4
authors: ["Robert Castley"]
time: 60 minutes
description: Splunk Database Monitoring を実際に操作して、遅いクエリを調査し、実行プランを確認し、データベースのパフォーマンスをそれに依存するアプリケーションと相関させる方法を学びます。
params:
  images:
    - images/featured-dbm.png
hidden: true
---

## はじめに

データベースはほぼすべてのアプリケーションの中心に位置しており、データベースが遅くなるとそれに依存するすべてのものが遅くなります。**Splunk Database Monitoring** は、Microsoft SQL Server、Oracle Database、PostgreSQL を横断する統一ビューを提供し、問題を引き起こしているクエリ、インスタンス、アプリケーションを特定できるようにします。

このハンズオンセッションでは、パフォーマンスに関する苦情に対応するデータベース管理者（DBA）の役割を演じます。本番環境で使用するのと同じ画面を通じて作業を進めます。インスタンスのランク付け、最も遅いクエリへのドリルダウン、クエリサンプルと実行プランの確認、そしてそれらのクエリを呼び出しているアプリケーションへの関連付けまで行います。

## ワークショップの概要

この1時間のハンズオンセッションでは、以下を扱います。

- **Database Monitoring Overview** - Database Monitoring とは何か、どのプラットフォームがサポートされているか、Splunk Observability Cloud のどこで利用できるかを学びます
- **Database Instances** - Overview ダッシュボードを使用して、実行回数、実行時間、CPU 時間でインスタンスをランク付けします
- **Queries と Query Samples** - インスタンス上で最も遅いクエリを特定し、クエリサンプルと実行プランを確認します
- **Query Metrics と Dependencies** - クエリごとのパフォーマンスメトリクスを確認し、各クエリにどのアプリケーションが依存しているかを把握します
- **APM トレースとの相関** - 遅いデータベースクエリから、それをトリガーした .NET または Java アプリケーションのトレースへ移動します

<!-- TODO screenshot: featured/hero image for the workshop, e.g., a Database Monitoring overview dashboard showing instance ranking and query duration trends -->
![Database Monitoring](images/featured-dbm.png)

**それでは、データベースに踏み込んでいきましょう。**
