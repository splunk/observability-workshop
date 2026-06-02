---
title: ワークフローの理解
weight: 3
time: 10 minutes
---

## 利用可能なワークフロー

この GitHub Actions ラボには、Smart Agent のライフサイクル全体を管理するための **11 個のワークフロー** が含まれています。すべてのワークフローファイルは、リポジトリの `.github/workflows/` で参照できます。

**Repository**: [https://github.com/chambear2809/github-actions-lab](https://github.com/chambear2809/github-actions-lab)

## ワークフローのカテゴリ

### 1. デプロイメント (1 ワークフロー)

#### Deploy Smart Agent (Batched)

- **File**: `deploy-agent-batched.yml`
- **目的**: Smart Agent をインストールし、サービスを開始します
- **特徴**:
  - 自動バッチ処理 (デフォルト: 1 バッチあたり 256 ホスト)
  - バッチサイズの設定が可能
  - 各バッチ内では並列デプロイ
  - バッチ間は順次処理
- **Inputs**:
  - `batch_size`: バッチあたりのホスト数 (デフォルト: 256)
- **Trigger**: 手動のみ (`workflow_dispatch`)

### 2. エージェントのインストール (4 ワークフロー)

すべてのインストールワークフローは、`smartagentctl` を使用して特定の種類のエージェントをインストールします。

#### Install Node Agent (Batched)

- **File**: `install-node-batched.yml`
- **Command**: `smartagentctl install node`
- **Batched**: あり (設定可能)

#### Install Machine Agent (Batched)

- **File**: `install-machine-batched.yml`
- **Command**: `smartagentctl install machine`
- **Batched**: あり (設定可能)

#### Install DB Agent (Batched)

- **File**: `install-db-batched.yml`
- **Command**: `smartagentctl install db`
- **Batched**: あり (設定可能)

#### Install Java Agent (Batched)

- **File**: `install-java-batched.yml`
- **Command**: `smartagentctl install java`
- **Batched**: あり (設定可能)

### 3. エージェントのアンインストール (4 ワークフロー)

すべてのアンインストールワークフローは、`smartagentctl` を使用して特定の種類のエージェントを削除します。

#### Uninstall Node Agent (Batched)

- **File**: `uninstall-node-batched.yml`
- **Command**: `smartagentctl uninstall node`
- **Batched**: あり (設定可能)

#### Uninstall Machine Agent (Batched)

- **File**: `uninstall-machine-batched.yml`
- **Command**: `smartagentctl uninstall machine`
- **Batched**: あり (設定可能)

#### Uninstall DB Agent (Batched)

- **File**: `uninstall-db-batched.yml`
- **Command**: `smartagentctl uninstall db`
- **Batched**: あり (設定可能)

#### Uninstall Java Agent (Batched)

- **File**: `uninstall-java-batched.yml`
- **Command**: `smartagentctl uninstall java`
- **Batched**: あり (設定可能)

### 4. Smart Agent の管理 (2 ワークフロー)

#### Stop and Clean Smart Agent (Batched)

- **File**: `stop-clean-smartagent-batched.yml`
- **Commands**:
  - `smartagentctl stop`
  - `smartagentctl clean`
- **目的**: Smart Agent サービスを停止し、すべてのデータを削除します
- **Batched**: あり (設定可能)

#### Cleanup All Agents (Batched)

- **File**: `cleanup-appdynamics.yml`
- **Command**: `sudo rm -rf /opt/appdynamics`
- **目的**: /opt/appdynamics ディレクトリを完全に削除します
- **Batched**: あり (設定可能)
- **警告**: この操作はすべての AppDynamics コンポーネントを完全に削除します

{{% notice style="danger" %}}
"Cleanup All Agents" ワークフローは `/opt/appdynamics` を完全に削除します。この操作は元に戻せません。慎重に使用してください。
{{% /notice %}}

## ワークフローの構造

すべてのバッチ処理対応ワークフローは、一貫した 2 ジョブ構造に従います。

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

**目的**: GitHub variables から対象ホストを読み込み、バッチマトリックスを作成します

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

**目的**: 各バッチに対して並列に実行され、バッチ内のすべてのホストで指定された操作を実行します

## バッチ処理の動作

### 仕組み

1. **Prepare Job** が `DEPLOYMENT_HOSTS` を読み込み、バッチに分割します
2. **Deploy Job** が各バッチに対して 1 つのマトリックスエントリを作成します
3. **バッチは順次処理** され、ランナーへの過負荷を防ぎます
4. **各バッチ内** では、バックグラウンドプロセスを使用してすべてのホストへ並列でデプロイします

### バッチサイズの設定

すべてのワークフローは `batch_size` 入力を受け付けます (デフォルト: 256)。

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

### 一般的なデプロイメントの流れ

1. **Deploy Smart Agent** - 初期デプロイ
2. **Install Machine Agent** - 必要に応じて特定のエージェントをインストール
3. **Install DB Agent** - データベース監視のインストール
4. (必要に応じて他のインストールワークフローを使用)

### メンテナンス・更新の流れ

1. **Stop and Clean Smart Agent** - サービスを停止し、データをクリーンアップ
2. **Deploy Smart Agent** - 更新版で再デプロイ
3. **Install agents again** - 必要なエージェントを再インストール

### 完全削除の流れ

1. **Stop and Clean Smart Agent** - サービスを停止
2. **Cleanup All Agents** - /opt/appdynamics ディレクトリを削除

## ワークフローのコードを確認する

リポジトリで完全なワークフロー YAML ファイルを確認できます。

**メインのデプロイメントワークフロー:**
[https://github.com/chambear2809/github-actions-lab/blob/main/.github/workflows/deploy-agent-batched.yml](https://github.com/chambear2809/github-actions-lab/blob/main/.github/workflows/deploy-agent-batched.yml)

**すべてのワークフロー:**
[https://github.com/chambear2809/github-actions-lab/tree/main/.github/workflows](https://github.com/chambear2809/github-actions-lab/tree/main/.github/workflows)

## ワークフローの機能

### 組み込みのエラーハンドリング

- ホスト単位のエラー追跡
- 失敗したホストのレポート
- バッチレベルでの失敗処理
- 必ず実行されるサマリー

### 並列実行

- バッチ内のすべてのホストへ同時にデプロイ
- SSH のバックグラウンドプロセス (`&`) を使用
- wait コマンドですべての完了を保証
- リソース制限内での最大限の並列性

### セキュリティ

- SSH キーがログに表示されることはありません
- 認証情報は環境変数としてバインドされます
- 自動化のため厳密なホストキーチェックは無効化されています
- ワークフロー完了後にキーは削除されます

## 次のステップ

利用可能なワークフローを理解したところで、最初のデプロイを実行してみましょう。
