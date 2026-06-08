---
title: Smart Agent と Ansible によるモニタリングのコード化
linkTitle: Ansible Automation
weight: 4
time: 10 minutes
description: Ansible を使用して AppDynamics Smart Agent のデプロイを自動化する方法を学びます。
---

## はじめに

このガイドでは、Ansible を使用して Cisco AppDynamics Smart Agent を複数のホストにデプロイする方法を詳しく説明します。自動化を活用することで、モニタリングインフラストラクチャの一貫性、堅牢性、および容易なスケーラビリティを確保できます。

## アーキテクチャの概要

デプロイアーキテクチャは、Ansible Control Node を活用してターゲットホストへの Smart Agent のインストールと設定をオーケストレーションします。

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

* **Ansible Control Node**: Playbook を実行するマシンです（例: ノートパソコンやジャンプホスト）。
* **Target Hosts**: Smart Agent がインストールされるサーバーです。
* **Inventory**: ターゲットホストとその接続情報のリストです。
* **Playbook**: デプロイタスクを定義する YAML ファイルです。

## 前提条件

開始する前に、以下を確認してください:

* SSH 経由でターゲットホストにアクセスできること。
* ターゲットホストでの sudo 権限があること。
* Smart Agent インストールパッケージ（`.deb` または `.rpm`）がダウンロード済みであること。
* AppDynamics Controller のアカウント情報（Access Key、Account Name、URL）があること。

## ステップ 1: macOS に Ansible をインストールする

まず、コントロールノードに Ansible をインストールする必要があります。

1. **Homebrew をインストールする**（未インストールの場合）:

    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

2. **Ansible をインストールする**:

    ```bash
    brew install ansible
    ```

3. **インストールを確認する**:

    ```bash
    ansible --version
    ```

    インストールされた Ansible のバージョンを示す出力が表示されます。
