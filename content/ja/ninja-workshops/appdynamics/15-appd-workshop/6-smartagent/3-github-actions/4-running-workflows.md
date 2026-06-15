---
title: ワークフローの実行
weight: 4
time: 15 minutes
---

## ワークフローのトリガー

すべてのワークフローは `workflow_dispatch` で設定されており、手動でトリガーする必要があります。ワークフローを実行するには主に2つの方法があります

1. **GitHub UI** - ビジュアルインターフェース、ほとんどのユーザーにとって最も簡単です
2. **GitHub CLI** - コマンドラインインターフェース、自動化に最適です

## 方法 1: GitHub UI

### ステップ 1: Actions タブに移動

1. GitHub 上のフォークしたリポジトリに移動します
2. 上部の **Actions** タブをクリックします

### ステップ 2: ワークフローの選択

左サイドバーに利用可能なすべてのワークフローが表示されます

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

実行したいワークフローをクリックします。

### ステップ 3: ワークフローの実行

1. 右上の **"Run workflow"** ボタンをクリックします
2. ブランチを選択します**main**
3. （オプション）必要に応じて **batch_size** を調整します
4. **"Run workflow"** ボタンをクリックします

### ステップ 4: 実行の監視

1. ワークフローが下のリストに表示されます
2. ワークフローの実行をクリックして詳細を確認します
3. リアルタイムで進行状況を確認します
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

初回デプロイの完全な手順を説明します

### ステップ 1: セットアップの確認

ワークフローを実行する前に、以下を確認してください

- ✅ セルフホストランナーが "Idle"（緑色）で表示されていること
- ✅ `SSH_PRIVATE_KEY` シークレットが設定されていること
- ✅ `DEPLOYMENT_HOSTS` 変数にターゲット IP が含まれていること
- ✅ ネットワーク接続が確認済みであること

### ステップ 2: Smart Agent のデプロイ

**GitHub UI 経由**

1. **Actions** タブに移動します
2. **"Deploy Smart Agent"** を選択します
3. **"Run workflow"** をクリックします
4. デフォルトの batch_size（256）を使用します
5. **"Run workflow"** をクリックします

**GitHub CLI 経由**

```bash
gh workflow run "Deploy Smart Agent" --repo YOUR_USERNAME/github-actions-lab
```

### ステップ 3: 実行の監視

ワークフローには以下が表示されます

1. **Prepare** ジョブ - バッチマトリックスの作成
2. **Deploy** ジョブ（バッチごとに1つ） - ホストへのデプロイ

各ジョブをクリックして詳細なログを確認します。

### ステップ 4: インストールの確認

ターゲットホストに SSH 接続して確認します

```bash
# SSH to target
ssh ubuntu@172.31.1.243

# Check Smart Agent status
cd /opt/appdynamics/appdsmartagent
sudo ./smartagentctl status
```

**期待される出力**

```
Smart Agent is running (PID: 12345)
Service: appdsmartagent.service
Status: active (running)
```

### ステップ 5: 追加エージェントのインストール（オプション）

必要に応じて、特定のエージェントタイプをインストールします

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

```
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

```
Processing batch 1 of 4
Deploying to 256 hosts in parallel...
Host 172.31.1.1: SUCCESS
Host 172.31.1.2: SUCCESS
Host 172.31.1.3: SUCCESS
...
Batch 1 complete: 256/256 succeeded
```

### 完了サマリー

```
Deployment Summary:
Total hosts: 1000
Successful: 998
Failed: 2
Failed hosts:
  - 172.31.1.48
  - 172.31.1.125
```

## 一般的なデプロイシナリオ

### シナリオ 1: 初回デプロイ

```bash
# 1. Deploy Smart Agent
gh workflow run "Deploy Smart Agent"

# 2. Verify deployment
# SSH to a host and check status

# 3. Install agents as needed
gh workflow run "Install Machine Agent (Batched for Large Scale)"
gh workflow run "Install DB Agent (Batched for Large Scale)"
```

### シナリオ 2: Smart Agent の更新

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
"Cleanup All Agents" は `/opt/appdynamics` を完全に削除します。この操作は元に戻せません！
{{% /notice %}}

## ワークフロー失敗のトラブルシューティング

### ワークフローが "Queued" のまま

**症状**: ワークフローが開始されません

**原因**: ランナーが利用できないかオフラインです

**解決方法**:

1. ランナーのステータスを確認します：Settings → Actions → Runners
2. ランナーが "Idle"（緑色）で表示されていることを確認します
3. 必要に応じてランナーを再起動します`sudo ./svc.sh restart`

### SSH 接続の失敗

**症状**: "Permission denied" または "Connection refused" エラー

**解決方法**:

**SSH を手動でテストします**

```bash
# From runner instance
ssh -i ~/.ssh/test-key.pem ubuntu@172.31.1.243
```

**セキュリティグループを確認します**

- ランナーからの SSH（22）が許可されていることを確認します
- ランナーとターゲットが同じセキュリティグループにあることを確認します

**SSH キーを確認します**

- `SSH_PRIVATE_KEY` シークレットが実際のキーと一致していることを確認します
- ターゲットホストに公開鍵が配置されていることを確認します

### 部分的なバッチ失敗

**症状**: 一部のホストは成功し、他は失敗します

**解決方法**:

1. ワークフローログを確認して失敗したホストを特定します
2. 失敗したホストに SSH 接続して調査します
3. ワークフローを再実行します（冪等性あり - 成功したホストはスキップされます）

### バッチジョブエラー

**症状**: "Error splitting hosts into batches"

**解決方法**:

- `DEPLOYMENT_HOSTS` 変数のフォーマットを確認します
- 1行に1つの IP であることを確認します
- 末尾のスペースや特殊文字がないことを確認します
- Unix 改行コード（LF、CRLF ではない）を使用してください

## パフォーマンスチューニング

### バッチサイズの調整

**小さいバッチ**（リソース消費が少ない、速度は遅い）

```bash
gh workflow run "Deploy Smart Agent" -f batch_size=128
```

**大きいバッチ**（リソース消費が多い、速度は速い）

```bash
gh workflow run "Deploy Smart Agent" -f batch_size=256
```

### ランナーリソースの推奨事項

| Hosts | CPU | Memory | Batch Size |
|-------|-----|--------|------------|
| 1-100 | 2 cores | 4 GB | 256 |
| 100-500 | 4 cores | 8 GB | 256 |
| 500-2000 | 8 cores | 16 GB | 256 |
| 2000+ | 16 cores | 32 GB | 256 |

## ベストプラクティス

1. **まず単一ホストでテストする**
   - 1つの IP でテスト変数を作成します
   - ワークフローを実行して確認します
   - その後、全リストにデプロイします

2. **ワークフローの実行を監視する**
   - リアルタイムでログを確認します
   - エラーを即座にチェックします
   - サンプルホストで確認します

3. **適切なバッチサイズを使用する**
   - デフォルト（256）はほとんどのケースで有効です
   - ランナーに負荷がかかる場合は減らします
   - ランナーのリソース使用量を監視します

4. **ワークフローを最新に保つ**
   - リポジトリから最新の変更をプルします
   - 本番環境以外で先にアップデートをテストします
   - カスタマイズを文書化します

5. **ランナーの健全性を維持する**
   - ランナーをオンラインかつアイドル状態に保ちます
   - ランナーソフトウェアを定期的にアップデートします
   - ディスク容量とリソースを監視します

## 次のステップ

おめでとうございます！GitHub Actions を使用した AppDynamics Smart Agent デプロイの自動化方法を学習しました。詳細については、[完全なリポジトリ](https://github.com/chambear2809/github-actions-lab)をご覧ください。
