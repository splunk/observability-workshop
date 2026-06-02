---
title: デプロイメントワークフロー
weight: 4
time: 15 minutes
---

## 初回デプロイメント

パイプラインの設定が完了したので、初めての Smart Agent デプロイメントを実行する手順を説明します。

### Step 1: パイプラインへ移動する

1. **Jenkins Dashboard** に移動します
2. **Deploy-Smart-Agent** パイプラインをクリックします

### Step 2: パラメーター付きでビルドする

1. 左サイドバーの **Build with Parameters** をクリックします
2. デフォルトパラメーターを確認します:
   - **SMARTAGENT_ZIP_PATH**: パスが正しいか確認します
   - **REMOTE_INSTALL_DIR**: `/opt/appdynamics/appdsmartagent`
   - **APPD_USER**: `ubuntu` (または使用している SSH ユーザー)
   - **APPD_GROUP**: `ubuntu`
   - **SSH_PORT**: `22`
   - **AGENT_NAME**: `smartagent`
   - **LOG_LEVEL**: `DEBUG`

3. 必要に応じてパラメーターを調整します
4. **Build** をクリックします

{{% notice style="tip" %}}
初回デプロイメントでは、IP アドレスを1つだけ記載した別の認証情報を作成し、単一ホストでテストすることを検討してください。
{{% /notice %}}

### Step 3: パイプライン実行を監視する

**Build** をクリックすると、以下が表示されます:

1. **Build added to queue** - Build History にビルド番号が表示されます
2. **ビルド番号をクリック** (例: #1) して詳細を表示します
3. **Console Output をクリック** してリアルタイムのログを表示します

### Step 4: コンソール出力を理解する

コンソール出力にはデプロイメントの各ステージが表示されます:

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

表示される主なステージ:

1. ✅ **Preparation** - ホストリストを読み込み、検証します
2. ✅ **Extract Smart Agent** - ZIP ファイルを展開します
3. ✅ **Configure Smart Agent** - config.ini を作成します
4. ✅ **Deploy to Remote Hosts** - 各ホストへデプロイします
5. ✅ **Verify Installation** - Smart Agent のステータスを確認します

### Step 5: 結果を確認する

完了後、以下が表示されます:

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

デプロイメントが成功したら、対象ホストで Smart Agent が稼働していることを検証します。

### Smart Agent ステータスの確認

対象ホストへ SSH 接続し、ステータスを確認します:

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

### インストール済みエージェントの一覧表示

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

AppDynamics コントローラーへの接続成功メッセージを確認します。

### AppDynamics Controller での検証

1. AppDynamics Controller にログインします
2. **Servers → Servers** に移動します
3. 新しくデプロイされたホストを探します
4. Smart Agent がメトリクスを送信していることを確認します

## 追加エージェントのインストール

Smart Agent がデプロイされたら、他のパイプラインを使用して特定のエージェントタイプをインストールできます。

### Machine Agent のインストール

1. **Install-Machine-Agent** パイプラインへ移動します
2. **Build with Parameters** をクリックします
3. パラメーターを確認します:
   - **AGENT_NAME**: `machine-agent`
   - **SSH_PORT**: `22`
4. **Build** をクリックします

パイプラインは各ホストへ SSH 接続し、以下を実行します:

```bash
cd /opt/appdynamics/appdsmartagent
sudo ./smartagentctl install --component machine
```

### Database Agent のインストール

1. **Install-Database-Agent** パイプラインへ移動します
2. **Build with Parameters** をクリックします
3. データベース接続パラメーターを設定します
4. **Build** をクリックします

パイプラインは全ホストに Database Agent をインストールおよび設定します。

### エージェントインストールの検証

エージェントをインストール後、表示されることを検証します:

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

### シナリオ 1: 初回デプロイメント

**ワークフロー:**

1. **Deploy-Smart-Agent** パイプラインを実行します
2. 完了を待ち、検証します
3. 必要に応じて **Install-Machine-Agent** を実行します
4. 必要に応じて **Install-Database-Agent** を実行します

### シナリオ 2: Smart Agent の更新

Smart Agent を新しいバージョンに更新する場合:

1. 新しい Smart Agent ZIP をダウンロードします
2. 設定済みのパスで Jenkins に配置します
3. **Deploy-Smart-Agent** パイプラインを再度実行します

パイプラインは自動的に以下を実行します:

- 既存の Smart Agent を停止する
- 古いファイルを削除する
- 新しいバージョンをインストールする
- Smart Agent を再起動する

### シナリオ 3: 新規ホストの追加

新しいホストに Smart Agent を追加する場合:

1. Jenkins の `deployment-hosts` 認証情報を更新します
2. 新しい IP アドレスを追加します (1 行に 1 つ)
3. **Deploy-Smart-Agent** パイプラインを実行します

パイプラインは以下を実行します:

- 設定済みのホストをスキップする (冪等な場合)
- 新しいホストにのみデプロイする

### シナリオ 4: 完全な削除

全ホストから Smart Agent を完全に削除する場合:

1. **Cleanup-All-Agents** パイプラインへ移動します
2. **Build with Parameters** をクリックします
3. `CONFIRM_CLEANUP` チェックボックスを **チェック** します
4. **Build** をクリックします

{{% notice style="danger" %}}
これにより `/opt/appdynamics/appdsmartagent` ディレクトリが全ホストから完全に削除されます。この操作は取り消せません。
{{% /notice %}}

## デプロイメントのトラブルシューティング

### Preparation ステージでビルドが失敗する

**症状**: ホストリストの読み込み時にパイプラインが失敗します

**原因**: `deployment-hosts` 認証情報が不足または不正です

**解決策**:

1. **Manage Jenkins → Credentials** へ移動します
2. `deployment-hosts` 認証情報が存在することを確認します
3. フォーマットを確認します (1 行に 1 IP、カンマなし)
4. 末尾のスペースがないことを確認します

### SSH 接続の失敗

**症状**: "Permission denied" または "Connection refused" エラー

**解決策**:

**セキュリティグループの確認:**

```bash
# Verify Jenkins agent can reach target
ping 172.31.1.243
telnet 172.31.1.243 22
```

**SSH を手動でテスト:**

```bash
# From Jenkins agent machine
ssh -i /path/to/key ubuntu@172.31.1.243
```

**SSH キーの検証:**

1. `ssh-private-key` 認証情報が正しいことを確認します
2. 公開キーが対象ホストの `~/.ssh/authorized_keys` にあることを確認します

### Smart Agent が起動しない

**症状**: デプロイメントは完了するが Smart Agent が稼働していません

**解決策**:

**対象ホストのログを確認:**

```bash
cd /opt/appdynamics/appdsmartagent
cat log.log
```

**よくある問題:**

- **アクセスキーが無効**: `account-access-key` 認証情報を確認します
- **ネットワーク接続**: Controller への送信 HTTPS を確認します
- **権限の問題**: APPD_USER に正しい権限があることを確認します

### 部分的なデプロイメント成功

**症状**: 一部のホストは成功し、他は失敗します

**解決策**:

1. **Console Output を確認** - どのホストが失敗したかを特定します
2. **失敗したホストを調査** - SSH 接続して手動でテストします
3. **パイプラインを再実行** - Jenkins は再試行が必要なホストを追跡します

## パイプラインのベストプラクティス

### 1. まず単一ホストでテストする

新しい設定は、本番環境にデプロイする前に必ず単一ホストでテストします:

```
1. Create deployment-hosts-test credential (1 IP)
2. Create test pipeline pointing to this credential
3. Verify success
4. Deploy to full host list
```

### 2. 説明的なビルド説明を使用する

ビルドをトリガーした後、説明を追加します:

1. ビルドページへ移動します
2. **Edit Build Information** をクリックします
3. 説明を追加します: "Production deployment - Q4 2024"

### 3. ビルド履歴を監視する

定期的にビルド履歴のパターンを確認します:

- 失敗したビルド
- 実行時間の傾向
- エラーメッセージ

### 4. メンテナンスウィンドウ中にデプロイメントをスケジュールする

本番システムの場合:

- Jenkins のスケジュールビルドを使用する
- トラフィックの少ない時間帯にデプロイする
- ロールバック計画を準備しておく

### 5. 認証情報を最新に保つ

- SSH キーを四半期ごとにローテーションする
- インフラストラクチャの変更に応じてホストリストを更新する
- AppDynamics アクセスキーの有効性を検証する

## Next Steps

次に、大規模デプロイメントに向けたスケーリングと運用上の考慮事項を見ていきます。
