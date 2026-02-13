---
title: Smart Agent と Ansible によるモニタリングのコード化
linkTitle: Ansible 自動化
weight: 4
time: 10 minutes
description: Ansible を使用した AppDynamics Smart Agent デプロイの自動化について学びます。
---

## はじめに

このガイドでは、Ansible を使用して Cisco AppDynamics Smart Agent を複数のホストにデプロイする方法を説明します。自動化を活用することで、モニタリングインフラストラクチャの一貫性、堅牢性、スケーラビリティを確保できます。

## アーキテクチャの概要

デプロイアーキテクチャは、Ansible コントロールノードを活用して、ターゲットホストへの Smart Agent のインストールと設定をオーケストレーションします。

```mermaid
graph TD
    CN[Ansible Control Node<br/>(macOS/Linux)] -->|SSH| H1[Target Host 1<br/>(Debian/RedHat)]
    CN -->|SSH| H2[Target Host 2<br/>(Debian/RedHat)]
    CN -->|SSH| H3[Target Host N<br/>(Debian/RedHat)]

    subgraph "Target Host Configuration"
        SA[Smart Agent Service]
        Config[config.ini]
        Package[Installer .deb/.rpm]
    end

    H1 --> SA
    H2 --> SA
    H3 --> SA
```

### 主要コンポーネント

* **Ansible Control Node**: プレイブックを実行するマシン（例: ラップトップやジャンプホスト）です。
* **Target Hosts**: Smart Agent がインストールされるサーバーです。
* **Inventory**: ターゲットホストとその接続情報の一覧です。
* **Playbook**: デプロイタスクを定義する YAML ファイルです。

## 前提条件

開始する前に、以下を確認してください：

* SSH 経由でターゲットホストにアクセスできること。
* ターゲットホストで sudo 権限を持っていること。
* Smart Agent インストールパッケージ（`.deb` または `.rpm`）をダウンロード済みであること。
* AppDynamics Controller のアカウント情報（Access Key、Account Name、URL）を用意していること。

## ステップ1: macOS に Ansible をインストールする

まず、コントロールノードに Ansible をインストールします。

1. **Homebrew をインストール** します（未インストールの場合）：

    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

2. **Ansible をインストール** します：

    ```bash
    brew install ansible
    ```

3. **インストールを確認** します：

    ```bash
    ansible --version
    ```

    Ansible のインストール済みバージョンを示す出力が表示されます。
