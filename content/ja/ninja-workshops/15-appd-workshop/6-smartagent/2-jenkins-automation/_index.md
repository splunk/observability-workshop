---
title: Jenkins 自動化
weight: 2
time: 2 minutes
description: Jenkins パイプラインを使用して、複数のホストにわたる AppDynamics Smart Agent のデプロイとライフサイクル管理を自動化する方法を学びます。
---

## はじめに

このワークショップでは、**Jenkins** を使用して複数の EC2 インスタンスにわたる **AppDynamics Smart Agent** のデプロイとライフサイクル管理を自動化する方法を紹介します。10台のホストでも10,000台のホストでも、Jenkins パイプラインを活用したスケーラブルで安全かつ再現性のある Smart Agent 運用方法を説明します。

![Jenkins and AppDynamics](https://img.shields.io/badge/Jenkins-D24939?style=flat&logo=jenkins&logoColor=white) ![AppDynamics](https://img.shields.io/badge/AppDynamics-0078D4?style=flat)

## 学習内容

このワークショップでは、以下の内容を学びます:

- Jenkins を使用して複数のホストに同時に **Smart Agent をデプロイ** する
- 安全な SSH および AppDynamics アクセスのために **Jenkins 認証情報を設定** する
- 柔軟なデプロイシナリオのために **パラメータ化されたパイプラインを作成** する
- 数千台のホストに対応するために **バッチ処理を実装** する
- インストール、設定、停止、クリーンアップを含む **エージェントの完全なライフサイクルを管理** する
- 自動エラー追跡とレポートにより **障害を適切に処理** する

## 主な機能

- **並列デプロイ** - 複数のホストに同時にデプロイ
- **完全なライフサイクル管理** - エージェントのインストール、アンインストール、停止、クリーンアップ
- **Infrastructure as Code** - すべてのパイプラインをバージョン管理
- **セキュア** - Jenkins 認証情報による SSH 鍵ベースの認証
- **大規模スケーラブル** - 自動バッチ処理により数千台のホストにデプロイ
- **Jenkins Agent** - AWS VPC 内で実行

## アーキテクチャ概要

```text
┌─────────────────────────────────────────────────────────────────┐
│                    Jenkins-based Deployment                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Developer ──▶ Jenkins Master ──▶ Jenkins Agent (AWS VPC)      │
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

このワークショップには以下の内容が含まれます:

1. **アーキテクチャと設計** - システム設計とネットワークトポロジーの理解
2. **Jenkins セットアップ** - Jenkins、認証情報、エージェントの設定
3. **パイプライン作成** - デプロイパイプラインの作成と設定
4. **デプロイワークフロー** - デプロイの実行とインストールの検証

## 前提条件

- Jenkins サーバー（2.300以降）と Pipeline プラグイン
- ターゲット EC2 インスタンスと同じ VPC 内の Jenkins エージェント
- 認証用の SSH キーペア
- AppDynamics Smart Agent パッケージ
- SSH アクセス可能なターゲット Ubuntu EC2 インスタンス

## GitHub リポジトリ

すべてのパイプラインコードと設定ファイルは GitHub リポジトリで公開されています:

**[https://github.com/chambear2809/sm-jenkins](https://github.com/chambear2809/sm-jenkins)**

リポジトリには以下が含まれます:

- 完全な Jenkinsfile パイプライン定義
- 詳細なセットアップドキュメント
- 設定例
- トラブルシューティングガイド

{{% notice title="ヒント" style="primary" icon="lightbulb" %}}
このワークショップを最も簡単にナビゲートするには、以下を使用します:

- このページの右上にある左右の矢印（ **<** | **>** ）
- キーボードの左（◀️）および右（▶️）カーソルキー
{{% /notice %}}
