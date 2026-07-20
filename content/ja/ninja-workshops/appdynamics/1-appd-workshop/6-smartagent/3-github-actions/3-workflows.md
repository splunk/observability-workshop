---
title: ワークフローの理解
weight: 3
time: 10 minutes
---

## 利用可能なワークフロー

GitHub Actionsラボには、Smart Agentのライフサイクル管理を完全にカバーする **11のワークフロー** が含まれています。すべてのワークフローファイルはリポジトリの `.github/workflows/` にあります。

**リポジトリ**: [https://github.com/chambear2809/github-actions-lab](https://github.com/chambear2809/github-actions-lab)

## ワークフローカテゴリ

### 1. デプロイメント（1ワークフロー）

#### Deploy Smart Agent（バッチ処理）

- **File**: `deploy-agent-batched.yml`
- **目的**: Smart Agentをインストールし、サービスを開始します
- **機能**:
  - 自動バッチ処理（デフォルト: バッチあたり256ホスト）
  - バッチサイズの設定が可能
  - 各バッチ内での並列デプロイ
  - バッチの順次処理
- **入力**:
  - `batch_size`: バッチあたりのホスト数（デフォルト: 256）
- **トリガー**: 手動のみ（`workflow_dispatch`）

### 2. エージェントのインストール（4ワークフロー）

すべてのインストールワークフローは `smartagentctl` を使用して特定のエージェントタイプをインストールします。

#### Install Node Agent（バッチ処理）

- **File**: `install-node-batched.yml`
- **Command**: `smartagentctl install node`
- **バッチ処理**: あり（設定可能）

#### Install Machine Agent（バッチ処理）

- **File**: `install-machine-batched.yml`
- **Command**: `smartagentctl install machine`
- **バッチ処理**: あり（設定可能）

#### Install DB Agent（バッチ処理）

- **File**: `install-db-batched.yml`
- **Command**: `smartagentctl install db`
- **バッチ処理**: あり（設定可能）

#### Install Java Agent（バッチ処理）

- **File**: `install-java-batched.yml`
- **Command**: `smartagentctl install java`
- **バッチ処理**: あり（設定可能）

### 3. エージェントのアンインストール（4ワークフロー）

すべてのアンインストールワークフローは `smartagentctl` を使用して特定のエージェントタイプを削除します。

#### Uninstall Node Agent（バッチ処理）

- **File**: `uninstall-node-batched.yml`
- **Command**: `smartagentctl uninstall node`
- **バッチ処理**: あり（設定可能）

#### Uninstall Machine Agent（バッチ処理）

- **File**: `uninstall-machine-batched.yml`
- **Command**: `smartagentctl uninstall machine`
- **バッチ処理**: あり（設定可能）

#### Uninstall DB Agent（バッチ処理）

- **File**: `uninstall-db-batched.yml`
- **Command**: `smartagentctl uninstall db`
- **バッチ処理**: あり（設定可能）

#### Uninstall Java Agent（バッチ処理）

- **File**: `uninstall-java-batched.yml`
- **Command**: `smartagentctl uninstall java`
- **バッチ処理**: あり（設定可能）

### 4. Smart Agentの管理（2ワークフロー）

#### Stop and Clean Smart Agent（バッチ処理）

- **File**: `stop-clean-smartagent-batched.yml`
- **Commands**:
  - `smartagentctl stop`
  - `smartagentctl clean`
- **目的**: Smart Agentサービスを停止し、すべてのデータを削除します
- **バッチ処理**: あり（設定可能）

#### Cleanup All Agents（バッチ処理）

- **File**: `cleanup-appdynamics.yml`
- **Command**: `sudo rm -rf /opt/appdynamics`
- **目的**: /opt/appdynamicsディレクトリを完全に削除します
- **バッチ処理**: あり（設定可能）
- **警告**: すべてのAppDynamicsコンポーネントが完全に削除されます

{{% notice style="danger" %}}
「Cleanup All Agents」ワークフローは `/opt/appdynamics` を完全に削除します。この操作は元に戻せません。注意して使用してください。
{{% /notice %}}

## ワークフローの構造

すべてのバッチワークフローは、一貫した2ジョブ構造に従います。

### Job 1: Prepare

```yaml
prepare:
  runs-on: self-hosted
  outputs:
    batches: ${{ steps.create-batches.outputs.batches }}
  steps:
    - name: Load hosts and create batches
      run: |
        # Load DEPLOYMENT_HOSTS variable
        # Split into batches of N hosts
        # Output as JSON array
```

**目的**: GitHubの変数からターゲットホストを読み込み、バッチマトリクスを作成します

### Job 2: Deploy/Install/Uninstall

```yaml
deploy:
  needs: prepare
  runs-on: self-hosted
  strategy:
    matrix:
      batch: ${{ fromJson(needs.prepare.outputs.batches) }}
  steps:
    - name: Setup SSH key
    - name: Execute operation on all hosts in batch (parallel)
```

**目的**: 各バッチに対して並列実行し、バッチ内のすべてのホストで特定の操作を実行します

## バッチ処理の動作

### 仕組み

1. **Prepare Job** が `DEPLOYMENT_HOSTS` を読み込み、バッチに分割します
2. **Deploy Job** がバッチごとに1つのマトリクスエントリを作成します
3. **バッチは順次処理されます** （ランナーへの過負荷を防ぐため）
4. **各バッチ内では** 、すべてのホストがバックグラウンドプロセスを使用して並列にデプロイされます

### バッチサイズの設定

すべてのワークフローは `batch_size` 入力を受け付けます（デフォルト: 256）。

```bash
# Via GitHub CLI
gh workflow run "Deploy Smart Agent" -f batch_size=128

# Via GitHub UI
Actions → Select workflow → Run workflow → Set batch_size
```

### 例

- **100ホスト、batch_size=256**: 1バッチ、約3分
- **500ホスト、batch_size=256**: 2バッチ、約6分
- **1,000ホスト、batch_size=128**: 8バッチ、約16分
- **5,000ホスト、batch_size=256**: 20バッチ、約60分

## ワークフローの実行順序

### 一般的なデプロイメントシーケンス

1. **Deploy Smart Agent** - 初期デプロイメント
2. **Install Machine Agent** - 必要に応じて特定のエージェントをインストール
3. **Install DB Agent** - データベースモニタリングをインストール
4. （必要に応じて他のインストールワークフローを使用）

### メンテナンス/アップデートシーケンス

1. **Stop and Clean Smart Agent** - サービスを停止し、データをクリーンアップ
2. **Deploy Smart Agent** - 更新バージョンで再デプロイ
3. **エージェントを再インストール** - 必要なエージェントを再インストール

### 完全な削除シーケンス

1. **Stop and Clean Smart Agent** - サービスを停止
2. **Cleanup All Agents** - /opt/appdynamicsディレクトリを削除

## ワークフローコードの確認

リポジトリで完全なワークフローYAMLファイルを確認できます。

**メインデプロイメントワークフロー:**
[https://github.com/chambear2809/github-actions-lab/blob/main/.github/workflows/deploy-agent-batched.yml](https://github.com/chambear2809/github-actions-lab/blob/main/.github/workflows/deploy-agent-batched.yml)

**すべてのワークフロー:**
[https://github.com/chambear2809/github-actions-lab/tree/main/.github/workflows](https://github.com/chambear2809/github-actions-lab/tree/main/.github/workflows)

## ワークフローの機能

### 組み込みのエラーハンドリング

- ホストごとのエラー追跡
- 失敗したホストのレポート
- バッチレベルの障害処理
- 常に実行されるサマリー

### 並列実行

- バッチ内のすべてのホストが同時にデプロイされます
- SSHバックグラウンドプロセス（`&`）を使用します
- waitコマンドですべての完了を保証します
- リソース制限内での最大並列性

### セキュリティ

- SSHキーがログに公開されることはありません
- 認証情報は環境変数としてバインドされます
- 自動化のためにstrict host key checkingが無効化されています
- ワークフロー完了後にキーが削除されます

## 次のステップ

利用可能なワークフローを理解したので、最初のデプロイメントを実行しましょう。
