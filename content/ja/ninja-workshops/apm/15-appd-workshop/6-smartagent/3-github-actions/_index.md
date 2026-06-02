---
title: GitHub Actions による自動化
weight: 3
time: 2 minutes
description: GitHub Actions とセルフホストランナーを利用して、AppDynamics Smart Agent のデプロイを自動化する方法を学びます。
---

## はじめに

このワークショップでは、**GitHub Actions** とセルフホストランナーを使用して、複数の EC2 インスタンスへの **AppDynamics Smart Agent** のデプロイとライフサイクル管理を自動化する方法を解説します。10 台のホストを管理する場合でも、10,000 台のホストを管理する場合でも、本ガイドではスケーラブルかつセキュアで再現可能な Smart Agent オペレーションを実現するための GitHub Actions ワークフロー活用方法を紹介します。

![GitHub Actions and AppDynamics](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat&logo=github-actions&logoColor=white) ![AppDynamics](https://img.shields.io/badge/AppDynamics-0078D4?style=flat)

## このワークショップで学ぶこと

このワークショップでは、以下の内容を学習します。

- GitHub Actions ワークフローを利用して、複数のホストに **Smart Agent をデプロイ**する方法
- 安全な認証情報管理のために **GitHub の secrets と variables を設定**する方法
- AWS VPC 内に**セルフホストランナーをセットアップ**する方法
- 数千台のホストに対応するための**自動バッチ処理を実装**する方法
- インストール、アンインストール、停止、クリーンアップを含む**エージェントの完全なライフサイクル管理**
- **ワークフローの実行状況を監視**し、問題をトラブルシュートする方法

## 主な機能

- 🚀 **並列デプロイ** - 複数のホストに同時にデプロイ
- 🔄 **完全なライフサイクル管理** - エージェントの全オペレーションを網羅する 11 個のワークフロー
- 🏗️ **Infrastructure as Code** - すべてのワークフローを GitHub でバージョン管理
- 🔐 **セキュア** - SSH キーを GitHub secrets として保存し、プライベート VPC ネットワーキングを使用
- 📈 **大規模なスケーラビリティ** - 自動バッチ処理により数千台のホストへのデプロイに対応
- 🎛️ **セルフホストランナー** - 自身の AWS VPC 内で実行

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

このワークショップには、以下の内容が含まれます。

1. **アーキテクチャと設計** - GitHub Actions ワークフローのアーキテクチャを理解する
2. **GitHub のセットアップ** - secrets、variables、セルフホストランナーの設定
3. **ワークフローの作成** - 利用可能な 11 個のワークフローの理解と使用方法
4. **デプロイの実行** - ワークフローの実行とインストールの検証

## 利用可能なワークフロー

このソリューションには、Smart Agent の完全なライフサイクル管理のための **11 個のワークフロー**が含まれています。

| カテゴリ | ワークフロー数 | 説明 |
| -------- | --------- | ----------- |
| **デプロイ** | 1 | Smart Agent のデプロイと起動 |
| **エージェントのインストール** | 4 | Node、Machine、DB、Java の各エージェントをインストール |
| **エージェントのアンインストール** | 4 | 特定のエージェントタイプをアンインストール |
| **エージェント管理** | 2 | 停止／クリーンアップと完全クリーンアップ |

すべてのワークフローはスケーラビリティのための自動バッチ処理に対応しています。

## 前提条件

- リポジトリへのアクセス権を持つ GitHub アカウント
- Ubuntu EC2 インスタンスを含む AWS VPC
- 同じ VPC 内のセルフホスト GitHub Actions ランナー
- 認証用の SSH キーペア
- AppDynamics Smart Agent パッケージ

## GitHub リポジトリ

すべてのワークフローコードと設定ファイルは、以下の GitHub リポジトリで公開されています。

**[https://github.com/chambear2809/github-actions-lab](https://github.com/chambear2809/github-actions-lab)**

リポジトリには以下が含まれます。

- 11 個の完全なワークフロー YAML ファイル
- 詳細なセットアップドキュメント
- アーキテクチャ図
- トラブルシューティングガイド
