---
title: Database Instances
linkTitle: 3. Database Instances
weight: 3
archetype: chapter
time: 15 minutes
description: Database Monitoring の Overview ダッシュボードを使用してインスタンスをランク付けし、最も問題のあるインスタンスを選択します。
---

{{% notice icon="user" style="orange" title="ペルソナ" %}}

あなたは引き続き **DBA** として、データベースが遅いという苦情のトリアージを行っています。SQL Server、Oracle、PostgreSQL にまたがる多数のデータベースインスタンスを管理しています。さらに深く調査する前に、問題の原因である可能性が最も高い1つ（または2つ）のインスタンスを見つける必要があります。

> [!splunk] **Database Monitoring Overview** ページは、監視対象のすべてのデータベースインスタンスを *execution count*、*total duration*、または *total CPU time* でランク付けします。これを利用して、最も忙しく、最も遅いインスタンスを特定し、**Navigator** ビューに移動して本格的な調査を開始します。

{{% /notice %}}

<!-- TODO screenshot: Database Monitoring overview page with multiple instances listed -->
![Database Instances](images/db-instances-overview.png?width=750px)
