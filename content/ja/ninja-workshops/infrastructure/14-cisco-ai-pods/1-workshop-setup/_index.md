---
title: ワークショップのセットアップ
linkTitle: 1. ワークショップのセットアップ
weight: 1
---

このセクションでは、ワークショップの主催者がワークショップをセットアップするために実行する手順を説明します:

* AWS アカウントのセットアップ
* OpenShift の前提条件
* AWS ROSA を使用して、GPU ベースのワーカーノードを持つ **RedHat OpenShift** クラスターをデプロイします。
* **NVIDIA NIM Operator** と **NVIDIA GPU Operator** をデプロイします。
* NVIDIA NIM を使用して **Large Language Model (LLM)** をクラスターにデプロイします。
* 各ワークショップユーザー用に、適切な権限を持つ OpenShift ログインとネームスペースを作成します。
* **Splunk OpenTelemetry collector** の Cluster Receiver コンポーネントをインストールします。
* **Weviate vector database** をクラスターにデプロイします。
* **Portworx Prometheus exporter** を模倣するサービスをデプロイします。
