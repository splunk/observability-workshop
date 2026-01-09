---
title: リモートインストール
weight: 1
time: 2 minutes
description: smartagentctl を使用して、複数のリモートホストに AppDynamics Smart Agent をインストールおよび管理する方法を学びます。
---

## はじめに

このワークショップでは、**smartagentctl** コマンドラインツールを使用して、複数のリモートホストに同時に **AppDynamics Smart Agent** をインストールおよび管理する方法を紹介します。このアプローチは、Jenkins や GitHub Actions などの追加の自動化ツールを必要とせずに、SSH ベースのリモート実行を使用してサーバーフリートに Smart Agent を迅速にデプロイするのに最適です。

![AppDynamics](https://img.shields.io/badge/AppDynamics-0078D4?style=flat)

## 学習内容

このワークショップでは、以下の方法を学びます：

- `remote.yaml` ファイルを使用した **リモートホストの構成**
- `config.ini` を使用した **Smart Agent 設定の構成**
- SSH 経由で複数のホストに同時に **Smart Agent をデプロイ**
- インフラストラクチャ全体でリモートから **エージェントの開始と停止**
- すべてのリモートホストでの **エージェントステータスの確認**
- 一般的なインストールと接続の問題の **トラブルシューティング**

## 主な機能

- 🚀 **SSH による直接デプロイ** - 追加の自動化プラットフォームが不要
- 🔄 **完全なライフサイクル管理** - エージェントのインストール、開始、停止、アンインストール
- 🏗️ **Configuration as Code** - YAML および INI ベースの構成ファイル
- 🔐 **セキュア** - SSH キーベースの認証
- 📈 **同時実行** - 並列デプロイのための構成可能な同時実行性
- 🎛️ **シンプルな CLI** - 使いやすい smartagentctl コマンドラインインターフェース

## アーキテクチャ概要

```
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
3. **インストールと起動** - リモートホストへの Smart Agent のデプロイと起動
4. **トラブルシューティング** - 一般的な問題と解決策

## 前提条件

- smartagentctl がインストールされた Control Node
- すべてのリモートホストへの SSH アクセス
- 認証用に構成された SSH 秘密鍵
- Control Node での sudo 権限
- SSH が有効になっているリモートホスト
- AppDynamics アカウントの認証情報

## 利用可能なコマンド

`smartagentctl` ツールは、以下のリモート操作をサポートしています：

- `start --remote` - リモートホストに Smart Agent をインストールして起動
- `stop --remote` - リモートホストの Smart Agent を停止
- `status --remote` - リモートホストの Smart Agent ステータスを確認
- `install --remote` - 起動せずに Smart Agent をインストール
- `uninstall --remote` - リモートホストから Smart Agent を削除
- `--service` フラグ - systemd サービスとしてインストール

すべてのコマンドは、詳細なログのための `--verbose` フラグをサポートしています。

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
このワークショップを進める最も簡単な方法は以下を使用することです：

* このページの右上にある左右の矢印（**<** | **>**）
* キーボードの左（◀️）と右（▶️）のカーソルキー
{{% /notice %}}
