---
title: デプロイワークフロー
weight: 4
time: 15 minutes
---

## 初回デプロイ

パイプラインの設定が完了したので、最初の Smart Agent デプロイを実行してみましょう。

### ステップ1: パイプラインに移動

1. **Jenkins Dashboard** に移動します
2. **Deploy-Smart-Agent** パイプラインをクリックします

### ステップ2: パラメータを指定してビルド

1. 左サイドバーの **Build with Parameters** をクリックします
2. デフォルトパラメータを確認します:
   - **SMARTAGENT_ZIP_PATH**: パスが正しいことを確認します
   - **REMOTE_INSTALL_DIR**: `/opt/appdynamics/appdsmartagent`
   - **APPD_USER**: `ubuntu`（または使用する SSH ユーザー）
   - **APPD_GROUP**: `ubuntu`
   - **SSH_PORT**: `22`
   - **AGENT_NAME**: `smartagent`
   - **LOG_LEVEL**: `DEBUG`

3. 必要に応じてパラメータを調整します
4. **Build** をクリックします

{{% notice style="tip" %}}
初回デプロイでは、IP アドレスが1つだけの別の認証情報を作成して、単一ホストでテストすることを検討してください。
{{% /notice %}}

### ステップ3: パイプラインの実行を監視

**Build** をクリックすると、以下が表示されます:

1. **Build added to queue** - Build History にビルド番号が表示されます
2. **ビルド番号をクリック** します（例: #1）
3. **Console Output** をクリックしてリアルタイムのログを表示します

### ステップ4: コンソール出力の理解

コンソール出力にはデプロイの各ステージが表示されます:

```text
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

1. **Preparation** - ホストリストの読み込みと検証
2. **Extract Smart Agent** - ZIP ファイルの展開
3. **Configure Smart Agent** - config.ini の作成
4. **Deploy to Remote Hosts** - 各ホストへのデプロイ
5. **Verify Installation** - Smart Agent の状態確認

### ステップ5: 結果の確認

完了後、以下のいずれかが表示されます:

**成功:**

```text
Smart Agent successfully deployed to all hosts
Finished: SUCCESS
```

**部分的な成功:**

```text
Deployment completed with some failures
Failed hosts: 172.31.1.48
Finished: UNSTABLE
```

**失敗:**

```text
Smart Agent deployment failed. Check logs for details.
Finished: FAILURE
```

## インストールの検証

デプロイが成功したら、ターゲットホストで Smart Agent が稼働していることを確認します。

### Smart Agent の状態確認

ターゲットホストに SSH 接続して状態を確認します:

```bash
# ターゲットホストに SSH 接続
ssh ubuntu@172.31.1.243

# インストールディレクトリに移動
cd /opt/appdynamics/appdsmartagent

# Smart Agent の状態を確認
sudo ./smartagentctl status
```

**期待される出力:**

```text
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

```text
No agents currently installed
(Use install-machine-agent or install-db-agent pipelines to add agents)
```

### ログの確認

```bash
cd /opt/appdynamics/appdsmartagent
tail -f log.log
```

AppDynamics Controller への接続成功メッセージを確認します。

### AppDynamics Controller での確認

1. AppDynamics Controller にログインします
2. **Servers → Servers** に移動します
3. 新しくデプロイされたホストを探します
4. Smart Agent が Metric をレポートしていることを確認します

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

### エージェントインストールの確認

エージェントのインストール後、表示されることを確認します:

```bash
cd /opt/appdynamics/appdsmartagent
sudo ./smartagentctl list
```

**期待される出力:**

```text
Installed agents:
- machine-agent (running)
- db-agent (running)
```

## 一般的なデプロイシナリオ

### シナリオ1: 初回デプロイ

**ワークフロー:**

1. **Deploy-Smart-Agent** パイプラインを実行します
2. 完了を待って検証します
3. 必要に応じて **Install-Machine-Agent** を実行します
4. 必要に応じて **Install-Database-Agent** を実行します

### シナリオ2: Smart Agent のアップデート

Smart Agent を新しいバージョンにアップデートするには:

1. 新しい Smart Agent ZIP をダウンロードします
2. 設定済みのパスに Jenkins に配置します
3. **Deploy-Smart-Agent** パイプラインを再度実行します

パイプラインは自動的に以下を行います:

- 既存の Smart Agent を停止
- 古いファイルを削除
- 新しいバージョンをインストール
- Smart Agent を再起動

### シナリオ3: 新しいホストの追加

Smart Agent を新しいホストに追加するには:

1. Jenkins の `deployment-hosts` 認証情報を更新します
2. 新しい IP アドレスを追加します（1行に1つ）
3. **Deploy-Smart-Agent** パイプラインを実行します

パイプラインは以下を行います:

- 設定済みのホストをスキップします（冪等性がある場合）
- 新しいホストにのみデプロイします

### シナリオ4: 完全な削除

すべてのホストから Smart Agent を完全に削除するには:

1. **Cleanup-All-Agents** パイプラインに移動します
2. **Build with Parameters** をクリックします
3. `CONFIRM_CLEANUP` チェックボックスに **チェックを入れます**
4. **Build** をクリックします

{{% notice style="danger" %}}
これにより、すべてのホストから `/opt/appdynamics/appdsmartagent` ディレクトリが完全に削除されます。この操作は元に戻せません。
{{% /notice %}}

## デプロイのトラブルシューティング

### Preparation ステージでビルドが失敗する

**症状**: ホストリストの読み込み時にパイプラインが失敗する

**原因**: `deployment-hosts` 認証情報が見つからないか、正しくない

**解決策**:

1. **Manage Jenkins → Credentials** に移動します
2. `deployment-hosts` 認証情報が存在することを確認します
3. フォーマットを確認します（1行に1つの IP、カンマなし）
4. 末尾にスペースがないことを確認します

### SSH 接続の失敗

**症状**: 「Permission denied」または「Connection refused」エラーが発生する

**解決策:**

**セキュリティグループの確認:**

```bash
# Jenkins エージェントからターゲットに到達できることを確認
ping 172.31.1.243
telnet 172.31.1.243 22
```

**SSH の手動テスト:**

```bash
# Jenkins エージェントマシンから
ssh -i /path/to/key ubuntu@172.31.1.243
```

**SSH 鍵の確認:**

1. `ssh-private-key` 認証情報が正しいことを確認します
2. ターゲットホストの `~/.ssh/authorized_keys` に公開鍵があることを確認します

### Smart Agent が起動しない

**症状**: デプロイは完了するが Smart Agent が稼働していない

**解決策:**

**ターゲットホストのログを確認:**

```bash
cd /opt/appdynamics/appdsmartagent
cat log.log
```

**よくある問題:**

- **無効なアクセスキー**: `account-access-key` 認証情報を確認します
- **ネットワーク接続**: Controller への送信 HTTPS 接続を確認します
- **権限の問題**: APPD_USER に正しい権限があることを確認します

### デプロイの部分的な成功

**症状**: 一部のホストは成功するが、他のホストは失敗する

**解決策**:

1. **Console Output を確認** します - どのホストが失敗したかを特定します
2. **失敗したホストを調査** します - SSH で接続して手動でテストします
3. **パイプラインを再実行** します - Jenkins がリトライが必要なホストを追跡します

## パイプラインのベストプラクティス

### 1. まず単一ホストでテスト

本番環境にデプロイする前に、必ず単一ホストで新しい設定をテストします:

```text
1. deployment-hosts-test 認証情報を作成（IP 1つ）
2. この認証情報を使用するテストパイプラインを作成
3. 成功を確認
4. 完全なホストリストにデプロイ
```

### 2. 説明的なビルド説明を使用

ビルドをトリガーした後、説明を追加します:

1. ビルドページに移動します
2. **Edit Build Information** をクリックします
3. 説明を追加します: 「本番環境デプロイ - 2024年第4四半期」

### 3. ビルド履歴の監視

ビルド履歴を定期的にチェックしてパターンを確認します:

- 失敗したビルド
- 所要時間の傾向
- エラーメッセージ

### 4. メンテナンスウィンドウ中にデプロイをスケジュール

本番システムの場合:

- Jenkins のスケジュールビルドを使用します
- トラフィックの少ない時間帯にデプロイします
- ロールバック計画を準備しておきます

### 5. 認証情報を最新に保つ

- SSH 鍵を四半期ごとにローテーションします
- インフラストラクチャの変更に合わせてホストリストを更新します
- AppDynamics アクセスキーの有効性を確認します

## 次のステップ

大規模デプロイのスケーリングと運用上の考慮事項について見ていきましょう。
