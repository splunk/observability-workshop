---
title: Jenkins セットアップ
weight: 2
time: 10 minutes
---

## 前提条件

開始する前に、以下が揃っていることを確認してください。

- Jenkins サーバー（バージョン 2.300 以降）
- ターゲット EC2 インスタンスと同じ AWS VPC 内にある Jenkins エージェント
- ターゲットホストへの認証用 SSH キーペア
- AppDynamics Smart Agent パッケージ
- SSH アクセス可能なターゲット Ubuntu EC2 インスタンス

## 必要な Jenkins プラグイン

**Manage Jenkins → Plugins → Available Plugins** から以下のプラグインをインストールします。

1. **Pipeline**（コアプラグイン、通常はプリインストール済み）
2. **SSH Agent Plugin**
3. **Credentials Plugin**（通常はプリインストール済み）
4. **Git Plugin**（SCM を使用する場合）

インストール手順は次のとおりです。

1. **Manage Jenkins → Plugins** に移動します
2. **Available** タブをクリックします
3. 各プラグインを検索します
4. 選択して **Install** をクリックします

## Jenkins エージェントの構成

Jenkins エージェントは、プライベート IP 経由でターゲット EC2 インスタンスに到達できる必要があります。主に 2 つのオプションがあります。

### オプション A: EC2 インスタンスをエージェントとして使用

1. **EC2 インスタンスをターゲットホストと同じ VPC 内で起動** します

2. **Java をインストール** します（Jenkins に必要）。

   ```bash
   sudo apt-get update
   sudo apt-get install -y openjdk-11-jdk
   ```

3. **Jenkins にエージェントを追加** します。
   - **Manage Jenkins → Nodes → New Node** に移動します
   - Name: `aws-vpc-agent`（または任意の名前）
   - Type: **Permanent Agent**
   - 設定:
     - **Remote root directory**: `/home/ubuntu/jenkins`
     - **Labels**: `linux`（パイプラインのエージェントラベルと一致させる必要があります）
     - **Launch method**: Launch agent via SSH
     - **Host**: EC2 のプライベート IP
     - **Credentials**: エージェント用の SSH 認証情報を追加します

### オプション B: 既存の Linux エージェントを使用

- エージェントに `linux` ラベルが付いていることを確認します
- ターゲットホストへのネットワーク接続を確認します
- SSH クライアントがインストールされていることを確認します

### エージェントラベルの構成

{{% notice style="warning" %}}
このワークショップのすべてのパイプラインは `linux` ラベルを使用します。エージェントがこのラベルで構成されていることを確認してください。
{{% /notice %}}

ラベルを設定または変更するには、次の手順に従います。

1. **Manage Jenkins → Nodes** に移動します
2. エージェントをクリックします
3. **Configure** をクリックします
4. **Labels** を `linux` に設定します
5. **Save** をクリックします

## 認証情報のセットアップ

**Manage Jenkins → Credentials → System → Global credentials (unrestricted)** に移動します。

パイプラインを動作させるために、3 つの認証情報を作成する必要があります。

### 1. ターゲットホスト用の SSH 秘密鍵

この認証情報により、Jenkins がターゲット EC2 インスタンスに SSH 接続できます。

**Type**: SSH Username with private key

- **ID**: `ssh-private-key`（完全に一致する必要があります）
- **Description**: `SSH key for EC2 target hosts`
- **Username**: `ubuntu`（または使用する SSH ユーザー）
- **Private Key**: 次のいずれかを選択します:
  - **Enter directly**: PEM ファイルの内容を貼り付けます
  - **From file**: PEM ファイルをアップロードします
  - **From Jenkins master**: パスを指定します

**フォーマット例**:

```
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA...
...
-----END RSA PRIVATE KEY-----
```

### 2. デプロイ先ホスト一覧

この認証情報には、Smart Agent をデプロイするすべてのターゲットホストの一覧が含まれます。

**Type**: Secret text

- **ID**: `deployment-hosts`（完全に一致する必要があります）
- **Description**: `List of target EC2 host IPs`
- **Secret**: 改行区切りの IP を入力します

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

- 1 行に 1 つの IP
- カンマなし
- スペースなし
- 余分な文字なし
- Unix 形式の改行コードを使用（CRLF ではなく LF）
{{% /notice %}}

### 3. AppDynamics アカウントアクセスキー

この認証情報には、Smart Agent 認証用の AppDynamics アカウントアクセスキーが含まれます。

**Type**: Secret text

- **ID**: `account-access-key`（完全に一致する必要があります）
- **Description**: `AppDynamics account access key`
- **Secret**: AppDynamics のアクセスキー

**例**: `abcd1234-ef56-7890-gh12-ijklmnopqrst`

{{% notice style="tip" %}}
AppDynamics のアクセスキーは、Controller の **Settings → License → Account** で確認できます。
{{% /notice %}}

## 認証情報のセキュリティに関するベストプラクティス

認証情報の管理にあたっては、以下のベストプラクティスに従ってください。

- ✅ Jenkins の認証情報暗号化（組み込み機能）を使用する
- ✅ Jenkins のロールベース認可によりアクセスを制限する
- ✅ SSH キーを定期的にローテーションする
- ✅ EC2 インスタンスには最小権限の IAM ロールを使用する
- ✅ 認証情報アクセスの監査ログを有効化する
- ✅ 認証情報をバージョン管理にコミットしない

## Smart Agent パッケージのセットアップ

Smart Agent の ZIP ファイルは、Jenkins からアクセス可能な場所に配置する必要があります。推奨されるアプローチは、Jenkins ホームディレクトリに保存することです。

### Smart Agent のダウンロード

```bash
# Download from AppDynamics
curl -o appdsmartagent_64_linux.zip \
  "https://download.appdynamics.com/download/prox/download-file/smart-agent/latest/appdsmartagent_64_linux.zip"

# Verify the download
ls -lh appdsmartagent_64_linux.zip
```

### 保存場所

パイプラインは、Smart Agent の ZIP を `/var/jenkins_home/smartagent/appdsmartagent.zip` で参照します。

次のいずれかを選択できます。

1. ZIP をこの正確な場所に配置する
2. `SMARTAGENT_ZIP_PATH` パイプラインパラメーターを変更して、ZIP の場所を指定する

## 構成の検証

パイプラインの作成に進む前に、セットアップを検証します。

### 1. エージェントのステータス確認

1. **Manage Jenkins → Nodes** に移動します
2. エージェントが「online」と表示されていることを確認します
3. ラベルが `linux` に設定されていることを確認します

### 2. SSH 接続のテスト

SSH が動作することを確認するために、シンプルなテストパイプラインを作成します。

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
2. 3 つの認証情報がすべてリストされていることを確認します:
   - `ssh-private-key`
   - `deployment-hosts`
   - `account-access-key`

## よくある問題のトラブルシューティング

### エージェントが利用できない

**症状**: パイプライン実行時に「No agent available」エラーが表示される

**解決策**:

- **Manage Jenkins → Nodes** を確認します
- エージェントがオンラインであることを確認します
- エージェントに `linux` ラベルが付いていることを確認します
- エージェントの接続性をテストします

### SSH 接続の失敗

**症状**: SSH 経由でターゲットホストに接続できない

**解決策**:

```bash
# Test from Jenkins agent machine
ssh -i /path/to/key ubuntu@172.31.1.243 -o ConnectTimeout=10

# Check security group allows SSH from agent
# Verify private key matches public key on target
```

### 認証情報が見つからない

**症状**: 「Credential not found」エラーが表示される

**解決策**:

- 認証情報の ID が完全に一致することを確認します:
  - `ssh-private-key`
  - `deployment-hosts`
  - `account-access-key`
- 認証情報のスコープが **Global** に設定されていることを確認します

### ターゲットホストでのパーミッション拒否

**症状**: SSH は成功するが、コマンドが permission denied で失敗する

**解決策**:

```bash
# On target host, verify user is in sudoers
sudo visudo
# Add line:
ubuntu ALL=(ALL) NOPASSWD: ALL
```

## 次のステップ

これで Jenkins に認証情報とエージェントが構成されたので、デプロイパイプラインを作成する準備が整いました。
