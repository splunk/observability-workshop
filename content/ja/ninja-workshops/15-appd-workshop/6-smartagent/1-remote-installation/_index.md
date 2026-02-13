---
title: リモートインストール
weight: 1
time: 2 minutes
description: smartagentctl を使用して、複数のリモートホストに AppDynamics Smart Agent をインストールおよび管理する方法を学びます。
---

## はじめに

このワークショップでは、**smartagentctl** コマンドラインツールを使用して、複数のリモートホストに同時に **AppDynamics Smart Agent** をインストールおよび管理する方法を紹介します。このアプローチは、JenkinsやGitHub Actionsなどの追加の自動化ツールを必要とせずに、SSHベースのリモート実行を使用してサーバーフリートにSmart Agentを迅速にデプロイするのに最適です。

![AppDynamics](https://img.shields.io/badge/AppDynamics-0078D4?style=flat)

## 学習内容

このワークショップでは、以下の方法を学びます：

- `remote.yaml` ファイルを使用した **リモートホストの構成**
- `config.ini` を使用した **Smart Agent 設定の構成**
- SSH経由で複数のホストに同時に **Smart Agent をデプロイ**
- インフラストラクチャ全体でリモートから **エージェントの開始と停止**
- すべてのリモートホストでの **エージェントステータスの確認**
- 一般的なインストールと接続の問題の **トラブルシューティング**

## 主な機能

- 🚀 **SSH による直接デプロイ** - 追加の自動化プラットフォームが不要
- 🔄 **完全なライフサイクル管理** - エージェントのインストール、開始、停止、アンインストール
- 🏗️ **Configuration as Code** - YAMLおよびINIベースの構成ファイル
- 🔐 **セキュア** - SSHキーベースの認証
- 📈 **同時実行** - 並列デプロイのための構成可能な同時実行性
- 🎛️ **シンプルな CLI** - 使いやすいsmartagentctlコマンドラインインターフェース

## アーキテクチャ概要

```text
┌─────────────────────────────────────────────────────────────────┐
│                  Remote Installation Architecture                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Control Node (smartagentctl) ──▶ SSH Connection               │
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

このワークショップには以下が含まれます：

1. **前提条件** - 必要なアクセス、ツール、権限
2. **構成** - `config.ini` と `remote.yaml` のセットアップ
3. **インストールと起動** - リモートホストへのSmart Agentのデプロイと起動
4. **トラブルシューティング** - 一般的な問題と解決策

## 前提条件

- smartagentctlがインストールされたControl Node
- すべてのリモートホストへのSSHアクセス
- 認証用に構成されたSSH秘密鍵
- Control Nodeでのsudo権限
- SSHが有効になっているリモートホスト
- AppDynamicsアカウントの認証情報

## 利用可能なコマンド

`smartagentctl` ツールは、以下のリモート操作をサポートしています：

- `start --remote` - リモートホストにSmart Agentをインストールして起動
- `stop --remote` - リモートホストのSmart Agentを停止
- `status --remote` - リモートホストのSmart Agentステータスを確認
- `install --remote` - 起動せずにSmart Agentをインストール
- `uninstall --remote` - リモートホストからSmart Agentを削除
- `--service` フラグ - systemdサービスとしてインストール

すべてのコマンドは、詳細なログのための `--verbose` フラグをサポートしています。

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
このワークショップを進める最も簡単な方法は以下を使用することです：

- このページの右上にある左右の矢印（**<** | **>**）
- キーボードの左（◀️）と右（▶️）のカーソルキー
{{% /notice %}}
