---
title: リモートインストール
weight: 1
time: 2 minutes
description: smartagentctlを使用して複数のリモートホストにAppDynamics Smart Agentをインストール・管理する方法を学びます。
---

## はじめに

このワークショップでは、**smartagentctl** コマンドラインツールを使用して、複数のリモートホストに **AppDynamics Smart Agent** を同時にインストール・管理する方法を説明します。このアプローチは、JenkinsやGitHub Actionsなどの追加の自動化ツールを必要とせず、SSHベースのリモート実行を使用してサーバー群にSmart Agentを迅速にデプロイするのに最適です。

![AppDynamics](https://img.shields.io/badge/AppDynamics-0078D4?style=flat)

## 学習内容

このワークショップでは、以下の内容を学びます

- `remote.yaml` ファイルを使用した **リモートホストの設定**
- `config.ini` を使用した **Smart Agent設定の構成**
- SSHを介した複数ホストへの **Smart Agentのデプロイ**
- インフラストラクチャ全体でのリモートからの **エージェントの起動と停止**
- すべてのリモートホストでの **エージェントステータスの確認**
- インストールや接続に関する一般的な問題の **トラブルシューティング**

## 主な機能

- 🚀 **SSHによる直接デプロイ** - 追加の自動化プラットフォーム不要
- 🔄 **完全なライフサイクル管理** - エージェントのインストール、起動、停止、アンインストール
- 🏗️ **コードとしての設定** - YAMLおよびINIベースの設定ファイル
- 🔐 **セキュア** - SSH鍵ベースの認証
- 📈 **並行実行** - 並列デプロイのための設定可能な同時実行数
- 🎛️ **シンプルなCLI** - 使いやすいsmartagentctlコマンドラインインターフェース

## アーキテクチャ概要

```text
┌─────────────────────────────────────────────────────────────────┐
│                  Remote Installation Architecture               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Control Node (smartagentctl) ──▶ SSH Connection                │
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

このワークショップには以下が含まれます

1. **前提条件** - 必要なアクセス、ツール、権限
2. **設定** - `config.ini` と `remote.yaml` のセットアップ
3. **インストールと起動** - リモートホストへのSmart Agentのデプロイと起動
4. **トラブルシューティング** - 一般的な問題と解決策

## 前提条件

- smartagentctlがインストールされたコントロールノード
- すべてのリモートホストへのSSHアクセス
- 認証用に設定されたSSH秘密鍵
- コントロールノードでのsudo権限
- SSHが有効なリモートホスト
- AppDynamicsアカウントの認証情報

## 利用可能なコマンド

`smartagentctl` ツールは以下のリモート操作をサポートしています

- `start --remote` - リモートホストにSmart Agentをインストールして起動
- `stop --remote` - リモートホストのSmart Agentを停止
- `status --remote` - リモートホストのSmart Agentステータスを確認
- `install --remote` - Smart Agentを起動せずにインストール
- `uninstall --remote` - リモートホストからSmart Agentを削除
- `--service` フラグ - systemdサービスとしてインストール

すべてのコマンドは詳細なログ出力のための `--verbose` フラグをサポートしています。
