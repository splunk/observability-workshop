---
title: GitHub Setup
weight: 2
time: 10 minutes
---

## 前提条件

開始する前に、以下を準備していることを確認してください。

- リポジトリアクセス権限のある GitHub アカウント
- Ubuntu EC2 インスタンスを含む AWS VPC
- ターゲットホストへの認証用 SSH キーペア（PEM ファイル）
- AppDynamics Smart Agent パッケージ
- SSH アクセス可能なターゲット Ubuntu EC2 インスタンス

## リポジトリの Fork または Clone

最初に、GitHub Actions ラボリポジトリへのアクセスを取得します。

**Repository URL**: [https://github.com/chambear2809/github-actions-lab](https://github.com/chambear2809/github-actions-lab)

```bash
# Option 1: Fork the repository via GitHub UI
# Go to https://github.com/chambear2809/github-actions-lab
# Click "Fork" button

# Option 2: Clone directly (for testing)
git clone https://github.com/chambear2809/github-actions-lab.git
cd github-actions-lab
```

## セルフホストランナーの構成

セルフホストランナーは、ターゲット EC2 インスタンスと同じ AWS VPC にデプロイする必要があります。

### EC2 インスタンスへのランナーのインストール

1. VPC 内に **EC2 インスタンスを起動** します（Ubuntu または Amazon Linux 2）

2. Fork したリポジトリで **ランナー設定に移動** します:

   ```
   Settings → Actions → Runners → New self-hosted runner
   ```

3. **ランナーインスタンスに SSH 接続** し、インストールコマンドを実行します:

```bash
# Create runner directory
mkdir actions-runner && cd actions-runner

# Download runner (check GitHub for latest version)
curl -o actions-runner-linux-x64-2.311.0.tar.gz -L \
  https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz

# Extract
tar xzf ./actions-runner-linux-x64-2.311.0.tar.gz

# Configure (use token from GitHub UI)
./config.sh --url https://github.com/YOUR_USERNAME/github-actions-lab --token YOUR_TOKEN

# Install as service
sudo ./svc.sh install

# Start service
sudo ./svc.sh start
```

### ランナーステータスの確認

以下の場所でランナーが **"Idle"**（緑色）として表示されていることを確認します:

```
Settings → Actions → Runners
```

{{% notice style="tip" %}}
ワークフロージョブを取得するには、ランナーがオンラインかつアイドル状態を維持している必要があります。オフラインと表示されている場合は、サービスステータスを確認してください: `sudo ./svc.sh status`
{{% /notice %}}

## GitHub Secrets の構成

以下に移動します: **Settings → Secrets and variables → Actions → Secrets**

### SSH Private Key Secret

このシークレットには、ターゲットホストにアクセスするための SSH 秘密鍵が含まれます。

1. **"New repository secret"** をクリックします
2. **Name**: `SSH_PRIVATE_KEY`
3. **Value**: PEM ファイルの内容を貼り付けます

```bash
# View your PEM file
cat /path/to/your-key.pem
```

形式の例:

```
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA...
...
-----END RSA PRIVATE KEY-----
```

1. **"Add secret"** をクリックします

{{% notice style="important" %}}
SSH キーをリポジトリにコミットしないでください。機密性の高い認証情報には常に GitHub Secrets を使用してください。
{{% /notice %}}

## GitHub Variables の構成

以下に移動します: **Settings → Secrets and variables → Actions → Variables**

### Deployment Hosts Variable（必須）

この変数には、Smart Agent をデプロイするすべてのターゲットホストのリストが含まれます。

1. **"New repository variable"** をクリックします
2. **Name**: `DEPLOYMENT_HOSTS`
3. **Value**: ターゲットホストの IP を入力します（1 行に 1 つ）

```
172.31.1.243
172.31.1.48
172.31.1.5
172.31.10.20
172.31.10.21
```

**形式の要件:**

- 1 行に 1 つの IP
- カンマなし
- スペースなし
- 余計な文字なし
- Unix 改行コードを使用（CRLF ではなく LF）

1. **"Add variable"** をクリックします

### オプション変数

これらの変数はオプションで、Smart Agent サービスのユーザー/グループ構成に使用されます。

#### SMARTAGENT_USER

1. **"New repository variable"** をクリックします
2. **Name**: `SMARTAGENT_USER`
3. **Value**: 例: `appdynamics`
4. **"Add variable"** をクリックします

#### SMARTAGENT_GROUP

1. **"New repository variable"** をクリックします
2. **Name**: `SMARTAGENT_GROUP`
3. **Value**: 例: `appdynamics`
4. **"Add variable"** をクリックします

## ネットワーク構成

すべての EC2 インスタンスを同じ VPC およびセキュリティグループに配置するラボセットアップでは、以下の構成を行います。

### セキュリティグループルール

**インバウンドルール:**

- 同じセキュリティグループからの SSH（ポート 22）（送信元: 同じ SG）

**アウトバウンドルール:**

- 0.0.0.0/0 への HTTPS（ポート 443）（GitHub API アクセス用）
- 同じセキュリティグループへの SSH（ポート 22）（ターゲットアクセス用）

### ネットワークのベストプラクティス

- ✅ `DEPLOYMENT_HOSTS` にはプライベート IP アドレス（172.31.x.x）を使用する
- ✅ ランナーとターゲットを同じセキュリティグループに配置する
- ✅ ターゲットホストにパブリック IP は不要
- ✅ ランナーはプライベートネットワーク経由で通信する
- ✅ GitHub ポーリングのためにアウトバウンド HTTPS が必要

## 構成の確認

ワークフローを実行する前に、セットアップを確認します。

### 1. ランナーステータスの確認

1. **Settings → Actions → Runners** に移動します
2. ランナーが "Idle"（緑色）として表示されることを確認します
3. "Last seen" のタイムスタンプが最近のものであることを確認します

### 2. SSH 接続のテスト

ランナーインスタンスからターゲットホストへ SSH 接続します:

```bash
# On runner instance
ssh -i ~/.ssh/your-key.pem ubuntu@172.31.1.243
```

成功した場合、ターゲットホスト上のシェルプロンプトが表示されます。

### 3. Secrets と Variables の確認

1. **Settings → Secrets and variables → Actions** に移動します
2. Secrets タブに `SSH_PRIVATE_KEY` が表示されることを確認します
3. Variables タブに `DEPLOYMENT_HOSTS` が表示されることを確認します

### 4. リポジトリアクセスの確認

ランナーがリポジトリにアクセスできることを確認します:

```bash
# On runner instance, as the runner user
cd ~/actions-runner
./run.sh  # Test run (Ctrl+C to stop)
```

"Listening for Jobs" と表示されるはずです。

## よくある問題のトラブルシューティング

### ランナーがジョブを取得しない

**症状**: ワークフローが "queued" 状態のままになる

**解決策**:

- ランナーのステータスを確認する: `sudo systemctl status actions.runner.*`
- ランナーを再起動する: `sudo ./svc.sh restart`
- GitHub への HTTPS（443）アウトバウンド接続を確認する

### SSH 接続の失敗

**症状**: ワークフローが "Permission denied" または "Connection refused" で失敗する

**解決策**:

```bash
# Test from runner
ssh -i ~/.ssh/test-key.pem ubuntu@172.31.1.243 -o ConnectTimeout=10

# Check security group allows SSH from runner
# Verify private key matches public key on targets
```

### ホスト名に無効な文字が含まれる

**症状**: エラー: "hostname contains invalid characters"

**解決策**:

- `DEPLOYMENT_HOSTS` 変数を編集する
- 末尾のスペースがないことを確認する
- Unix 改行コードを使用する（CRLF ではなく LF）
- 1 行に 1 つの IP、余計な文字を入れない

### Secrets が見つからない

**症状**: エラー: "Secret SSH_PRIVATE_KEY not found"

**解決策**:

- シークレット名が `SSH_PRIVATE_KEY` と完全に一致することを確認する
- シークレットがリポジトリ Secrets（環境シークレットではなく）にあることを確認する
- リポジトリの管理者権限があることを確認する

## セキュリティのベストプラクティス

セキュアな運用のために以下のベストプラクティスに従ってください。

- ✅ すべての秘密鍵に GitHub Secrets を使用する
- ✅ SSH キーを定期的にローテーションする
- ✅ ランナーをプライベート VPC サブネット内に配置する
- ✅ ランナーのセキュリティグループのアクセスを最小限に制限する
- ✅ ランナーのソフトウェアを定期的に更新する
- ✅ ブランチ保護ルールを有効化する
- ✅ 環境ごとに異なるキーを使用する
- ✅ リポジトリアクセスの監査ログを有効化する

## 次のステップ

GitHub の構成とランナーのセットアップが完了したので、利用可能なワークフローを確認し、最初のデプロイを実行する準備が整いました。
