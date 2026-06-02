---
title: Monitoring as Code with Smart Agent and Ansible
linkTitle: Ansible Automation
weight: 4
time: 10 minutes
description: Ansible を使用して AppDynamics Smart Agent のデプロイを自動化する方法を学びます。
---

## はじめに

このガイドでは、Ansible を使用して Cisco AppDynamics Smart Agent を複数のホストにデプロイする方法について詳しく説明します。自動化を活用することで、監視インフラストラクチャの一貫性、堅牢性、そして容易なスケーラビリティを確保できます。

## アーキテクチャの概要

このデプロイアーキテクチャでは、Ansible Control Node を活用して、ターゲットホストへの Smart Agent のインストールと構成をオーケストレーションします。

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

### 主要なコンポーネント

* **Ansible Control Node**: Playbook を実行するマシン（例: 自身のラップトップやジャンプホスト）です。
* **Target Hosts**: Smart Agent をインストールするサーバーです。
* **Inventory**: ターゲットホストとその接続情報の一覧です。
* **Playbook**: デプロイタスクを定義した YAML ファイルです。

## 前提条件

開始する前に、以下を満たしていることを確認してください。

* SSH 経由でターゲットホストにアクセスできること。
* ターゲットホストで sudo 権限を持っていること。
* Smart Agent のインストールパッケージ（`.deb` または `.rpm`）をダウンロード済みであること。
* AppDynamics Controller のアカウント情報（Access Key、Account Name、URL）。

## ステップ 1: macOS に Ansible をインストールする

まず、Control Node に Ansible をインストールする必要があります。

1. **Homebrew のインストール**（まだインストールしていない場合）:

    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

2. **Ansible のインストール**:

    ```bash
    brew install ansible
    ```

3. **インストールの検証**:

    ```bash
    ansible --version
    ```

    インストールされた Ansible のバージョンが出力されているはずです。
