---
title: GitHub Actionsによる自動化
weight: 3
time: 2 minutes
description: セルフホストランナーを使用したGitHub ActionsによるAppDynamics Smart Agentデプロイメントの自動化方法を学びます。
---

## はじめに

このワークショップでは、セルフホストランナーを使用した **GitHub Actions** で、複数のEC2インスタンスにわたる **AppDynamics Smart Agent** のデプロイメントとライフサイクル管理を自動化する方法を説明します。10台のホストでも10,000台のホストでも、GitHub Actionsワークフローを活用してスケーラブルで安全かつ再現可能なSmart Agent運用を実現する方法を学びます。

![GitHub Actions and AppDynamics](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat&logo=github-actions&logoColor=white) ![AppDynamics](https://img.shields.io/badge/AppDynamics-0078D4?style=flat)

## 学習内容

このワークショップでは、以下の内容を学びます。

- **Smart Agentのデプロイ** - GitHub Actionsワークフローを使用して複数のホストにデプロイ
- **GitHubシークレットと変数の設定** - 安全な認証情報管理
- **セルフホストランナーのセットアップ** - AWS VPC内での構成
- **自動バッチ処理の実装** - 数千台のホストへのスケーリング
- **エージェントライフサイクルの完全管理** - インストール、アンインストール、停止、クリーンアップ
- **ワークフロー実行の監視** - トラブルシューティング

## 主な機能

- 🚀 **並列デプロイメント** - 複数のホストに同時にデプロイ
- 🔄 **完全なライフサイクル管理** - すべてのエージェント操作をカバーする11のワークフロー
- 🏗️ **Infrastructure as Code** - すべてのワークフローをGitHubでバージョン管理
- 🔐 **セキュア** - SSHキーをGitHubシークレットに保存、プライベートVPCネットワーキング
- 📈 **大規模スケーラビリティ** - 自動バッチ処理で数千台のホストにデプロイ
- 🎛️ **セルフホストランナー** - AWS VPC内で実行

## アーキテクチャ概要

```text
┌─────────────────────────────────────────────────────────────────┐
│                  GitHub Actions-based Deployment                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Developer ──▶ GitHub.com ──▶ Self-hosted Runner (AWS VPC)      │
│                                          │                      │
│                                          ├──▶ Host 1 (SSH)      │
│                                          ├──▶ Host 2 (SSH)      │
│                                          ├──▶ Host 3 (SSH)      │
│                                          └──▶ Host N (SSH)      │
│                                                                 │
│  All hosts send metrics ──▶ AppDynamics Controller              │
└─────────────────────────────────────────────────────────────────┘
```

## ワークショップの構成

このワークショップには以下が含まれます。

1. **アーキテクチャと設計** - GitHub Actionsワークフローアーキテクチャの理解
2. **GitHubセットアップ** - シークレット、変数、セルフホストランナーの設定
3. **ワークフロー作成** - 11の利用可能なワークフローの理解と使用
4. **デプロイメント実行** - ワークフローの実行とインストールの検証

## 利用可能なワークフロー

このソリューションには、Smart Agentの完全なライフサイクル管理のための **11のワークフロー** が含まれています。

| カテゴリ | ワークフロー数 | 説明 |
| -------- | --------- | ----------- |
| **デプロイメント** | 1 | Smart Agentのデプロイと起動 |
| **エージェントインストール** | 4 | Node、Machine、DB、Javaエージェントのインストール |
| **エージェントアンインストール** | 4 | 特定のエージェントタイプのアンインストール |
| **エージェント管理** | 2 | 停止/クリーンおよび完全クリーンアップ |

すべてのワークフローはスケーラビリティのための自動バッチ処理をサポートしています。

## 前提条件

- リポジトリアクセス権のあるGitHubアカウント
- Ubuntu EC2インスタンスを持つAWS VPC
- 同じVPC内のセルフホストGitHub Actionsランナー
- 認証用のSSHキーペア
- AppDynamics Smart Agentパッケージ

## GitHubリポジトリ

すべてのワークフローコードと設定ファイルはGitHubリポジトリで利用可能です。

**[https://github.com/chambear2809/github-actions-lab](https://github.com/chambear2809/github-actions-lab)**

リポジトリには以下が含まれます。

- 11の完全なワークフローYAMLファイル
- 詳細なセットアップドキュメント
- アーキテクチャ図
- トラブルシューティングガイド
