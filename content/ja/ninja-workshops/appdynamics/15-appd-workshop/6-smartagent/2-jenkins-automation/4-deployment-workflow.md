---
title: デプロイメントワークフロー
weight: 4
time: 15 minutes
---

## 初回デプロイメント

パイプラインの設定が完了したので、最初の Smart Agent デプロイメントの実行手順を説明します。

### ステップ 1: パイプラインに移動

1. **Jenkins Dashboard** に移動します
2. **Deploy-Smart-Agent** パイプラインをクリックします

### ステップ 2: パラメータ付きビルド

1. 左サイドバーの **Build with Parameters** をクリックします
2. デフォルトパラメータを確認します:
   - **SMARTAGENT_ZIP_PATH**: パスが正しいことを確認します
   - **REMOTE_INSTALL_DIR**: `/opt/appdynamics/appdsmartagent`
   - **APPD_USER**: `ubuntu`（または SSH ユーザー）
   - **APPD_GROUP**: `ubuntu`
   - **SSH_PORT**: `22`
   - **AGENT_NAME**: `smartagent`
   - **LOG_LEVEL**: `DEBUG`

3. 必要に応じてパラメータを調整します
4. **Build** をクリックします

{{% notice style="tip" %}}
初回デプロイメントでは、IP アドレスを1つだけ含む別のクレデンシャルを作成して、単一ホストでテストすることを検討してください。
{{% /notice %}}

### ステップ 3: パイプライン実行の監視

**Build** をクリックすると、以下が表示されます:

1. **Build added to queue** - Build History にビルド番号が表示されます
2. **ビルド番号をクリック**（例: #1）して詳細を表示します
3. **Console Output をクリック**してリアルタイムログを表示します

### ステップ 4: コンソール出力の理解

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

表示される主要なステージ:

1. ✅ **Preparation** - ホストリストの読み込みと検証
2. ✅ **Extract Smart Agent** - ZIP ファイルの展開
3. ✅ **Configure Smart Agent** - config.ini の作成
4. ✅ **Deploy to Remote Hosts** - 各ホストへのデプロイ
5. ✅ **Verify Installation** - Smart Agent のステータス確認

### ステップ 5: 結果の確認

完了後、以下のいずれかが表示されます:

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

デプロイメントが成功した後、ターゲットホストで Smart Agent が実行されていることを確認します。

### Smart Agent のステータス確認

ターゲットホストに SSH 接続してステータスを確認します:

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

AppDynamics Controller への接続成功メッセージを確認してください。

### AppDynamics Controller での検証

1. AppDynamics Controller にログインします
2. **Servers → Servers** に移動します
3. 新しくデプロイされたホストを探します
4. Smart Agent がメトリクスを報告していることを確認します

## 追加エージェントのインストール

Smart Agent がデプロイされたら、他のパイプラインを使用して特定のエージェントタイプをインストールできます。

### Machine Agent のインストール

1. **Install-Machine-Agent** パイプラインに移動します
2. **Build with Parameters** をクリックします
3. パラメータを確認します:
   - **AGENT_NAME**: `machine-agent`
   - **SSH_PORT**: `22`
4. **Build** をクリックします

パイプラインは各ホストに SSH 接続して以下を実行します:

```bash
cd /opt/appdynamics/appdsmartagent
sudo ./smartagentctl install --component machine
```

### Database Agent のインストール

1. **Install-Database-Agent** パイプラインに移動します
2. **Build with Parameters** をクリックします
3. データベース接続パラメータを設定します
4. **Build** をクリックします

パイプラインはすべてのホストに Database Agent をインストールして設定します。

### エージェントインストールの検証

エージェントをインストールした後、表示されることを確認します:

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

### シナリオ 1: 初期デプロイメント

**ワークフロー:**

1. **Deploy-Smart-Agent** パイプラインを実行します
2. 完了を待って検証します
3. 必要に応じて **Install-Machine-Agent** を実行します
4. 必要に応じて **Install-Database-Agent** を実行します

### シナリオ 2: Smart Agent の更新

Smart Agent を新しいバージョンに更新するには:

1. 新しい Smart Agent ZIP をダウンロードします
2. Jenkins の設定済みパスに配置します
3. **Deploy-Smart-Agent** パイプラインを再度実行します

パイプラインは自動的に以下を行います:

- 既存の Smart Agent を停止
- 古いファイルを削除
- 新しいバージョンをインストール
- Smart Agent を再起動

### シナリオ 3: 新しいホストの追加

新しいホストに Smart Agent を追加するには:

1. Jenkins の `deployment-hosts` クレデンシャルを更新します
2. 新しい IP アドレスを追加します（1行に1つ）
3. **Deploy-Smart-Agent** パイプラインを実行します

パイプラインは以下を行います:

- 設定済みのホストをスキップ（冪等な場合）
- 新しいホストにのみデプロイ

### シナリオ 4: 完全削除

すべてのホストから Smart Agent を完全に削除するには:

1. **Cleanup-All-Agents** パイプラインに移動します
2. **Build with Parameters** をクリックします
3. `CONFIRM_CLEANUP` チェックボックスを**チェック**します
4. **Build** をクリックします

{{% notice style="danger" %}}
これにより、すべてのホストから `/opt/appdynamics/appdsmartagent` ディレクトリが完全に削除されます。この操作は元に戻すことができません。
{{% /notice %}}

## デプロイメントのトラブルシューティング

### Preparation ステージでビルドが失敗する

**症状**: ホストリストの読み込み時にパイプラインが失敗します

**原因**: `deployment-hosts` クレデンシャルが見つからないか正しくありません

**解決策**:

1. **Manage Jenkins → Credentials** に移動します
2. `deployment-hosts` クレデンシャルが存在することを確認します
3. フォーマットを確認します（1行に1つの IP、カンマなし）
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

**手動で SSH をテスト:**

```bash
# From Jenkins agent machine
ssh -i /path/to/key ubuntu@172.31.1.243
```

**SSH キーの検証:**

1. `ssh-private-key` クレデンシャルが正しいことを確認します
2. ターゲットホストの `~/.ssh/authorized_keys` に公開鍵があることを確認します

### Smart Agent が起動しない

**症状**: デプロイメントは完了するが Smart Agent が実行されていません

**解決策**:

**ターゲットホストのログを確認:**

```bash
cd /opt/appdynamics/appdsmartagent
cat log.log
```

**一般的な問題:**

- **無効なアクセスキー**: `account-access-key` クレデンシャルを確認してください
- **ネットワーク接続**: Controller への送信 HTTPS を確認してください
- **権限の問題**: APPD_USER が正しい権限を持っていることを確認してください

### 部分的なデプロイメント成功

**症状**: 一部のホストは成功し、他は失敗します

**解決策**:

1. **Console Output を確認** - どのホストが失敗したかを特定します
2. **失敗したホストを調査** - SSH で手動テストを行います
3. **パイプラインを再実行** - Jenkins がリトライが必要なホストを追跡します

## パイプラインのベストプラクティス

### 1. まず単一ホストでテスト

本番環境にデプロイする前に、必ず単一ホストで新しい設定をテストしてください:

```
1. Create deployment-hosts-test credential (1 IP)
2. Create test pipeline pointing to this credential
3. Verify success
4. Deploy to full host list
```

### 2. わかりやすいビルド説明を使用

ビルドをトリガーした後、説明を追加します:

1. ビルドページに移動します
2. **Edit Build Information** をクリックします
3. 説明を追加します: "Production deployment - Q4 2024"

### 3. ビルド履歴の監視

ビルド履歴を定期的に確認してパターンを把握します:

- 失敗したビルド
- 所要時間のトレンド
- エラーメッセージ

### 4. メンテナンスウィンドウ中にデプロイメントをスケジュール

本番システムの場合:

- Jenkins のスケジュールビルドを使用します
- トラフィックの少ない時間帯にデプロイします
- ロールバック計画を準備しておきます

### 5. クレデンシャルを最新の状態に保つ

- SSH キーを四半期ごとにローテーションします
- インフラストラクチャの変更に合わせてホストリストを更新します
- AppDynamics アクセスキーの有効性を確認します

## 次のステップ

大規模デプロイメントのスケーリングと運用上の考慮事項について説明します。
