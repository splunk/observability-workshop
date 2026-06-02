---
title: Workshop Setup
linkTitle: 1. Workshop Setup
weight: 1
---

このセクションには、ワークショップ主催者がワークショップをセットアップするために実行すべき手順が含まれます。

* AWS アカウントのセットアップ
* OpenShift の前提条件
* AWS ROSA を使用して、GPU ベースのワーカーノードを持つ **RedHat OpenShift** クラスターをデプロイします。
* **NVIDIA NIM Operator** と **NVIDIA GPU Operator** をデプロイします。
* NVIDIA NIM を使用してクラスターに **Large Language Model (LLM)** をデプロイします。
* 適切な権限を持つ OpenShift ログインと名前空間を、各ワークショップユーザー向けに作成します。
* **Splunk OpenTelemetry collector** の Cluster Receiver コンポーネントをインストールします。
* クラスターに **Weviate vector database** をデプロイします。
* **Portworx Prometheus exporter** を模倣するサービスをデプロイします。
