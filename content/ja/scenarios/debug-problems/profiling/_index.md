---
title: Profiling Workshop
linkTitle: Profiling Workshop
weight: 3
archetype: chapter
time: 2 minutes
authors: ["Derek Mitchell"]
description: このワークショップでは、Database Query Performance と AlwaysOn Profiling を使用して、エンジニアがマイクロサービスの問題をデバッグするために必要な時間を短縮する方法を紹介します。

---

**Service Maps** と **Traces** は、問題がどのサービスに存在するかを特定する上で非常に有用です。また、関連するログデータは、そのサービスで問題が発生している理由について詳細な情報を提供します。

しかし、エンジニアは自分のサービスで発生している問題をデバッグするために、さらに深く掘り下げる必要がある場合があります。

ここで、Splunk の **AlwaysOn Profiling** や **Database Query Performance** などの機能が役立ちます。

**AlwaysOn Profiling** はスタックトレースを継続的に収集し、コードのどの行が最も多くの CPU とメモリを消費しているかを発見できるようにします。

また、**Database Query Performance** は、長時間実行されている、最適化されていない、または負荷の高いクエリを素早く特定し、それらが引き起こしている可能性のある問題を軽減できます。

このワークショップでは、以下の内容を学びます:

* パフォーマンスの問題が複数あるアプリケーションをデバッグする方法。
* **Database Query Performance** を使用して、アプリケーションのパフォーマンスに影響を与える低速なクエリを見つける方法。
* **AlwaysOn Profiling** を有効にし、最も多くの CPU とメモリを消費しているコードを見つける方法。
* **Splunk Observability Cloud** からの調査結果に基づいて修正を適用し、結果を検証する方法。

このワークショップでは、Kubernetes でホストされている `The Door Game` という Java ベースのアプリケーションを使用します。それでは始めましょう！
