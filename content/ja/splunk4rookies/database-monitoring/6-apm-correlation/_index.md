---
title: APM トレースとの関連付け
linkTitle: 6. APM トレースとの関連付け
weight: 6
archetype: chapter
time: 5 minutes
description: 遅いデータベースクエリから、それを呼び出した .NET や Java アプリケーションのトレースに Splunk APM を使用してジャンプします。
---

{{% notice icon="user" style="orange" title="ペルソナ" %}}

あなたは **DBA** ですが、遅いクエリはアプリケーションによって発生しています。開発者は呼び出し箇所の修正を始めるためにトレースが必要です。あなたは彼らに直接リンクを渡したいと考えています。

> [!splunk] アプリケーションが Splunk APM でインストルメントされている場合、Database Monitoring は**データベースクエリを .NET および Java のトレースと関連付ける**ことができます。Database Monitoring のクエリから、それを実行した APM トレースに直接ピボットできます。これにより、アプリケーションチームは SQL ステートメントだけでなく、バックエンドの完全なコンテキストを得ることができます。

{{% /notice %}}

<!-- TODO screenshot: Database Monitoring query view with a "View in APM" / Related Content link visible to a Splunk APM trace -->
![Database と APM の関連付け](images/db-to-apm.png?width=750px)
