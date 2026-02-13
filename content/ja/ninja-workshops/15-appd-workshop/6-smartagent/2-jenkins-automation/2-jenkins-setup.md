---
title: Jenkins セットアップ
weight: 2
time: 10 minutes
---

## 前提条件

開始する前に、以下を準備してください:

- Jenkinsサーバー（バージョン2.300以降）
- ターゲットEC2インスタンスと同じAWS VPC内のJenkinsエージェント
- ターゲットホストへの認証用SSHキーペア
- AppDynamics Smart Agentパッケージ
- SSHアクセス可能なターゲットUbuntu EC2インスタンス

## 必要な Jenkins プラグイン

**Manage Jenkins → Plugins → Available Plugins** から以下のプラグインをインストールします:

1. **Pipeline**（コアプラグイン、通常はプリインストール済み）
2. **SSH Agent Plugin**
3. **Credentials Plugin**（通常はプリインストール済み）
4. **Git Plugin**（SCMを使用する場合）

インストール手順:

1. **Manage Jenkins → Plugins** に移動します
2. **Available** タブをクリックします
3. 各プラグインを検索します
4. 選択して **Install** をクリックします

## Jenkins Agent の設定

JenkinsエージェントはプライベートIP経由でターゲットEC2インスタンスに到達できる必要があります。主に2つの方法があります:

### オプション A: EC2 インスタンスをエージェントとして使用

1. ターゲットホストと **同じ VPC に EC2 インスタンスを起動** します

2. **Java をインストール** します（Jenkinsに必要）:

   ```bash
   sudo apt-get update
   sudo apt-get install -y openjdk-11-jdk
   ```

3. **Jenkins にエージェントを追加** します:
   - **Manage Jenkins → Nodes → New Node** に移動します
   - 名前: `aws-vpc-agent`（または任意の名前）
   - タイプ: **Permanent Agent**
   - 設定:
     - **Remote root directory**: `/home/ubuntu/jenkins`
     - **Labels**: `linux`（パイプラインのエージェントラベルと一致させる必要があります）
     - **Launch method**: Launch agent via SSH
     - **Host**: EC2のプライベートIP
     - **Credentials**: エージェント用のSSH認証情報を追加

### オプション B: 既存の Linux エージェントを使用

- エージェントに `linux` ラベルが設定されていることを確認します
- ターゲットホストへのネットワーク接続を確認します
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

### 1. ターゲットホスト用 SSH 秘密鍵

この認証情報により、JenkinsがターゲットEC2インスタンスにSSH接続できるようになります。

**Type**: SSH Username with private key

- **ID**: `ssh-private-key`（正確に一致させる必要があります）
- **Description**: `SSH key for EC2 target hosts`
- **Username**: `ubuntu`（または使用するSSHユーザー）
- **Private Key**: 以下のいずれかを選択:
  - **Enter directly**: PEMファイルの内容を貼り付け
  - **From file**: PEMファイルをアップロード
  - **From Jenkins master**: パスを指定

**フォーマット例**:

```text
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA...
...
-----END RSA PRIVATE KEY-----
```

### 2. デプロイ対象ホストリスト

この認証情報には、Smart Agentをデプロイするすべてのターゲットホストのリストが含まれます。

**Type**: Secret text

- **ID**: `deployment-hosts`（正確に一致させる必要があります）
- **Description**: `List of target EC2 host IPs`
- **Secret**: 改行区切りのIPアドレスを入力

**例**:

```text
172.31.1.243
172.31.1.48
172.31.1.5
172.31.10.20
172.31.10.21
```

{{% notice style="important" %}}
**フォーマット要件:**

- 1行に1つのIPアドレス
- カンマなし
- スペースなし
- 余分な文字なし
- Unix改行コード（LF、CRLFではない）を使用
{{% /notice %}}

### 3. AppDynamics アカウントアクセスキー

この認証情報には、Smart Agentの認証に使用するAppDynamicsアカウントアクセスキーが含まれます。

**Type**: Secret text

- **ID**: `account-access-key`（正確に一致させる必要があります）
- **Description**: `AppDynamics account access key`
- **Secret**: AppDynamicsのアクセスキー

**例**: `abcd1234-ef56-7890-gh12-ijklmnopqrst`

{{% notice style="tip" %}}
AppDynamicsのアクセスキーは、Controllerの **Settings → License → Account** で確認できます。
{{% /notice %}}

## 認証情報のセキュリティベストプラクティス

認証情報管理のベストプラクティスに従ってください:

- Jenkinsの認証情報暗号化を使用する（組み込み機能）
- Jenkinsのロールベース認可でアクセスを制限する
- SSH鍵を定期的にローテーションする
- EC2インスタンスに最小権限のIAMロールを使用する
- 認証情報アクセスの監査ログを有効にする
- 認証情報をバージョン管理にコミットしない

## Smart Agent パッケージのセットアップ

Smart AgentのZIPファイルは、Jenkinsからアクセス可能な場所に配置する必要があります。推奨される方法は、Jenkinsのホームディレクトリに保存することです。

### Smart Agent のダウンロード

```bash
# AppDynamics からダウンロード
curl -o appdsmartagent_64_linux.zip \
  "https://download.appdynamics.com/download/prox/download-file/smart-agent/latest/appdsmartagent_64_linux.zip"

# ダウンロードを確認
ls -lh appdsmartagent_64_linux.zip
```

### 保存場所

パイプラインはSmart Agent ZIPを `/var/jenkins_home/smartagent/appdsmartagent.zip` で参照します。

以下のいずれかの方法で対応できます:

1. この場所にZIPファイルを正確に配置する
2. パイプラインパラメータ `SMARTAGENT_ZIP_PATH` をZIPファイルの場所に変更する

## 設定の確認

パイプライン作成に進む前に、セットアップを確認します:

### 1. エージェントの状態確認

1. **Manage Jenkins → Nodes** に移動します
2. エージェントが「online」と表示されていることを確認します
3. ラベルが `linux` に設定されていることを確認します

### 2. SSH 接続のテスト

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
2. 以下の3つの認証情報がリストに表示されていることを確認します:
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
- エージェントの接続をテストします

### SSH 接続の失敗

**症状**: SSH経由でターゲットホストに接続できない

**解決策**:

```bash
# Jenkins エージェントマシンからテスト
ssh -i /path/to/key ubuntu@172.31.1.243 -o ConnectTimeout=10

# セキュリティグループがエージェントからの SSH を許可していることを確認
# 秘密鍵がターゲットの公開鍵と一致していることを確認
```

### 認証情報が見つからない

**症状**:「Credential not found」エラーが発生する

**解決策**:

- 認証情報のIDが正確に一致していることを確認します:
  - `ssh-private-key`
  - `deployment-hosts`
  - `account-access-key`
- 認証情報のスコープが **Global** に設定されていることを確認します

### ターゲットホストでの権限拒否

**症状**: SSHは成功するがコマンドが権限拒否で失敗する

**解決策**:

```bash
# ターゲットホストで、ユーザーが sudoers に含まれていることを確認
sudo visudo
# 以下の行を追加:
ubuntu ALL=(ALL) NOPASSWD: ALL
```

## 次のステップ

Jenkinsの認証情報とエージェントの設定が完了したら、デプロイパイプラインの作成に進みます。
