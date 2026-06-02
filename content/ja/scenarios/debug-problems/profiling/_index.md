---
title: Profiling Workshop
linkTitle: Profiling Workshop
weight: 3
archetype: chapter
time: 2 minutes
authors: ["Derek Mitchell"]
description: このワークショップでは、Database Query PerformanceとAlwaysOn Profilingを使用して、マイクロサービスの問題をエンジニアがデバッグするのに必要な時間を短縮する方法を紹介します。

---

**Service Maps** と **Traces** は、問題がどのサービスに存在するかを特定する上で非常に有用です。さらに関連するログデータは、そのサービスで問題が発生している理由を詳細に把握するのに役立ちます。

しかし、エンジニアはサービス内で発生している問題をデバッグするために、さらに深く掘り下げる必要がある場合があります。

そこで活用できるのが、Splunkの **AlwaysOn Profiling** や **Database Query Performance** といった機能です。

**AlwaysOn Profiling** はスタックトレースを継続的に収集するため、コード内のどの行がCPUやメモリを最も消費しているかを発見できます。

そして **Database Query Performance** は、実行時間の長いクエリ、最適化されていないクエリ、負荷の重いクエリを素早く特定し、それらが引き起こしている可能性のある問題を軽減します。

このワークショップでは、以下の内容を学びます。

* 複数のパフォーマンス問題を抱えるアプリケーションをデバッグする方法。
* **Database Query Performance** を使用して、アプリケーションのパフォーマンスに影響を与える実行の遅いクエリを見つける方法。
* **AlwaysOn Profiling** を有効化し、CPUとメモリを最も消費しているコードを特定する方法。
* **Splunk Observability Cloud** の調査結果に基づいて修正を適用し、結果を検証する方法。

このワークショップでは、Kubernetes上でホストされている `The Door Game` というJavaベースのアプリケーションを使用します。さっそく始めましょう！
