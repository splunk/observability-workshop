---
title: Jenkinsセットアップ
weight: 2
time: 10 minutes
---

## 前提条件

開始する前に、以下を準備してください。

- Jenkinsサーバー（バージョン2.300以降）
- ターゲットEC2インスタンスと同じAWS VPCにあるJenkinsエージェント
- ターゲットホストへの認証用SSHキーペア
- AppDynamics Smart Agentパッケージ
- SSHアクセス可能なターゲットUbuntu EC2インスタンス

## 必要なJenkinsプラグイン

**Manage Jenkins → Plugins → Available Plugins** からこれらのプラグインをインストールします。

1. **Pipeline**（コアプラグイン、通常プリインストール済み）
2. **SSH Agent Plugin**
3. **Credentials Plugin**（通常プリインストール済み）
4. **Git Plugin**（SCMを使用する場合）

インストール手順:

1. **Manage Jenkins → Plugins** に移動します
2. **Available** タブをクリックします
3. 各プラグインを検索します
4. 選択して **Install** をクリックします

## Jenkinsエージェントの設定

JenkinsエージェントがプライベートIPでターゲットEC2インスタンスに到達できる必要があります。主に2つのオプションがあります。

### オプションA: EC2インスタンスをエージェントとして使用

1. ターゲットホストと **同じVPCにEC2インスタンスを起動** します

2. **Javaをインストール** します（Jenkinsに必要）:

   ```bash
   sudo apt-get update
   sudo apt-get install -y openjdk-11-jdk
   ```

3. **Jenkinsにエージェントを追加** します:
   - **Manage Jenkins → Nodes → New Node** に移動します
   - 名前: `aws-vpc-agent`（任意の名前）
   - タイプ: **Permanent Agent**
   - 設定:
     - **Remote root directory**: `/home/ubuntu/jenkins`
     - **Labels**: `linux`（パイプラインのエージェントラベルと一致させる必要があります）
     - **Launch method**: Launch agent via SSH
     - **Host**: EC2プライベートIP
     - **Credentials**: エージェント用のSSH認証情報を追加

### オプションB: 既存のLinuxエージェントを使用

- エージェントに `linux` ラベルがあることを確認します
- ターゲットホストへのネットワーク接続性を確認します
- SSHクライアントがインストールされていることを確認します

### エージェントラベルの設定

{{% notice style="warning" %}}
このワークショップのすべてのパイプラインは `linux` ラベルを使用します。エージェントにこのラベルが設定されていることを確認してください。
{{% /notice %}}

ラベルを設定または変更するには:

1. **Manage Jenkins → Nodes** に移動します
2. エージェントをクリックします
3. **Configure** をクリックします
4. **Labels** を `linux` に設定します
5. **Save** をクリックします

## 認証情報のセットアップ

**Manage Jenkins → Credentials → System → Global credentials (unrestricted)** に移動します。

パイプラインを動作させるために、3つの認証情報を作成する必要があります。

### 1. ターゲットホスト用SSHプライベートキー

この認証情報により、JenkinsがターゲットEC2インスタンスにSSH接続できるようになります。

**Type**: SSH Username with private key

- **ID**: `ssh-private-key`（正確に一致させる必要があります）
- **Description**: `SSH key for EC2 target hosts`
- **Username**: `ubuntu`（またはSSHユーザー名）
- **Private Key**: 以下のいずれかを選択します:
  - **Enter directly**: PEMファイルの内容を貼り付けます
  - **From file**: PEMファイルをアップロードします
  - **From Jenkins master**: パスを指定します

**フォーマット例**:

```
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA...
...
-----END RSA PRIVATE KEY-----
```

### 2. デプロイメントホストリスト

この認証情報には、Smart Agentをデプロイするすべてのターゲットホストのリストが含まれます。

**Type**: Secret text

- **ID**: `deployment-hosts`（正確に一致させる必要があります）
- **Description**: `List of target EC2 host IPs`
- **Secret**: 改行区切りのIPを入力します

**例**:

```
172.31.1.243
172.31.1.48
172.31.1.5
172.31.10.20
172.31.10.21
```

{{% notice style="important" %}}
**フォーマット要件:**

- 1行に1つのIP
- カンマなし
- スペースなし
- 余分な文字なし
- Unix改行コード（LF、CRLFではない）を使用
{{% /notice %}}

### 3. AppDynamicsアカウントアクセスキー

この認証情報には、Smart Agent認証用のAppDynamicsアカウントアクセスキーが含まれます。

**Type**: Secret text

- **ID**: `account-access-key`（正確に一致させる必要があります）
- **Description**: `AppDynamics account access key`
- **Secret**: AppDynamicsアクセスキー

**例**: `abcd1234-ef56-7890-gh12-ijklmnopqrst`

{{% notice style="tip" %}}
AppDynamicsアクセスキーは、Controllerの **Settings → License → Account** で確認できます。
{{% /notice %}}

## 認証情報のセキュリティベストプラクティス

認証情報管理のベストプラクティスに従ってください。

- ✅ Jenkinsの認証情報暗号化を使用する（組み込み機能）
- ✅ Jenkinsのロールベース認可でアクセスを制限する
- ✅ SSHキーを定期的にローテーションする
- ✅ EC2インスタンスに最小権限のIAMロールを使用する
- ✅ 認証情報アクセスの監査ログを有効にする
- ✅ 認証情報をバージョン管理にコミットしない

## Smart Agentパッケージのセットアップ

Smart AgentのZIPファイルは、Jenkinsがアクセスできる場所に配置する必要があります。推奨されるアプローチは、Jenkinsホームディレクトリに保存することです。

### Smart Agentのダウンロード

```bash
# Download from AppDynamics
curl -o appdsmartagent_64_linux.zip \
  "https://download.appdynamics.com/download/prox/download-file/smart-agent/latest/appdsmartagent_64_linux.zip"

# Verify the download
ls -lh appdsmartagent_64_linux.zip
```

### 保存場所

パイプラインはSmart Agent ZIPを以下のパスで参照します: `/var/jenkins_home/smartagent/appdsmartagent.zip`

以下のいずれかを選択できます:

1. ZIPファイルをこの正確な場所に配置する
2. パイプラインパラメータ `SMARTAGENT_ZIP_PATH` をZIPファイルの場所に変更する

## 設定の確認

パイプラインの作成に進む前に、セットアップを確認します。

### 1. エージェントのステータス確認

1. **Manage Jenkins → Nodes** に移動します
2. エージェントが「online」と表示されていることを確認します
3. ラベルが `linux` に設定されていることを確認します

### 2. SSH接続のテスト

SSHが動作することを確認するための簡単なテストパイプラインを作成します:

```groovy
pipeline {
    agent { label 'linux' }
    stages {
        stage('Test SSH') {
            steps {
                withCredentials([
                    sshUserPrivateKey(credentialsId: 'ssh-private-key', 
                                     keyFileVariable: 'SSH_KEY', 
                                     usernameVariable: 'SSH_USER'),
                    string(credentialsId: 'deployment-hosts', variable: 'HOSTS')
                ]) {
                    sh '''
                        echo "Testing SSH credentials..."
                        echo "$HOSTS" | head -1 | while read HOST; do
                            ssh -i $SSH_KEY \
                                -o StrictHostKeyChecking=no \
                                -o ConnectTimeout=10 \
                                $SSH_USER@$HOST \
                                "echo 'Connection successful'"
                        done
                    '''
                }
            }
        }
    }
}
```

### 3. 認証情報の存在確認

1. **Manage Jenkins → Credentials** に移動します
2. 3つの認証情報がすべてリストされていることを確認します:
   - `ssh-private-key`
   - `deployment-hosts`
   - `account-access-key`

## よくある問題のトラブルシューティング

### エージェントが利用できない

**症状**: パイプライン実行時に「No agent available」エラーが発生する

**解決策**:

- **Manage Jenkins → Nodes** を確認します
- エージェントがオンラインであることを確認します
- エージェントに `linux` ラベルがあることを確認します
- エージェントの接続性をテストします

### SSH接続の失敗

**症状**: SSHでターゲットホストに接続できない

**解決策**:

```bash
# Test from Jenkins agent machine
ssh -i /path/to/key ubuntu@172.31.1.243 -o ConnectTimeout=10

# Check security group allows SSH from agent
# Verify private key matches public key on target
```

### 認証情報が見つからない

**症状**: 「Credential not found」エラーが発生する

**解決策**:

- 認証情報IDが正確に一致していることを確認します:
  - `ssh-private-key`
  - `deployment-hosts`
  - `account-access-key`
- 認証情報のスコープが **Global** に設定されていることを確認します

### ターゲットホストでの権限拒否

**症状**: SSH接続は成功するが、コマンドが権限拒否で失敗する

**解決策**:

```bash
# On target host, verify user is in sudoers
sudo visudo
# Add line:
ubuntu ALL=(ALL) NOPASSWD: ALL
```

## 次のステップ

Jenkinsの認証情報とエージェントの設定が完了しました。デプロイメントパイプラインの作成に進みましょう。
