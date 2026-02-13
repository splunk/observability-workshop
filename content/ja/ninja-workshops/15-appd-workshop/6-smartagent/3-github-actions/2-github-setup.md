---
title: GitHub のセットアップ
weight: 2
time: 10 minutes
---

## 前提条件

開始する前に、以下を確認します:

- リポジトリアクセス権を持つ GitHub アカウント
- Ubuntu EC2 インスタンスを持つ AWS VPC
- ターゲットホストへの認証用 SSH キーペア（PEM ファイル）
- AppDynamics Smart Agent パッケージ
- SSH アクセス可能なターゲット Ubuntu EC2 インスタンス

## リポジトリのフォークまたはクローン

まず、GitHub Actions ラボリポジトリへのアクセスを取得します。

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

1. VPC 内で **EC2 インスタンスを起動** します（Ubuntu または Amazon Linux 2）

2. フォークしたリポジトリの **ランナー設定に移動** します:

   ```text
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

ランナーが以下の場所で **"Idle"**（緑色）と表示されていることを確認します:

```text
Settings → Actions → Runners
```

{{% notice style="tip" %}}
ランナーはワークフロージョブを受け取るためにオンラインかつアイドル状態を維持する必要があります。オフラインと表示される場合は、サービスステータスを確認します: `sudo ./svc.sh status`
{{% /notice %}}

## GitHub Secrets の設定

**Settings → Secrets and variables → Actions → Secrets** に移動します。

### SSH 秘密鍵の Secret

この Secret には、ターゲットホストにアクセスするための SSH 秘密鍵が含まれます。

1. **"New repository secret"** をクリックします
2. **Name**: `SSH_PRIVATE_KEY`
3. **Value**: PEM ファイルの内容を貼り付けます

```bash
# View your PEM file
cat /path/to/your-key.pem
```

フォーマット例:

```text
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA...
...
-----END RSA PRIVATE KEY-----
```

1. **"Add secret"** をクリックします

{{% notice style="important" %}}
SSH キーをリポジトリにコミットしないでください。機密性の高い認証情報には必ず GitHub Secrets を使用します。
{{% /notice %}}

## GitHub Variables の設定

**Settings → Secrets and variables → Actions → Variables** に移動します。

### デプロイホスト Variable（必須）

この Variable には、Smart Agent をデプロイするすべてのターゲットホストのリストが含まれます。

1. **"New repository variable"** をクリックします
2. **Name**: `DEPLOYMENT_HOSTS`
3. **Value**: ターゲットホストの IP を入力します（1行に1つ）

```text
172.31.1.243
172.31.1.48
172.31.1.5
172.31.10.20
172.31.10.21
```

**フォーマット要件:**

- 1行に1つの IP
- カンマなし
- スペースなし
- 余分な文字なし
- Unix 改行コード（LF、CRLF ではなく）を使用

1. **"Add variable"** をクリックします

### オプションの Variables

これらの Variable はオプションで、Smart Agent サービスのユーザー/グループ設定に使用されます:

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

## ネットワーク設定

同じ VPC およびセキュリティグループ内のすべての EC2 インスタンスを使用するラボセットアップの場合:

### セキュリティグループルール

**インバウンドルール:**

- 同じセキュリティグループからの SSH（ポート22）（ソース: 同じ SG）

**アウトバウンドルール:**

- 0.0.0.0/0 への HTTPS（ポート443）（GitHub API アクセス用）
- 同じセキュリティグループへの SSH（ポート22）（ターゲットアクセス用）

### ネットワークのベストプラクティス

- `DEPLOYMENT_HOSTS` にはプライベート IP アドレス（172.31.x.x）を使用
- ランナーとターゲットを同じセキュリティグループに配置
- ターゲットホストにパブリック IP は不要
- ランナーはプライベートネットワーク経由で通信
- GitHub ポーリング用のアウトバウンド HTTPS が必要

## 設定の確認

ワークフローを実行する前に、セットアップを確認します:

### 1. ランナーステータスの確認

1. **Settings → Actions → Runners** に移動します
2. ランナーが「Idle」（緑色）と表示されていることを確認します
3. 「Last seen」のタイムスタンプが最近であることを確認します

### 2. SSH 接続のテスト

ランナーインスタンスからターゲットホストに SSH 接続します:

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

ランナーがリポジトリにアクセスできることを確認します:

```bash
# On runner instance, as the runner user
cd ~/actions-runner
./run.sh  # Test run (Ctrl+C to stop)
```

「Listening for Jobs」と表示されます。

## よくある問題のトラブルシューティング

### ランナーがジョブを取得しない

**症状**: ワークフローが「queued」状態のまま

**解決策**:

- ランナーステータスを確認します: `sudo systemctl status actions.runner.*`
- ランナーを再起動します: `sudo ./svc.sh restart`
- GitHub へのアウトバウンド HTTPS（443）接続を確認します

### SSH 接続の失敗

**症状**: ワークフローが「Permission denied」または「Connection refused」で失敗

**解決策**:

```bash
# Test from runner
ssh -i ~/.ssh/test-key.pem ubuntu@172.31.1.243 -o ConnectTimeout=10

# Check security group allows SSH from runner
# Verify private key matches public key on targets
```

### ホスト名に無効な文字

**症状**: エラー「hostname contains invalid characters」

**解決策**:

- `DEPLOYMENT_HOSTS` Variable を編集します
- 末尾にスペースがないことを確認します
- Unix 改行コード（LF、CRLF ではなく）を使用します
- 1行に1つの IP、余分な文字なし

### Secrets が見つからない

**症状**: エラー「Secret SSH_PRIVATE_KEY not found」

**解決策**:

- Secret 名が正確に一致していることを確認します: `SSH_PRIVATE_KEY`
- Secret がリポジトリ Secrets（環境 Secrets ではなく）にあることを確認します
- リポジトリの管理者アクセス権があることを確認します

## セキュリティのベストプラクティス

安全な運用のために、以下のベストプラクティスに従います:

- すべての秘密鍵に GitHub Secrets を使用
- SSH キーを定期的にローテーション
- ランナーをプライベート VPC サブネットに配置
- ランナーのセキュリティグループを最小限のアクセスに制限
- ランナーソフトウェアを定期的にアップデート
- ブランチ保護ルールを有効化
- 環境ごとに別のキーを使用
- リポジトリアクセスの監査ログを有効化

## 次のステップ

GitHub の設定とランナーのセットアップが完了したら、利用可能なワークフローを確認し、最初のデプロイを実行しましょう。
