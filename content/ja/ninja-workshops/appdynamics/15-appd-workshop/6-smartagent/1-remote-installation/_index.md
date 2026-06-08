---
title: Remote Installation
weight: 1
time: 2 minutes
description: smartagentctl を使用して複数のリモートホストに AppDynamics Smart Agent をインストールおよび管理する方法を学びます。
---

## はじめに

このワークショップでは、**smartagentctl** コマンドラインツールを使用して、複数のリモートホストに **AppDynamics Smart Agent** を同時にインストールおよび管理する方法を説明します。このアプローチは、Jenkins や GitHub Actions などの追加の自動化ツールを必要とせずに、SSH ベースのリモート実行を使用してサーバー群に Smart Agent を迅速にデプロイするのに最適です。

![AppDynamics](https://img.shields.io/badge/AppDynamics-0078D4?style=flat)

## 学習内容

このワークショップでは、以下の方法を学びます

- `remote.yaml` ファイルを使用した**リモートホストの設定**
- `config.ini` を使用した **Smart Agent 設定の構成**
- SSH 経由で複数のホストに同時に **Smart Agent をデプロイ**する方法
- インフラストラクチャ全体でリモートから**エージェントの起動と停止**を行う方法
- すべてのリモートホストで**エージェントのステータスを確認**する方法
- 一般的なインストールおよび接続の問題の**トラブルシューティング**

## 主な機能

- 🚀 **直接 SSH デプロイ** - 追加の自動化プラットフォームが不要
- 🔄 **完全なライフサイクル管理** - エージェントのインストール、起動、停止、アンインストール
- 🏗️ **Configuration as Code** - YAML および INI ベースの設定ファイル
- 🔐 **セキュア** - SSH キーベースの認証
- 📈 **並行実行** - 並列デプロイのための設定可能な同時実行数
- 🎛️ **シンプルな CLI** - 使いやすい smartagentctl コマンドラインインターフェース

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

1. **前提条件** - 必要なアクセス、ツール、および権限
2. **設定** - `config.ini` と `remote.yaml` のセットアップ
3. **インストールと起動** - リモートホストへの Smart Agent のデプロイと起動
4. **トラブルシューティング** - 一般的な問題と解決策

## 前提条件

- smartagentctl がインストールされたコントロールノード
- すべてのリモートホストへの SSH アクセス
- 認証用に設定された SSH 秘密鍵
- コントロールノードでの sudo 権限
- SSH が有効になっているリモートホスト
- AppDynamics アカウントの認証情報

## 利用可能なコマンド

`smartagentctl` ツールは以下のリモート操作をサポートしています

- `start --remote` - リモートホストに Smart Agent をインストールして起動
- `stop --remote` - リモートホストの Smart Agent を停止
- `status --remote` - リモートホストの Smart Agent のステータスを確認
- `install --remote` - Smart Agent を起動せずにインストール
- `uninstall --remote` - リモートホストから Smart Agent を削除
- `--service` フラグ - systemd サービスとしてインストール

すべてのコマンドは詳細なログ出力のために `--verbose` フラグをサポートしています。
