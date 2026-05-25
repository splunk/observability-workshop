---
title: Isovalent Enterprise Platform と Splunk Observability Cloud の統合
linkTitle: Isovalent Splunk Observability 統合
weight: 6
authors: ["Alec Chamberlain"]
time: 105 minutes
description: EKS 上の Cilium、Hubble、Tetragon から eBPF ネットワークおよびランタイムシグナルを Splunk Observability Cloud にストリーミングします — Hubble を活用した DNS 調査を含みます。
---

このワークショップでは、**Isovalent Enterprise Platform と Splunk Observability Cloud** を統合し、eBPF テクノロジーを使用して Kubernetes のネットワーキング、セキュリティ、およびランタイム動作の包括的な可視性を提供する方法を実演します。

## 学習内容

このワークショップを完了すると、以下のことができるようになります

- Amazon EKS に Cilium を CNI として ENI モードでデプロイする
- Hubble を L7 可視性を備えたネットワークオブザーバビリティ用に構成する
- Tetragon をランタイムセキュリティモニタリング用にインストールする
- eBPF ベースのメトリクスを OpenTelemetry を使用して Splunk Observability Cloud と統合する
- ネットワークフロー、セキュリティイベント、およびインフラストラクチャメトリクスを統合ダッシュボードで監視する
- eBPF を活用したオブザーバビリティと kube-proxy の置き換えを理解する

## セクション

- [概要](./1-overview/_index.md) - Cilium アーキテクチャと eBPF の基礎を理解する
- [前提条件](./2-prerequisites/_index.md) - 必要なツールとアクセス
- [EKS セットアップ](./3-eks-setup/_index.md) - Cilium 用の EKS クラスターを作成する
- [Cilium インストール](./4-cilium-installation/_index.md) - Cilium、Hubble、Tetragon をデプロイする
- [Splunk 統合](./5-splunk-integration/_index.md) - メトリクスを Splunk Observability Cloud に接続する
- [検証](./6-verification/_index.md) - 統合を検証する
- [デモスクリプト](./7-demo/_index.md) - エンドツーエンドの DNS 調査シナリオを実行する

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
この統合は、Linux カーネル内で直接高性能かつ低オーバーヘッドのオブザーバビリティを実現するために eBPF（Extended Berkeley Packet Filter）を活用しています。
{{% /notice %}}

## 前提条件

- 適切な認証情報で構成された AWS CLI
- kubectl、eksctl、および Helm 3.x がインストール済みであること
- EKS クラスター、VPC、および EC2 インスタンスを作成する権限を持つ AWS アカウント
- アクセストークンを持つ Splunk Observability Cloud アカウント
- 完全なセットアップに約90分

## 統合のメリット

Isovalent Enterprise Platform を Splunk Observability Cloud に接続することで、以下のメリットが得られます

- 🔍 **深い可視性**: ネットワークフロー、L7 プロトコル（HTTP、DNS、gRPC）、およびランタイムセキュリティイベント
- 🚀 **高パフォーマンス**: 最小限のオーバーヘッドで eBPF ベースのオブザーバビリティを実現
- 🔐 **セキュリティインサイト**: プロセスモニタリング、システムコールトレーシング、およびネットワークポリシーの適用
- 📊 **統合ダッシュボード**: Cilium、Hubble、Tetragon のメトリクスをインフラストラクチャおよび APM データと並べて表示
- ⚡ **効率的なネットワーキング**: kube-proxy の置き換えと ENI モードによるネイティブ VPC ネットワーキング

## ソースリポジトリ

このワークショップで参照されるすべての構成ファイル、Helm values、およびダッシュボード JSON ファイルは、以下のリポジトリで入手できます

- **[isovalent_splunk_o11y](https://github.com/chambear2809/isovalent_splunk_o11y/)** — Helm values、OTel Collector 構成、Splunk ダッシュボード JSON ファイル、および完全な統合ガイド
- **[isovalent-demo-jobs-app](https://github.com/chambear2809/isovalent-demo-jobs-app)** — デモシナリオで使用される jobs-app Helm チャート（エラーインジェクションおよび修復スクリプトを含む）
