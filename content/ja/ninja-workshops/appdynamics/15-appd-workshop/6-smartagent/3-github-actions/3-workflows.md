---
title: ワークフローの理解
weight: 3
time: 10 minutes
---

## 利用可能なワークフロー

GitHub Actions ラボには、Smart Agent のライフサイクル管理を完全にカバーする **11 のワークフロー** が含まれています。すべてのワークフローファイルはリポジトリの `.github/workflows/` にあります。

**リポジトリ**: [https://github.com/chambear2809/github-actions-lab](https://github.com/chambear2809/github-actions-lab)

## ワークフローのカテゴリ

### 1. デプロイメント（1 ワークフロー）

#### Deploy Smart Agent (Batched)

- **ファイル**: `deploy-agent-batched.yml`
- **目的**: Smart Agent をインストールしてサービスを開始します
- **機能**:
  - 自動バッチ処理（デフォルト: バッチあたり 256 ホスト）
  - バッチサイズの設定が可能
  - 各バッチ内での並列デプロイメント
  - バッチの順次処理
- **入力**:
  - `batch_size`: バッチあたりのホスト数（デフォルト: 256）
- **トリガー**: 手動のみ（`workflow_dispatch`）

### 2. エージェントのインストール（4 ワークフロー）

すべてのインストールワークフローは `smartagentctl` を使用して特定のエージェントタイプをインストールします:

#### Install Node Agent (Batched)

- **ファイル**: `install-node-batched.yml`
- **コマンド**: `smartagentctl install node`
- **バッチ処理**: あり（設定可能）

#### Install Machine Agent (Batched)

- **ファイル**: `install-machine-batched.yml`
- **コマンド**: `smartagentctl install machine`
- **バッチ処理**: あり（設定可能）

#### Install DB Agent (Batched)

- **ファイル**: `install-db-batched.yml`
- **コマンド**: `smartagentctl install db`
- **バッチ処理**: あり（設定可能）

#### Install Java Agent (Batched)

- **ファイル**: `install-java-batched.yml`
- **コマンド**: `smartagentctl install java`
- **バッチ処理**: あり（設定可能）

### 3. エージェントのアンインストール（4 ワークフロー）

すべてのアンインストールワークフローは `smartagentctl` を使用して特定のエージェントタイプを削除します:

#### Uninstall Node Agent (Batched)

- **ファイル**: `uninstall-node-batched.yml`
- **コマンド**: `smartagentctl uninstall node`
- **バッチ処理**: あり（設定可能）

#### Uninstall Machine Agent (Batched)

- **ファイル**: `uninstall-machine-batched.yml`
- **コマンド**: `smartagentctl uninstall machine`
- **バッチ処理**: あり（設定可能）

#### Uninstall DB Agent (Batched)

- **ファイル**: `uninstall-db-batched.yml`
- **コマンド**: `smartagentctl uninstall db`
- **バッチ処理**: あり（設定可能）

#### Uninstall Java Agent (Batched)

- **ファイル**: `uninstall-java-batched.yml`
- **コマンド**: `smartagentctl uninstall java`
- **バッチ処理**: あり（設定可能）

### 4. Smart Agent の管理（2 ワークフロー）

#### Stop and Clean Smart Agent (Batched)

- **ファイル**: `stop-clean-smartagent-batched.yml`
- **コマンド**:
  - `smartagentctl stop`
  - `smartagentctl clean`
- **目的**: Smart Agent サービスを停止し、すべてのデータをパージします
- **バッチ処理**: あり（設定可能）

#### Cleanup All Agents (Batched)

- **ファイル**: `cleanup-appdynamics.yml`
- **コマンド**: `sudo rm -rf /opt/appdynamics`
- **目的**: /opt/appdynamics ディレクトリを完全に削除します
- **バッチ処理**: あり（設定可能）
- **警告**: すべての AppDynamics コンポーネントが完全に削除されます

{{% notice style="danger" %}}
「Cleanup All Agents」ワークフローは `/opt/appdynamics` を完全に削除します。この操作は元に戻すことができません。注意して使用してください！
{{% /notice %}}

## ワークフローの構造

すべてのバッチワークフローは、一貫した 2 ジョブ構造に従います:

### ジョブ 1: Prepare

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

**目的**: GitHub 変数からターゲットホストを読み込み、バッチマトリックスを作成します

### ジョブ 2: Deploy/Install/Uninstall

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

**目的**: 各バッチに対して並列で実行し、バッチ内のすべてのホストで特定の操作を実行します

## バッチ処理の動作

### 仕組み

1. **Prepare ジョブ** が `DEPLOYMENT_HOSTS` を読み込み、バッチに分割します
2. **Deploy ジョブ** がバッチごとに 1 つのマトリックスエントリを作成します
3. **バッチは順次処理されます**（ランナーへの過負荷を防ぐため）
4. **各バッチ内では**、すべてのホストがバックグラウンドプロセスを使用して並列でデプロイされます

### バッチサイズの設定

すべてのワークフローは `batch_size` 入力を受け付けます（デフォルト: 256）:

```bash
# Via GitHub CLI
gh workflow run "Deploy Smart Agent" -f batch_size=128

# Via GitHub UI
Actions → Select workflow → Run workflow → Set batch_size
```

### 例

- **100 ホスト、batch_size=256**: 1 バッチ、約 3 分
- **500 ホスト、batch_size=256**: 2 バッチ、約 6 分
- **1,000 ホスト、batch_size=128**: 8 バッチ、約 16 分
- **5,000 ホスト、batch_size=256**: 20 バッチ、約 60 分

## ワークフローの実行順序

### 一般的なデプロイメントシーケンス

1. **Deploy Smart Agent** - 初期デプロイメント
2. **Install Machine Agent** - 必要に応じて特定のエージェントをインストール
3. **Install DB Agent** - データベース監視をインストール
4. （必要に応じて他のインストールワークフローを使用）

### メンテナンス/アップデートシーケンス

1. **Stop and Clean Smart Agent** - サービスを停止しデータをクリーンアップ
2. **Deploy Smart Agent** - 更新バージョンで再デプロイ
3. **エージェントの再インストール** - 必要なエージェントを再インストール

### 完全削除シーケンス

1. **Stop and Clean Smart Agent** - サービスを停止
2. **Cleanup All Agents** - /opt/appdynamics ディレクトリを削除

## ワークフローコードの確認

リポジトリで完全なワークフロー YAML ファイルを確認できます:

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
- SSH バックグラウンドプロセス（`&`）を使用します
- wait コマンドですべての完了を確認します
- リソース制限内での最大並列性

### セキュリティ

- SSH キーがログに公開されることはありません
- 認証情報は環境変数としてバインドされます
- 自動化のために厳密なホストキーチェックが無効化されています
- ワークフロー完了後にキーが削除されます

## 次のステップ

利用可能なワークフローを理解したところで、最初のデプロイメントを実行しましょう！
