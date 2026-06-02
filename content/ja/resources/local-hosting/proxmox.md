---
title: Proxmox
weight: 3
description: Proxmox VEホスト上でのローカルホスティング。
---

## Proxmoxワークショップインスタンスのセットアップ

### 概要

`ubuntu-cloud-k3d.sh`スクリプトは、Proxmox VE上でのSplunk Observability ワークショップ用VM作成を自動化します。必要なすべてのツールと設定がプリインストールされた、Ubuntu 24.04のcloud-initベースのVMを作成します。

#### 前提条件

- 管理者権限があるProxmox VEクラスター
- クラウドイメージとパッケージをダウンロードするためのインターネット接続
- 利用可能なVM IDの範囲とストレージ容量
- ワークショップアクセス用の有効なSWiPE ID
- **ローカルストレージでSnippetsが有効化されていること** - cloud-init設定ファイルに必要です。有効化する手順:
  1. ProxmoxのWeb UIで **Datacenter → Storage → local** に移動します
  2. **Edit** をクリックします
  3. **Content** で、**Snippets** をリストに追加します
  4. **OK** をクリックします

#### クイックスタート

Proxmoxホスト上で直接スクリプトを実行します。

`k3d` スクリプト:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/splunk/observability-workshop/refs/heads/main/local-hosting/proxmox/ubuntu-cloud-k3d.sh)"
```

`k3s` スクリプト (**LEGACY**):

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/splunk/observability-workshop/refs/heads/main/local-hosting/proxmox/ubuntu-cloud-k3s.sh)"
```

### スクリプトの動作内容

#### 1. 初期セットアップ

- パッケージリポジトリを更新し、必要なツール (`jq`, `curl`) をインストールします
- ユーザー確認とSWiPE ID入力のための対話的なプロンプトを表示します

#### 2. 認証と設定

- Splunkワークショップ APIに対してSWiPE IDを検証します
- ワークショップトークンと設定 (REALM、RUM_TOKEN、INGEST_TOKENなど) を取得します
- 一意のVM IDとホスト名を生成します

#### 3. VMの作成

- Ubuntu 24.04 Nobleクラウドイメージをダウンロードします
- ディスクを40GBにリサイズします
- 以下の構成でProxmox VMを作成します:
  - **Memory**: 16GB RAM
  - **CPU**: 4コア (ホストCPUタイプ)
  - **Storage**: `local-lvm` ストレージを使用
  - **Network**: `vmbr0` にブリッジしてDHCPを使用
  - **Boot**: UEFIでcloud-initをサポート

#### 4. ソフトウェアのインストール

cloud-init設定により、以下が自動的にインストールされます:

- **Container Tools**: Docker、Docker Compose
- **Kubernetes**: K3s、kubectl、Helm、K9s
- **Development**: OpenJDK 17、Maven、Python3、Git
- **Infrastructure**: Terraform、Ansible
- **Monitoring**: Chaos Mesh

#### 5. ワークショップコンテンツ

- Splunk Observability ワークショップ教材をダウンロードします
- ワークショップトークンを使ってKubernetesシークレットをセットアップします
- プライベートコンテナレジストリを設定します
- デモアプリケーションとコンテンツを準備します

### VMの仕様

- **OS**: Ubuntu 24.04 LTS (Noble)
- **Memory**: 16GB RAM
- **CPU**: 4コア
- **Disk**: 40GB (拡張可能)
- **User**: `splunk` / `Splunk123!`
- **SSH**: パスワード認証が有効

### 環境変数

スクリプトはVM内で以下の環境変数を設定します:

- `RUM_TOKEN`: Real User Monitoringトークン
- `ACCESS_TOKEN`: データインジェストトークン
- `API_TOKEN`: Splunk APIトークン
- `HEC_TOKEN`: HTTP Event Collectorトークン
- `HEC_URL`: HECエンドポイントURL
- `REALM`: Splunk realm
- `INSTANCE`: 一意のホスト名
- `CLUSTER_NAME`: Kubernetesクラスター名

### VMへのアクセス

1. VMの作成と起動が完了するまで待ちます (5〜10分)
2. ProxmoxコンソールまたはDHCPログでVMのIPアドレスを確認します
3. VMにSSH接続します:

   ```bash
   ssh splunk@<vm-ip>
   # Password: Splunk123!
   ```

### VM内で便利なコマンド

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

- **Invalid SWiPE ID**: ワークショップの登録内容とIDを確認してください
- **VM creation fails**: Proxmoxのストレージ容量と権限を確認してください
- **Network issues**: `vmbr0` ブリッジが正しく設定されていることを確認してください
- **Slow deployment**: cloud-initがすべてのインストールを完了するために十分な時間を確保してください

### タグ

作成されたVMには以下のタグが付与されます: `o11y-workshop`、`noble`、`k3d`
