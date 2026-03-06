---
title: GitHub Actions による自動化
weight: 3
time: 2 minutes
description: セルフホストランナーを使用した GitHub Actions による AppDynamics Smart Agent デプロイの自動化方法を学びます。
---

## はじめに

このワークショップでは、セルフホストランナーを使用した **GitHub Actions** で、複数のEC2インスタンスにわたる **AppDynamics Smart Agent** のデプロイとライフサイクル管理を自動化する方法を紹介します。10台のホストでも10,000台のホストでも、このガイドではスケーラブルで安全かつ再現可能なSmart Agent運用のためにGitHub Actionsワークフローを活用する方法を説明します。

![GitHub Actions and AppDynamics](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat&logo=github-actions&logoColor=white) ![AppDynamics](https://img.shields.io/badge/AppDynamics-0078D4?style=flat)

## 学習内容

このワークショップでは、以下の内容を学びます:

- GitHub Actionsワークフローを使用して複数のホストに **Smart Agent をデプロイ** する
- 安全な認証情報管理のために **GitHub Secrets と Variables を設定** する
- AWS VPC内に **セルフホストランナーをセットアップ** する
- 数千台のホストにスケールするための **自動バッチ処理を実装** する
- インストール、アンインストール、停止、クリーンアップなど **エージェントの完全なライフサイクルを管理** する
- **ワークフローの実行を監視** し、問題をトラブルシューティングする

## 主な機能

- **並列デプロイ** - 複数のホストに同時にデプロイ
- **完全なライフサイクル管理** - エージェントのすべての操作をカバーする11のワークフロー
- **Infrastructure as Code** - すべてのワークフローをGitHubでバージョン管理
- **セキュア** - SSH鍵はGitHub Secretsに保存、プライベートVPCネットワーキング
- **大規模スケーラブル** - 自動バッチ処理で数千台のホストにデプロイ
- **セルフホストランナー** - AWS VPC内で実行

## アーキテクチャ概要

```text
┌─────────────────────────────────────────────────────────────────┐
│                  GitHub Actions-based Deployment                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Developer ──▶ GitHub.com ──▶ Self-hosted Runner (AWS VPC)     │
│                                          │                       │
│                                          ├──▶ Host 1 (SSH)      │
│                                          ├──▶ Host 2 (SSH)      │
│                                          ├──▶ Host 3 (SSH)      │
│                                          └──▶ Host N (SSH)      │
│                                                                  │
│  All hosts send metrics ──▶ AppDynamics Controller             │
└─────────────────────────────────────────────────────────────────┘
```

## ワークショップの構成

このワークショップは以下の内容で構成されています:

1. **アーキテクチャと設計** - GitHub Actionsワークフローアーキテクチャの理解
2. **GitHub のセットアップ** - Secrets、Variables、セルフホストランナーの設定
3. **ワークフローの作成** - 11の利用可能なワークフローの理解と使用
4. **デプロイの実行** - ワークフローの実行とインストールの検証

## 利用可能なワークフロー

このソリューションには、Smart Agentの完全なライフサイクル管理のための **11のワークフロー** が含まれています:

| カテゴリ | ワークフロー数 | 説明 |
| --- | --- | --- |
| **デプロイ** | 1 | Smart Agent のデプロイと起動 |
| **エージェントのインストール** | 4 | Node、Machine、DB、Java エージェントのインストール |
| **エージェントのアンインストール** | 4 | 特定のエージェントタイプのアンインストール |
| **エージェント管理** | 2 | 停止/クリーンおよび完全なクリーンアップ |

すべてのワークフローはスケーラビリティのための自動バッチ処理をサポートしています。

## 前提条件

- リポジトリアクセス権を持つGitHubアカウント
- Ubuntu EC2インスタンスを持つAWS VPC
- 同じVPC内のセルフホストGitHub Actionsランナー
- 認証用のSSHキーペア
- AppDynamics Smart Agentパッケージ

## GitHub リポジトリ

すべてのワークフローコードと設定ファイルはGitHubリポジトリで利用できます:

**[https://github.com/chambear2809/github-actions-lab](https://github.com/chambear2809/github-actions-lab)**

リポジトリには以下が含まれています:

- 11の完全なワークフロー YAMLファイル
- 詳細なセットアップドキュメント
- アーキテクチャ図
- トラブルシューティングガイド

{{% notice title="ヒント" style="primary" icon="lightbulb" %}}
このワークショップを最も簡単にナビゲートするには、以下を使用します:

- このページの右上にある左右の矢印（**<** | **>**）
- キーボードの左（◀️）および右（▶️）カーソルキー
{{% /notice %}}
