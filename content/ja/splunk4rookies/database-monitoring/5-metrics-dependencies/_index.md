---
title: Query Metrics と Dependencies
linkTitle: 5. Query Metrics と Dependencies
weight: 5
archetype: chapter
time: 10 minutes
description: Query Metrics、Dependencies、Metadata タブを使用して、クエリの時系列トレンドとそのクエリを呼び出しているアプリケーションを確認します。
---

{{% notice icon="user" style="orange" title="ペルソナ" %}}

あなたは **DBA** で、調査対象のクエリの目星がついています。アプリケーションチームに変更を依頼する前に、そのクエリが本当に時間の経過とともに遅くなっているのかを確認し、どのアプリケーションとホストがそのクエリを呼び出しているのかを正確に把握したいと考えています。

> [!splunk] **Query metrics**、**Dependencies**、**Metadata** タブがこれらの疑問に答えます。クエリのトレンド、どのクライアントアプリケーションやホストがそのクエリに依存しているか、そしてデータベースエンジンがインスタンス自体について把握している情報を確認できます。

{{% /notice %}}

<!-- TODO screenshot: Query metrics tab showing trend charts for execution count and duration -->
![Query Metrics](images/query-metrics-tab.png?width=750px)
