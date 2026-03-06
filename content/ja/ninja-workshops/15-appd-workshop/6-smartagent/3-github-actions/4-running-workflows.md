---
title: ワークフローの実行
weight: 4
time: 15 minutes
---

## ワークフローのトリガー

すべてのワークフローは `workflow_dispatch` で設定されており、手動でトリガーする必要があります。ワークフローを実行する主な方法は2つあります:

1. **GitHub UI** - ビジュアルインターフェース、ほとんどのユーザーにとって最も簡単
2. **GitHub CLI** - コマンドラインインターフェース、自動化に最適

## 方法 1: GitHub UI

### ステップ 1: Actions タブに移動

1. GitHub上のフォークしたリポジトリに移動します
2. 上部の **Actions** タブをクリックします

### ステップ 2: ワークフローを選択

左側のサイドバーに、利用可能なすべてのワークフローが表示されます:

- Deploy Smart Agent
- Install Node Agent (Batched)
- Install Machine Agent (Batched)
- Install DB Agent (Batched)
- Install Java Agent (Batched)
- Uninstall Node Agent (Batched)
- Uninstall Machine Agent (Batched)
- Uninstall DB Agent (Batched)
- Uninstall Java Agent (Batched)
- Stop and Clean Smart Agent (Batched)
- Cleanup All Agents

実行するワークフローをクリックします。

### ステップ 3: ワークフローを実行

1. **"Run workflow"** ボタン（右上）をクリックします
2. ブランチ **main** を選択します
3. （オプション）必要に応じて **batch_size** を調整します
4. **"Run workflow"** ボタンをクリックします

### ステップ 4: 実行を監視

1. ワークフローが下のリストに表示されます
2. ワークフローの実行をクリックして詳細を確認します
3. リアルタイムで進捗を監視します
4. ジョブ名をクリックして詳細なログを確認します

## 方法 2: GitHub CLI

### GitHub CLI のインストール

```bash
# macOS
brew install gh

# Linux
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
```

### 認証

```bash
gh auth login
```

### ワークフローの実行

```bash
# Deploy Smart Agent (default batch size)
gh workflow run "Deploy Smart Agent" --repo YOUR_USERNAME/github-actions-lab

# Deploy with custom batch size
gh workflow run "Deploy Smart Agent" \
  --repo YOUR_USERNAME/github-actions-lab \
  -f batch_size=128

# Install agents
gh workflow run "Install Node Agent (Batched for Large Scale)" \
  --repo YOUR_USERNAME/github-actions-lab

gh workflow run "Install Machine Agent (Batched for Large Scale)" \
  --repo YOUR_USERNAME/github-actions-lab

# Uninstall agents
gh workflow run "Uninstall Node Agent (Batched for Large Scale)" \
  --repo YOUR_USERNAME/github-actions-lab

# Stop and clean
gh workflow run "Stop and Clean Smart Agent (Batched for Large Scale)" \
  --repo YOUR_USERNAME/github-actions-lab

# Complete cleanup
gh workflow run "Cleanup All Agents" \
  --repo YOUR_USERNAME/github-actions-lab
```

### ワークフローの監視

```bash
# List recent workflow runs
gh run list --repo YOUR_USERNAME/github-actions-lab

# View specific run
gh run view RUN_ID --repo YOUR_USERNAME/github-actions-lab

# Watch run in progress
gh run watch RUN_ID --repo YOUR_USERNAME/github-actions-lab

# View failed logs
gh run view RUN_ID --log-failed --repo YOUR_USERNAME/github-actions-lab
```

## 初回デプロイのウォークスルー

完全な初回デプロイの手順を説明します:

### ステップ 1: セットアップの確認

ワークフローを実行する前に、以下を確認します:

- セルフホストランナーが「Idle」（緑色）と表示されている
- `SSH_PRIVATE_KEY` Secretが設定されている
- `DEPLOYMENT_HOSTS` VariableにターゲットIPが含まれている
- ネットワーク接続が確認済み

### ステップ 2: Smart Agent のデプロイ

**GitHub UI 経由:**

1. **Actions** タブに移動します
2. **"Deploy Smart Agent"** を選択します
3. **"Run workflow"** をクリックします
4. デフォルトのbatch_size（256）を受け入れます
5. **"Run workflow"** をクリックします

**GitHub CLI 経由:**

```bash
gh workflow run "Deploy Smart Agent" --repo YOUR_USERNAME/github-actions-lab
```

### ステップ 3: 実行の監視

ワークフローは以下を表示します:

1. **Prepare** ジョブ - バッチマトリックスの作成
2. **Deploy** ジョブ（バッチごとに1つ）- ホストへのデプロイ

各ジョブをクリックして詳細なログを確認します。

### ステップ 4: インストールの確認

ターゲットホストにSSH接続して確認します:

```bash
# SSH to target
ssh ubuntu@172.31.1.243

# Check Smart Agent status
cd /opt/appdynamics/appdsmartagent
sudo ./smartagentctl status
```

**期待される出力:**

```text
Smart Agent is running (PID: 12345)
Service: appdsmartagent.service
Status: active (running)
```

### ステップ 5: 追加エージェントのインストール（オプション）

必要に応じて、特定のエージェントタイプをインストールします:

```bash
# Install Machine Agent
gh workflow run "Install Machine Agent (Batched for Large Scale)" \
  --repo YOUR_USERNAME/github-actions-lab

# Install DB Agent
gh workflow run "Install DB Agent (Batched for Large Scale)" \
  --repo YOUR_USERNAME/github-actions-lab
```

## ワークフロー出力の理解

### Prepare ジョブの出力

```text
Loading deployment hosts...
Total hosts: 1000
Batch size: 256
Creating 4 batches...
Batch 1: Hosts 1-256
Batch 2: Hosts 257-512
Batch 3: Hosts 513-768
Batch 4: Hosts 769-1000
```

### Deploy ジョブの出力（バッチごと）

```text
Processing batch 1 of 4
Deploying to 256 hosts in parallel...
Host 172.31.1.1: SUCCESS
Host 172.31.1.2: SUCCESS
Host 172.31.1.3: SUCCESS
...
Batch 1 complete: 256/256 succeeded
```

### 完了サマリー

```text
Deployment Summary:
Total hosts: 1000
Successful: 998
Failed: 2
Failed hosts:
  - 172.31.1.48
  - 172.31.1.125
```

## よくあるデプロイシナリオ

### シナリオ 1: 初期デプロイ

```bash
# 1. Deploy Smart Agent
gh workflow run "Deploy Smart Agent"

# 2. Verify deployment
# SSH to a host and check status

# 3. Install agents as needed
gh workflow run "Install Machine Agent (Batched for Large Scale)"
gh workflow run "Install DB Agent (Batched for Large Scale)"
```

### シナリオ 2: Smart Agent のアップデート

```bash
# 1. Stop and clean current installation
gh workflow run "Stop and Clean Smart Agent (Batched for Large Scale)"

# 2. Update Smart Agent ZIP in repository
# (Push new version to repository)

# 3. Deploy new version
gh workflow run "Deploy Smart Agent"

# 4. Reinstall agents
gh workflow run "Install Machine Agent (Batched for Large Scale)"
```

### シナリオ 3: 新しいホストの追加

```bash
# 1. Update DEPLOYMENT_HOSTS variable in GitHub
# Add new IPs

# 2. Deploy to all hosts (will skip existing ones with idempotent logic)
gh workflow run "Deploy Smart Agent"
```

### シナリオ 4: 完全な削除

```bash
# 1. Stop and clean
gh workflow run "Stop and Clean Smart Agent (Batched for Large Scale)"

# 2. Complete removal
gh workflow run "Cleanup All Agents"
```

{{% notice style="danger" %}}
「Cleanup All Agents」は `/opt/appdynamics` を完全に削除します。この操作は元に戻せません。
{{% /notice %}}

## ワークフロー失敗のトラブルシューティング

### ワークフローが「Queued」のまま

**症状**: ワークフローが開始されない

**原因**: ランナーが利用できないかオフライン

**解決策**:

1. ランナーステータスを確認します: Settings → Actions → Runners
2. ランナーが「Idle」（緑色）と表示されていることを確認します
3. 必要に応じてランナーを再起動します: `sudo ./svc.sh restart`

### SSH 接続の失敗

**症状**:「Permission denied」または「Connection refused」エラー

**解決策**:

**SSH を手動でテスト:**

```bash
# From runner instance
ssh -i ~/.ssh/test-key.pem ubuntu@172.31.1.243
```

**セキュリティグループを確認:**

- ランナーからのSSH（22）が許可されていることを確認
- ランナーとターゲットが同じセキュリティグループにあることを確認

**SSH キーを確認:**

- `SSH_PRIVATE_KEY` Secretが実際のキーと一致していることを確認
- ターゲットホストに公開鍵があることを確認

### 部分的なバッチの失敗

**症状**: 一部のホストが成功し、他が失敗

**解決策**:

1. ワークフローログで失敗したホストを特定
2. 失敗したホストにSSH接続して調査
3. ワークフローを再実行（冪等性 - 成功したホストはスキップ）

### バッチジョブエラー

**症状**:「Error splitting hosts into batches」

**解決策**:

- `DEPLOYMENT_HOSTS` Variableのフォーマットを確認
- 1行に1つのIPであることを確認
- 末尾のスペースや特殊文字がないことを確認
- Unix改行コード（LF、CRLFではなく）を使用

## パフォーマンスチューニング

### バッチサイズの調整

**小さなバッチ**（リソース使用量が少ない、速度は低下）:

```bash
gh workflow run "Deploy Smart Agent" -f batch_size=128
```

**大きなバッチ**（リソース使用量が多い、速度は向上）:

```bash
gh workflow run "Deploy Smart Agent" -f batch_size=256
```

### ランナーリソースの推奨事項

| ホスト数  | CPU    | メモリ | バッチサイズ |
|-----------|--------|--------|--------------|
| 1-100     | 2コア  | 4 GB   | 256          |
| 100-500   | 4コア  | 8 GB   | 256          |
| 500-2000  | 8コア  | 16 GB  | 256          |
| 2000+     | 16コア | 32 GB  | 256          |

## ベストプラクティス

1. **まず単一ホストでテスト**
   - 1つのIPでテスト変数を作成
   - ワークフローを実行して確認
   - その後フルリストにデプロイ

2. **ワークフロー実行の監視**
   - リアルタイムでログを監視
   - エラーを即座に確認
   - サンプルホストで検証

3. **適切なバッチサイズの使用**
   - デフォルト（256）はほとんどの場合に適用
   - ランナーに負荷がかかる場合は削減
   - ランナーのリソース使用量を監視

4. **ワークフローを最新の状態に維持**
   - リポジトリから最新の変更をプル
   - 本番環境以外で先にアップデートをテスト
   - カスタマイズ内容をドキュメント化

5. **ランナーの正常性を維持**
   - ランナーをオンラインかつアイドル状態に維持
   - ランナーソフトウェアを定期的にアップデート
   - ディスク容量とリソースを監視

## 次のステップ

おめでとうございます。GitHub Actionsを使用したAppDynamics Smart Agentデプロイの自動化方法を学びました。詳細については、[完全なリポジトリ](https://github.com/chambear2809/github-actions-lab)を参照してください。
