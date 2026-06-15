---
title: GitHub Setup
weight: 2
time: 10 minutes
---

## 前提条件

始める前に、以下が準備されていることを確認してください

- リポジトリアクセス権を持つ GitHub アカウント
- Ubuntu EC2 インスタンスを持つ AWS VPC
- ターゲットホストへの認証用 SSH キーペア（PEM ファイル）
- AppDynamics Smart Agent パッケージ
- SSH アクセスが可能なターゲット Ubuntu EC2 インスタンス

## リポジトリのフォークまたはクローン

まず、GitHub Actions ラボリポジトリへのアクセスを取得します

**リポジトリ URL**: [https://github.com/chambear2809/github-actions-lab](https://github.com/chambear2809/github-actions-lab)

```bash
# Option 1: Fork the repository via GitHub UI
# Go to https://github.com/chambear2809/github-actions-lab
# Click "Fork" button

# Option 2: Clone directly (for testing)
git clone https://github.com/chambear2809/github-actions-lab.git
cd github-actions-lab
```

## セルフホストランナーの設定

セルフホストランナーは、ターゲット EC2 インスタンスと同じ AWS VPC にデプロイする必要があります。

### EC2 インスタンスへのランナーのインストール

1. **EC2 インスタンスを起動します**（VPC 内に Ubuntu または Amazon Linux 2）

2. フォークしたリポジトリで**ランナー設定に移動します**

   ```
   Settings → Actions → Runners → New self-hosted runner
   ```

3. **ランナーインスタンスに SSH 接続し**、インストールコマンドを実行します

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

ランナーが以下の場所で **"Idle"**（緑色）と表示されていることを確認します

```
Settings → Actions → Runners
```

{{% notice style="tip" %}}
ランナーはワークフロージョブを受け取るために、オンラインかつアイドル状態を維持する必要があります。オフラインと表示される場合は、サービスステータスを確認してください`sudo ./svc.sh status`
{{% /notice %}}

## GitHub Secrets の設定

移動先: **Settings → Secrets and variables → Actions → Secrets**

### SSH 秘密鍵シークレット

このシークレットには、ターゲットホストにアクセスするための SSH 秘密鍵が含まれます。

1. **"New repository secret"** をクリックします
2. **Name**: `SSH_PRIVATE_KEY`
3. **Value**: PEM ファイルの内容を貼り付けます

```bash
# View your PEM file
cat /path/to/your-key.pem
```

フォーマット例

```
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA...
...
-----END RSA PRIVATE KEY-----
```

1. **"Add secret"** をクリックします

{{% notice style="important" %}}
SSH キーをリポジトリにコミットしないでください！機密性の高い認証情報には必ず GitHub Secrets を使用してください。
{{% /notice %}}

## GitHub Variables の設定

移動先: **Settings → Secrets and variables → Actions → Variables**

### デプロイメントホスト変数（必須）

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

**フォーマット要件**

- 1 行に 1 つの IP
- カンマなし
- スペースなし
- 余分な文字なし
- Unix 改行コード（LF、CRLF ではない）を使用

1. **"Add variable"** をクリックします

### オプション変数

これらの変数はオプションで、Smart Agent サービスのユーザー/グループ設定に使用されます

#### SMARTAGENT_USER

1. **"New repository variable"** をクリックします
2. **Name**: `SMARTAGENT_USER`
3. **Value**: 例`appdynamics`
4. **"Add variable"** をクリックします

#### SMARTAGENT_GROUP

1. **"New repository variable"** をクリックします
2. **Name**: `SMARTAGENT_GROUP`
3. **Value**: 例`appdynamics`
4. **"Add variable"** をクリックします

## ネットワーク設定

すべての EC2 インスタンスが同じ VPC とセキュリティグループにあるラボセットアップの場合

### セキュリティグループルール

**インバウンドルール**

- SSH (port 22)：同じセキュリティグループから（ソース：同じ SG）

**アウトバウンドルール**

- HTTPS (port 443)：0.0.0.0/0 宛て（GitHub API アクセス用）
- SSH (port 22)：同じセキュリティグループ宛て（ターゲットアクセス用）

### ネットワークのベストプラクティス

- ✅ `DEPLOYMENT_HOSTS` にはプライベート IP アドレス（172.31.x.x）を使用します
- ✅ ランナーとターゲットを同じセキュリティグループに配置します
- ✅ ターゲットホストにパブリック IP は不要です
- ✅ ランナーはプライベートネットワーク経由で通信します
- ✅ GitHub ポーリングにはアウトバウンド HTTPS が必要です

## 設定の確認

ワークフローを実行する前に、セットアップを確認します

### 1. ランナーステータスの確認

1. **Settings → Actions → Runners** に移動します
2. ランナーが "Idle"（緑色）と表示されていることを確認します
3. "Last seen" のタイムスタンプが最近であることを確認します

### 2. SSH 接続のテスト

ランナーインスタンスからターゲットホストに SSH 接続します

```bash
# On runner instance
ssh -i ~/.ssh/your-key.pem ubuntu@172.31.1.243
```

成功すると、ターゲットホストのシェルプロンプトが表示されます。

### 3. Secrets と Variables の確認

1. **Settings → Secrets and variables → Actions** に移動します
2. Secrets タブに `SSH_PRIVATE_KEY` が表示されていることを確認します
3. Variables タブに `DEPLOYMENT_HOSTS` が表示されていることを確認します

### 4. リポジトリアクセスの確認

ランナーがリポジトリにアクセスできることを確認します

```bash
# On runner instance, as the runner user
cd ~/actions-runner
./run.sh  # Test run (Ctrl+C to stop)
```

"Listening for Jobs" と表示されるはずです。

## よくある問題のトラブルシューティング

### ランナーがジョブを受け取らない

**症状**: ワークフローが "queued" 状態のままになる

**解決策**:

- ランナーステータスを確認します`sudo systemctl status actions.runner.*`
- ランナーを再起動します`sudo ./svc.sh restart`
- GitHub へのアウトバウンド HTTPS (443) 接続を確認します

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

**症状**: エラー："hostname contains invalid characters"

**解決策**:

- `DEPLOYMENT_HOSTS` 変数を編集します
- 末尾のスペースがないことを確認します
- Unix 改行コード（LF、CRLF ではない）を使用します
- 1 行に 1 つの IP、余分な文字なし

### Secrets が見つからない

**症状**: エラー："Secret SSH_PRIVATE_KEY not found"

**解決策**:

- シークレット名が正確に一致していることを確認します`SSH_PRIVATE_KEY`
- シークレットがリポジトリシークレットにあることを確認します（環境シークレットではない）
- リポジトリの管理者アクセス権があることを確認します

## セキュリティのベストプラクティス

安全な運用のために、以下のベストプラクティスに従ってください

- ✅ すべての秘密鍵に GitHub Secrets を使用します
- ✅ SSH キーを定期的にローテーションします
- ✅ ランナーをプライベート VPC サブネットに配置します
- ✅ ランナーのセキュリティグループを最小限のアクセスに制限します
- ✅ ランナーソフトウェアを定期的に更新します
- ✅ ブランチ保護ルールを有効にします
- ✅ 異なる環境には別々のキーを使用します
- ✅ リポジトリアクセスの監査ログを有効にします

## 次のステップ

GitHub の設定とランナーのセットアップが完了したら、利用可能なワークフローを確認し、最初のデプロイメントを実行する準備が整いました！
