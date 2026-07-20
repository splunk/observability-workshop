---
title: デプロイメントワークフロー
weight: 4
time: 15 minutes
---

## 初回デプロイメント

パイプラインの設定が完了したので、最初のSmart Agentデプロイメントを実行する手順を確認します。

### ステップ1: パイプラインに移動

1. **Jenkins Dashboard** に移動します
2. **Deploy-Smart-Agent** パイプラインをクリックします

### ステップ2: パラメータ付きビルド

1. 左サイドバーの **Build with Parameters** をクリックします
2. デフォルトパラメータを確認します
   - **SMARTAGENT_ZIP_PATH**: パスが正しいことを確認します
   - **REMOTE_INSTALL_DIR**: `/opt/appdynamics/appdsmartagent`
   - **APPD_USER**: `ubuntu`（またはSSHユーザー）
   - **APPD_GROUP**: `ubuntu`
   - **SSH_PORT**: `22`
   - **AGENT_NAME**: `smartagent`
   - **LOG_LEVEL**: `DEBUG`

3. 必要に応じてパラメータを調整します
4. **Build** をクリックします

{{% notice style="tip" %}}
初回デプロイメントでは、IPアドレスを1つだけ含む別のクレデンシャルを作成して、単一ホストでテストすることを検討してください。
{{% /notice %}}

### ステップ3: パイプライン実行のモニタリング

**Build** をクリックすると、以下が表示されます

1. **Build added to queue** - Build Historyにビルド番号が表示されます
2. **ビルド番号をクリック**（例: #1）して詳細を表示します
3. **Console Output** をクリックしてリアルタイムログを表示します

### ステップ4: コンソール出力の理解

コンソール出力にはデプロイメントの各ステージが表示されます

```
Started by user admin
Running in Durability level: MAX_SURVIVABILITY
[Pipeline] Start of Pipeline
[Pipeline] node
Running on aws-vpc-agent in /home/ubuntu/jenkins/workspace/Deploy-Smart-Agent
[Pipeline] {
[Pipeline] stage
[Pipeline] { (Preparation)
[Pipeline] script
[Pipeline] {
Preparing Smart Agent deployment to 3 hosts: 172.31.1.243, 172.31.1.48, 172.31.1.5
...
```

表示される主要なステージは以下の通りです

1. ✅ **Preparation** - ホストリストの読み込みと検証
2. ✅ **Extract Smart Agent** - ZIPファイルの展開
3. ✅ **Configure Smart Agent** - config.iniの作成
4. ✅ **Deploy to Remote Hosts** - 各ホストへのデプロイ
5. ✅ **Verify Installation** - Smart Agentステータスの確認

### ステップ5: 結果の確認

完了後、以下が表示されます

**成功:**

```
Smart Agent successfully deployed to all hosts
Finished: SUCCESS
```

**部分的な成功:**

```
Deployment completed with some failures
Failed hosts: 172.31.1.48
Finished: UNSTABLE
```

**失敗:**

```
Smart Agent deployment failed. Check logs for details.
Finished: FAILURE
```

## インストールの検証

デプロイメントが成功した後、ターゲットホストでSmart Agentが実行されていることを確認します。

### Smart Agentステータスの確認

ターゲットホストにSSHで接続してステータスを確認します

```bash
# SSH to target host
ssh ubuntu@172.31.1.243

# Navigate to installation directory
cd /opt/appdynamics/appdsmartagent

# Check Smart Agent status
sudo ./smartagentctl status
```

**期待される出力:**

```
Smart Agent is running (PID: 12345)
Service: appdsmartagent.service
Status: active (running)
```

### インストール済みエージェントの一覧

```bash
cd /opt/appdynamics/appdsmartagent
sudo ./smartagentctl list
```

**期待される出力:**

```
No agents currently installed
(Use install-machine-agent or install-db-agent pipelines to add agents)
```

### ログの確認

```bash
cd /opt/appdynamics/appdsmartagent
tail -f log.log
```

AppDynamics Controllerへの接続成功メッセージを確認します。

### AppDynamics Controllerでの確認

1. AppDynamics Controllerにログインします
2. **Servers → Servers** に移動します
3. 新しくデプロイされたホストを確認します
4. Smart AgentがMetricを報告していることを確認します

## 追加エージェントのインストール

Smart Agentがデプロイされた後、他のパイプラインを使用して特定のエージェントタイプをインストールできます。

### Machine Agentのインストール

1. **Install-Machine-Agent** パイプラインに移動します
2. **Build with Parameters** をクリックします
3. パラメータを確認します
   - **AGENT_NAME**: `machine-agent`
   - **SSH_PORT**: `22`
4. **Build** をクリックします

パイプラインは各ホストにSSHで接続し、以下を実行します

```bash
cd /opt/appdynamics/appdsmartagent
sudo ./smartagentctl install --component machine
```

### Database Agentのインストール

1. **Install-Database-Agent** パイプラインに移動します
2. **Build with Parameters** をクリックします
3. データベース接続パラメータを設定します
4. **Build** をクリックします

パイプラインはすべてのホストにDatabase Agentをインストールし、設定します。

### エージェントインストールの検証

エージェントのインストール後、表示されることを確認します

```bash
cd /opt/appdynamics/appdsmartagent
sudo ./smartagentctl list
```

**期待される出力:**

```
Installed agents:
- machine-agent (running)
- db-agent (running)
```

## 一般的なデプロイメントシナリオ

### シナリオ1: 初期デプロイメント

**ワークフロー:**

1. **Deploy-Smart-Agent** パイプラインを実行します
2. 完了を待って検証します
3. 必要に応じて **Install-Machine-Agent** を実行します
4. 必要に応じて **Install-Database-Agent** を実行します

### シナリオ2: Smart Agentの更新

Smart Agentを新しいバージョンに更新するには

1. 新しいSmart Agent ZIPをダウンロードします
2. Jenkinsの設定済みパスに配置します
3. **Deploy-Smart-Agent** パイプラインを再度実行します

パイプラインは自動的に以下を行います

- 既存のSmart Agentを停止
- 古いファイルを削除
- 新しいバージョンをインストール
- Smart Agentを再起動

### シナリオ3: 新しいホストの追加

新しいホストにSmart Agentを追加するには

1. Jenkinsの `deployment-hosts` クレデンシャルを更新します
2. 新しいIPアドレスを追加します（1行に1つ）
3. **Deploy-Smart-Agent** パイプラインを実行します

パイプラインは以下を行います

- 設定済みのホストをスキップ（べき等の場合）
- 新しいホストにのみデプロイ

### シナリオ4: 完全な削除

すべてのホストからSmart Agentを完全に削除するには

1. **Cleanup-All-Agents** パイプラインに移動します
2. **Build with Parameters** をクリックします
3. `CONFIRM_CLEANUP` チェックボックスを **チェック** します
4. **Build** をクリックします

{{% notice style="danger" %}}
これにより、すべてのホストから `/opt/appdynamics/appdsmartagent` ディレクトリが完全に削除されます。この操作は元に戻せません。
{{% /notice %}}

## デプロイメントのトラブルシューティング

### Preparationステージでビルドが失敗する

**症状**: ホストリストの読み込み時にパイプラインが失敗する

**原因**: `deployment-hosts` クレデンシャルが存在しないか、正しくない

**解決策**:

1. **Manage Jenkins → Credentials** に移動します
2. `deployment-hosts` クレデンシャルが存在することを確認します
3. フォーマットを確認します（1行に1つのIP、カンマなし）
4. 末尾にスペースがないことを確認します

### SSH接続の失敗

**症状**: "Permission denied"または"Connection refused"エラー

**解決策**:

**セキュリティグループの確認:**

```bash
# Verify Jenkins agent can reach target
ping 172.31.1.243
telnet 172.31.1.243 22
```

**手動でSSHをテスト:**

```bash
# From Jenkins agent machine
ssh -i /path/to/key ubuntu@172.31.1.243
```

**SSHキーの確認:**

1. `ssh-private-key` クレデンシャルが正しいことを確認します
2. ターゲットホストの `~/.ssh/authorized_keys` に公開鍵があることを確認します

### Smart Agentが起動しない

**症状**: デプロイメントは完了するがSmart Agentが実行されていない

**解決策**:

**ターゲットホストのログを確認:**

```bash
cd /opt/appdynamics/appdsmartagent
cat log.log
```

**よくある問題:**

- **無効なアクセスキー**: `account-access-key` クレデンシャルを確認します
- **ネットワーク接続**: ControllerへのアウトバウンドHTTPSを確認します
- **権限の問題**: APPD_USERが正しい権限を持っていることを確認します

### 部分的なデプロイメント成功

**症状**: 一部のホストは成功し、他は失敗する

**解決策**:

1. **Console Output** を確認 - どのホストが失敗したかを特定します
2. **失敗したホストを調査** - SSHで接続して手動でテストします
3. **パイプラインを再実行** - Jenkinsがリトライが必要なホストを追跡します

## パイプラインのベストプラクティス

### 1. まず単一ホストでテスト

本番環境にデプロイする前に、常に単一ホストで新しい設定をテストします

```
1. Create deployment-hosts-test credential (1 IP)
2. Create test pipeline pointing to this credential
3. Verify success
4. Deploy to full host list
```

### 2. わかりやすいビルド説明を使用

ビルドをトリガーした後、説明を追加します

1. ビルドページに移動します
2. **Edit Build Information** をクリックします
3. 説明を追加します: "Production deployment - Q4 2024"

### 3. ビルド履歴のモニタリング

定期的にビルド履歴でパターンを確認します

- 失敗したビルド
- 所要時間の傾向
- エラーメッセージ

### 4. メンテナンスウィンドウ中にデプロイをスケジュール

本番システムの場合

- Jenkinsのスケジュールビルドを使用します
- トラフィックの少ない時間帯にデプロイします
- ロールバック計画を準備します

### 5. クレデンシャルを最新の状態に保つ

- SSHキーを四半期ごとにローテーションします
- インフラストラクチャの変更に応じてホストリストを更新します
- AppDynamicsアクセスキーの有効性を確認します

## 次のステップ

大規模デプロイメントのスケーリングと運用上の考慮事項を確認します。
