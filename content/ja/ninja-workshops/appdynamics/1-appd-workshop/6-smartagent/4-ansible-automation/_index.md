---
title: Smart AgentとAnsibleによるMonitoring as Code
linkTitle: Ansible Automation
weight: 4
time: 10 minutes
description: Ansibleを使用してAppDynamics Smart Agentのデプロイを自動化する方法を学びます。
---

## はじめに

このガイドでは、Ansibleを使用してCisco AppDynamics Smart Agentを複数のホストにデプロイする方法を説明します。自動化を活用することで、モニタリングインフラストラクチャの一貫性、堅牢性、スケーラビリティを確保できます。

## アーキテクチャ概要

デプロイアーキテクチャでは、Ansible Control Nodeを活用してターゲットホストへのSmart Agentのインストールと設定をオーケストレーションします。

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

* **Ansible Control Node**: Playbookを実行するマシン（例: ノートPCやジャンプホスト）
* **Target Hosts**: Smart Agentがインストールされるサーバー
* **Inventory**: ターゲットホストとその接続情報のリスト
* **Playbook**: デプロイタスクを定義するYAMLファイル

## 前提条件

開始する前に、以下を確認してください

* SSH経由でターゲットホストにアクセスできること
* ターゲットホストでsudo権限があること
* Smart Agentインストールパッケージ（`.deb` または `.rpm`）がダウンロード済みであること
* AppDynamics Controllerのアカウント情報（Access Key、Account Name、URL）があること

## ステップ1: macOSにAnsibleをインストール

まず、コントロールノードにAnsibleをインストールします。

1. **Homebrewをインストール**（未インストールの場合）

    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

2. **Ansibleをインストール**

    ```bash
    brew install ansible
    ```

3. **インストールを確認**

    ```bash
    ansible --version
    ```

    Ansibleのインストール済みバージョンが表示されます。
