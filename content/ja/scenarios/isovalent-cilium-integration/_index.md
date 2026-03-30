---
title: Isovalent Enterprise Platform と Splunk Observability Cloud の統合
linkTitle: Isovalent Splunk Observability 統合
weight: 6
archetype: chapter
authors: ["Alec Chamberlain"]
time: 105 minutes
description: Amazon EKS に Isovalent Enterprise Platform（Cilium、Hubble、Tetragon）をデプロイし、Splunk Observability Cloud と統合して、eBPF ベースの包括的な監視とオブザーバビリティを実現します。Hubble ダッシュボードを使用した DNS 問題の調査を含むエンドツーエンドのデモが含まれています。
---

このワークショップでは、**Isovalent Enterprise Platform と Splunk Observability Cloud の統合**を実演し、eBPFテクノロジーを使用してKubernetesのネットワーキング、セキュリティ、ランタイム動作の包括的な可視性を提供する方法を説明します。

## 学習内容

このワークショップを完了すると、以下のことができるようになります：

- ENIモードでCiliumをCNIとして使用するAmazon EKSをデプロイする
- L7可視性を備えたネットワークオブザーバビリティのためのHubbleを設定する
- ランタイムセキュリティ監視のためのTetragonをインストールする
- OpenTelemetryを使用してeBPFベースのメトリクスをSplunk Observability Cloudと統合する
- 統合ダッシュボードでネットワークフロー、セキュリティイベント、インフラストラクチャメトリクスを監視する
- eBPFによるオブザーバビリティとkube-proxyの置き換えを理解する

## セクション

- [概要](./1-overview/_index.md) - CiliumアーキテクチャとeBPFの基礎を理解する
- [前提条件](./2-prerequisites/_index.md) - 必要なツールとアクセス権
- [EKS セットアップ](./3-eks-setup/_index.md) - Cilium用のEKSクラスターを作成する
- [Cilium インストール](./4-cilium-installation/_index.md) - Cilium、Hubble、Tetragonをデプロイする
- [Splunk 統合](./5-splunk-integration/_index.md) - メトリクスをSplunk Observability Cloudに接続する
- [検証](./6-verification/_index.md) - 統合を検証する
- [デモスクリプト](./7-demo/_index.md) - エンドツーエンドのDNS調査シナリオをウォークスルーする

{{% notice title="ヒント" style="primary" icon="lightbulb" %}}
この統合は、Linuxカーネル内で直接、高性能で低オーバーヘッドのオブザーバビリティを実現するためにeBPF（Extended Berkeley Packet Filter）を活用しています。
{{% /notice %}}

## 前提条件

- 適切な認証情報で設定されたAWS CLI
- kubectl、eksctl、Helm 3.xがインストールされていること
- EKSクラスター、VPC、EC2インスタンスを作成する権限を持つAWSアカウント
- アクセストークンを持つSplunk Observability Cloudアカウント
- 完全なセットアップに約90分

## 統合のメリット

Isovalent Enterprise PlatformをSplunk Observability Cloudに接続することで、以下のメリットが得られます：

- 🔍 **深い可視性**: ネットワークフロー、L7プロトコル（HTTP、DNS、gRPC）、ランタイムセキュリティイベント
- 🚀 **高パフォーマンス**: 最小限のオーバーヘッドでeBPFベースのオブザーバビリティを実現
- 🔐 **セキュリティインサイト**: プロセス監視、システムコールトレーシング、ネットワークポリシーの適用
- 📊 **統合ダッシュボード**: Cilium、Hubble、TetragonのメトリクスをインフラストラクチャおよびAPMデータと並べて表示
- ⚡ **効率的なネットワーキング**: kube-proxyの置き換えとENIモードによるネイティブVPCネットワーキング

## ソースリポジトリ

このワークショップで参照されるすべての設定ファイル、Helm values、ダッシュボードJSONファイルは、以下のリポジトリで入手できます：

- **[isovalent_splunk_o11y](https://github.com/chambear2809/isovalent_splunk_o11y/)** — Helm values、OTel Collector設定、SplunkダッシュボードJSONファイル、および完全な統合ガイド
- **[isovalent-demo-jobs-app](https://github.com/chambear2809/isovalent-demo-jobs-app)** — デモシナリオで使用されるjobs-app Helm chart（エラーインジェクションと修復スクリプトを含む）

{{% children depth="1" type="card" description="true" %}}
