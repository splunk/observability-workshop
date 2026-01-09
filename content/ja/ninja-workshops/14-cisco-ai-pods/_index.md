---
title: Splunk Observability Cloudで Cisco AI Podsを監視する
linkTitle: Splunk Observability CloudでCisco AI Podsを監視する
weight: 14
archetype: chapter
time: 2 minutes
authors: ["Derek Mitchell"]
description: このハンズオンワークショップでは、Splunk Observability CloudでCisco AI Podsを監視する方法を学びます。Red Hat OpenShiftにOpenTelemetry Collectorをデプロイし、Prometheusレシーバーを使用してインフラストラクチャメトリクスを取り込み、Large Language Models (LLMs)と連携するPythonサービスを監視するためのAPMを設定する方法を習得できます。
draft: false
hidden: false
---

**Cisco AI-ready PODs** は、ハードウェアとソフトウェア技術の最良の組み合わせにより、堅牢でスケーラブル、かつ効率的なAI対応インフラストラクチャを提供し、多様なニーズに対応します。

**Splunk Observability Cloud** は、このインフラストラクチャ全体と、このスタック上で実行されているすべてのアプリケーションコンポーネントに対する包括的な可視性を提供します。

Cisco AI POD環境向けにSplunk Observability Cloudを設定する手順は完全にドキュメント化されています（詳細は[こちら](https://github.com/signalfx/splunk-opentelemetry-examples/tree/main/collector/cisco-ai-ready-pods)を参照してください）。

しかし、インストール手順を練習するためにCisco AI POD環境にアクセスできるとは限りません。

このワークショップでは、実際のCisco AI PODへのアクセスを必要とせずに、Splunk Observability CloudでCisco AI PODsを監視するために使用されるいくつかの技術をデプロイして操作するハンズオン体験を提供します。具体的には以下の内容が含まれます：

* GPUベースのワーカーノードを持つ **RedHat OpenShift** クラスターのデプロイを練習します。
* **NVIDIA NIM Operator** と **NVIDIA GPU Operator** のデプロイを練習します。
* NVIDIA NIMを使用して **Large Language Models (LLMs)** をクラスターにデプロイする練習をします。
* Red Hat OpenShiftクラスターに **OpenTelemetry Collector** をデプロイする練習をします。
* インフラストラクチャメトリクスを取り込むためにコレクターに **Prometheus** レシーバーを追加する練習をします。
* **Weaviate** ベクトルデータベースをクラスターにデプロイする練習をします。
* Large Language Models (LLMs)と連携するPythonサービスを **OpenTelemetry** で計装する練習をします。
* LLMと連携するアプリケーションからOpenTelemetryがトレースでキャプチャする詳細を理解します。

> 注意: Red Hat OpenShiftとNVIDIA AI Enterpriseコンポーネントは、通常、実際のAI PODにプリインストールされています。ただし、このワークショップではAWSを使用するため、これらのセットアップ手順を手動で実行する必要があります。

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}
このワークショップを最も簡単にナビゲートするには、以下を使用してください：

* このページの右上にある左右の矢印 (**<** | **>**)
* キーボードの左 (◀️) と右 (▶️) カーソルキー
  {{% /notice %}}
