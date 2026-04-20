---
title: Isovalent Enterprise Platform と Splunk Observability Cloud の統合
linkTitle: Isovalent Splunk Observability 統合
weight: 6
archetype: chapter
authors: ["Alec Chamberlain"]
time: 105 minutes
description: Amazon EKS 上に Isovalent Enterprise Platform（Cilium、Hubble、Tetragon）をデプロイし、Splunk Observability Cloud と統合して、eBPF ベースの包括的なモニタリングとオブザーバビリティを実現します。Hubble ダッシュボードを使用した DNS 問題調査のエンドツーエンドデモを含みます。
---

このワークショップでは、**Isovalent Enterprise Platform と Splunk Observability Cloud** を統合し、eBPF テクノロジーを使用して Kubernetes のネットワーキング、セキュリティ、およびランタイム動作に対する包括的な可視性を提供する方法を紹介します。

## 学習内容

このワークショップを完了すると、以下のことができるようになります

- ENI モードで Cilium を CNI として使用する Amazon EKS のデプロイ
- L7 可視性を備えたネットワークオブザーバビリティのための Hubble の設定
- ランタイムセキュリティモニタリングのための Tetragon のインストール
- OpenTelemetry を使用した eBPF ベースのメトリクスと Splunk Observability Cloud の統合
- 統合ダッシュボードでのネットワークフロー、セキュリティイベント、インフラストラクチャメトリクスのモニタリング
- eBPF を活用したオブザーバビリティと kube-proxy の置き換えの理解

## セクション

- [概要](./1-overview/_index.md) - Cilium アーキテクチャと eBPF の基礎を理解する
- [前提条件](./2-prerequisites/_index.md) - 必要なツールとアクセス
- [EKS セットアップ](./3-eks-setup/_index.md) - Cilium 用の EKS クラスターを作成する
- [Cilium インストール](./4-cilium-installation/_index.md) - Cilium、Hubble、Tetragon をデプロイする
- [Splunk 統合](./5-splunk-integration/_index.md) - メトリクスを Splunk Observability Cloud に接続する
- [検証](./6-verification/_index.md) - 統合を検証する
- [デモスクリプト](./7-demo/_index.md) - エンドツーエンドの DNS 調査シナリオを実施する

{{% notice title="ヒント" style="primary" icon="lightbulb" %}}
この統合では、Linux カーネル内で直接動作する高パフォーマンス・低オーバーヘッドのオブザーバビリティのために eBPF（Extended Berkeley Packet Filter）を活用しています。
{{% /notice %}}

## 前提条件

- 適切な認証情報が設定された AWS CLI
- kubectl、eksctl、および Helm 3.x がインストール済みであること
- EKS クラスター、VPC、EC2 インスタンスを作成する権限を持つ AWS アカウント
- アクセストークンを持つ Splunk Observability Cloud アカウント
- 完全なセットアップに約90分

## 統合のメリット

Isovalent Enterprise Platform を Splunk Observability Cloud に接続することで、以下のメリットが得られます

- 🔍 **詳細な可視性**: ネットワークフロー、L7 プロトコル（HTTP、DNS、gRPC）、およびランタイムセキュリティイベント
- 🚀 **高パフォーマンス**: 最小限のオーバーヘッドによる eBPF ベースのオブザーバビリティ
- 🔐 **セキュリティインサイト**: プロセスモニタリング、システムコールトレーシング、およびネットワークポリシーの適用
- 📊 **統合ダッシュボード**: インフラストラクチャおよび APM データと並んだ Cilium、Hubble、Tetragon のメトリクス
- ⚡ **効率的なネットワーキング**: kube-proxy の置き換えと ENI モードによるネイティブ VPC ネットワーキング

## ソースリポジトリ

このワークショップで参照されるすべての設定ファイル、Helm values、およびダッシュボード JSON ファイルは、以下のリポジトリで利用できます

- **[isovalent_splunk_o11y](https://github.com/chambear2809/isovalent_splunk_o11y/)** — Helm values、OTel Collector 設定、Splunk ダッシュボード JSON ファイル、および完全な統合ガイド
- **[isovalent-demo-jobs-app](https://github.com/chambear2809/isovalent-demo-jobs-app)** — デモシナリオで使用される jobs-app Helm チャート（エラーインジェクションおよび修復スクリプトを含む）
