---
title: Splunk Observability Cloud で Cisco AI Pods を監視する
linkTitle: Splunk Observability Cloud で Cisco AI Pods を監視する
weight: 14
archetype: chapter
time: 60 minutes
authors: ["Derek Mitchell"]
description: Red Hat OpenShift 上に OpenTelemetry Collector をデプロイし、Prometheus 経由で Cisco AI Pod のメトリクスをスクレイピングしながら、LLM を呼び出す Python サービスをトレースします。
draft: false
hidden: false
aliases:
  - /ninja-workshops/14-cisco-ai-pods/
---

**Cisco の AI-ready POD** は、ハードウェアとソフトウェアの優れた技術を組み合わせ、多様なニーズに対応する堅牢でスケーラブルかつ効率的な AI 対応インフラを実現します。

**Splunk Observability Cloud** は、こうしたインフラ全体に加え、このスタック上で稼働するすべてのアプリケーションコンポーネントに対する包括的な可視化を提供します。

Cisco AI POD 環境向けに Splunk Observability Cloud を構成する手順は [完全なドキュメント](https://github.com/signalfx/splunk-opentelemetry-examples/tree/main/collector/cisco-ai-ready-pods) として公開されています。

ただし、インストール手順を実際に試すために Cisco AI POD 環境へアクセスできるとは限りません。

このワークショップでは、実際の Cisco AI POD へのアクセスを必要とせずに、Splunk Observability Cloud で Cisco AI POD を監視する際に使用される複数の技術をデプロイし、操作するハンズオン体験を提供します。具体的には次の内容を扱います。

* Red Hat OpenShift クラスタへの **OpenTelemetry Collector** のデプロイを実践します。
* Collector に **Prometheus** レシーバーを追加し、インフラメトリクスを取り込む方法を実践します。
* **Weaviate** ベクターデータベースをクラスタにデプロイする方法を実践します。
* 大規模言語モデル (LLM) と連携する Python サービスを **OpenTelemetry** で計装する方法を実践します。
* LLM と連携するアプリケーションのトレースから、OpenTelemetry がどのような詳細情報を取得するかを理解します。

> 注: ワークショップのセットアップセクションは、ワークショップ主催者のみが実行する必要があります。
