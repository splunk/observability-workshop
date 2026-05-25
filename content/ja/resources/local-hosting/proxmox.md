---
title: Proxmox
weight: 3
description: Proxmox VE でローカルホスティング環境を作成する方法を学びます
---

## Proxmox ワークショップインスタンスのセットアップ

### 概要

`ubuntu-cloud-k3d.sh` スクリプトは、Proxmox VE 上に Splunk Observability Workshop VM の作成を自動化します。必要なツールと設定がすべてプリインストールされた、Ubuntu 24.04 cloud-init ベースの完全な VM を作成します。

#### 前提条件

- 管理者アクセス権を持つ Proxmox VE クラスター
- クラウドイメージとパッケージのダウンロードに必要なインターネット接続
- 使用可能な VM ID 範囲とストレージ容量
- ワークショップアクセス用の有効な SWiPE ID
- **ローカルストレージで Snippets が有効であること** - cloud-init 設定ファイルに必要です。有効にするには
  1. Proxmox Web UI で **Datacenter → Storage → local** に移動します
  2. **Edit** をクリックします
  3. **Content** で、リストに **Snippets** を追加します
  4. **OK** をクリックします

#### クイックスタート

Proxmox ホストでスクリプトを直接実行します

`k3d` スクリプト

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/splunk/observability-workshop/refs/heads/main/local-hosting/proxmox/ubuntu-cloud-k3d.sh)"
```

`k3s` スクリプト（**レガシー**）

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/splunk/observability-workshop/refs/heads/main/local-hosting/proxmox/ubuntu-cloud-k3s.sh)"
```

### スクリプトの動作

#### 1. 初期セットアップ

- パッケージリポジトリを更新し、必要なツール（`jq`、`curl`）をインストールします
- ユーザー確認と SWiPE ID 入力のためのインタラクティブなプロンプトを表示します

#### 2. 認証と設定

- Splunk ワークショップ API に対して SWiPE ID を検証します
- ワークショップトークンと設定（REALM、RUM_TOKEN、INGEST_TOKEN など）を取得します
- 一意の VM ID とホスト名を生成します

#### 3. VM の作成

- Ubuntu 24.04 Noble クラウドイメージをダウンロードします
- ディスクを 40GB にリサイズします
- 以下の仕様で Proxmox VM を作成します
  - **メモリ**: 16GB RAM
  - **CPU**: 4 コア（ホスト CPU タイプ）
  - **ストレージ**: `local-lvm` ストレージを使用
  - **ネットワーク**: DHCP で `vmbr0` にブリッジ接続
  - **ブート**: cloud-init サポート付き UEFI

#### 4. ソフトウェアのインストール

cloud-init 設定により、以下が自動的にインストールされます

- **コンテナツール**: Docker, Docker Compose
- **Kubernetes**: K3s, kubectl, Helm, K9s
- **開発ツール**: OpenJDK 17, Maven, Python3, Git
- **インフラストラクチャ**: Terraform, Ansible
- **モニタリング**: Chaos Mesh

#### 5. ワークショップコンテンツ

- Splunk Observability Workshop の資料をダウンロードします
- ワークショップトークンを使用して Kubernetes シークレットを設定します
- プライベートコンテナレジストリを設定します
- デモアプリケーションとコンテンツを準備します

### VM の仕様

- **OS**: Ubuntu 24.04 LTS (Noble)
- **メモリ**: 16GB RAM
- **CPU**: 4 コア
- **ディスク**: 40GB（拡張可能）
- **ユーザー**: `splunk` / `Splunk123!`
- **SSH**: パスワード認証が有効

### 環境変数

スクリプトは VM 内で以下の環境変数を設定します

- `RUM_TOKEN`: Real User Monitoring トークン
- `ACCESS_TOKEN`: データ取り込みトークン
- `API_TOKEN`: Splunk API トークン
- `HEC_TOKEN`: HTTP Event Collector トークン
- `HEC_URL`: HEC エンドポイント URL
- `REALM`: Splunk レルム
- `INSTANCE`: 一意のホスト名
- `CLUSTER_NAME`: Kubernetes クラスター名

### VM へのアクセス

1. VM の作成と起動が完了するまで待ちます（5〜10 分）
2. Proxmox コンソールまたは DHCP ログで VM の IP アドレスを確認します
3. VM に SSH 接続します

   ```bash
   ssh splunk@<vm-ip>
   # Password: Splunk123!
   ```

### VM 内で便利なコマンド

```bash
# Check Kubernetes status
kubectl get nodes

# Access Kubernetes dashboard
k9s

# View workshop materials
ls ~/workshop/

# Check environment variables
env | grep -E "(TOKEN|REALM)"
```

### トラブルシューティング

- **無効な SWiPE ID**: ワークショップの登録と ID を確認してください
- **VM の作成に失敗**: Proxmox のストレージ容量と権限を確認してください
- **ネットワークの問題**: `vmbr0` ブリッジが正しく設定されていることを確認してください
- **デプロイが遅い**: cloud-init がすべてのインストールを完了するまで追加の時間を確保してください

### タグ

作成された VM には次のタグが付与されます: `o11y-workshop`, `noble`, `k3d`
