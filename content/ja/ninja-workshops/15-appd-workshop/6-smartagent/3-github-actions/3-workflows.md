---
title: ワークフローの理解
weight: 3
time: 10 minutes
---

## 利用可能なワークフロー

GitHub Actions ラボには、Smart Agent の完全なライフサイクル管理のための **11のワークフロー** が含まれています。すべてのワークフローファイルはリポジトリの `.github/workflows/` で利用できます。

**リポジトリ**: [https://github.com/chambear2809/github-actions-lab](https://github.com/chambear2809/github-actions-lab)

## ワークフローカテゴリ

### 1. デプロイ（1ワークフロー）

#### Deploy Smart Agent（バッチ処理）

- **ファイル**: `deploy-agent-batched.yml`
- **目的**: Smart Agent のインストールとサービスの起動
- **機能**:
  - 自動バッチ処理（デフォルト: バッチあたり256ホスト）
  - 設定可能なバッチサイズ
  - 各バッチ内での並列デプロイ
  - シーケンシャルバッチ処理
- **入力**:
  - `batch_size`: バッチあたりのホスト数（デフォルト: 256）
- **トリガー**: 手動のみ（`workflow_dispatch`）

### 2. エージェントのインストール（4ワークフロー）

すべてのインストールワークフローは、特定のエージェントタイプをインストールするために `smartagentctl` を使用します:

#### Install Node Agent（バッチ処理）

- **ファイル**: `install-node-batched.yml`
- **コマンド**: `smartagentctl install node`
- **バッチ処理**: あり（設定可能）

#### Install Machine Agent（バッチ処理）

- **ファイル**: `install-machine-batched.yml`
- **コマンド**: `smartagentctl install machine`
- **バッチ処理**: あり（設定可能）

#### Install DB Agent（バッチ処理）

- **ファイル**: `install-db-batched.yml`
- **コマンド**: `smartagentctl install db`
- **バッチ処理**: あり（設定可能）

#### Install Java Agent（バッチ処理）

- **ファイル**: `install-java-batched.yml`
- **コマンド**: `smartagentctl install java`
- **バッチ処理**: あり（設定可能）

### 3. エージェントのアンインストール（4ワークフロー）

すべてのアンインストールワークフローは、特定のエージェントタイプを削除するために `smartagentctl` を使用します:

#### Uninstall Node Agent（バッチ処理）

- **ファイル**: `uninstall-node-batched.yml`
- **コマンド**: `smartagentctl uninstall node`
- **バッチ処理**: あり（設定可能）

#### Uninstall Machine Agent（バッチ処理）

- **ファイル**: `uninstall-machine-batched.yml`
- **コマンド**: `smartagentctl uninstall machine`
- **バッチ処理**: あり（設定可能）

#### Uninstall DB Agent（バッチ処理）

- **ファイル**: `uninstall-db-batched.yml`
- **コマンド**: `smartagentctl uninstall db`
- **バッチ処理**: あり（設定可能）

#### Uninstall Java Agent（バッチ処理）

- **ファイル**: `uninstall-java-batched.yml`
- **コマンド**: `smartagentctl uninstall java`
- **バッチ処理**: あり（設定可能）

### 4. Smart Agent 管理（2ワークフロー）

#### Stop and Clean Smart Agent（バッチ処理）

- **ファイル**: `stop-clean-smartagent-batched.yml`
- **コマンド**:
  - `smartagentctl stop`
  - `smartagentctl clean`
- **目的**: Smart Agent サービスの停止とすべてのデータのパージ
- **バッチ処理**: あり（設定可能）

#### Cleanup All Agents（バッチ処理）

- **ファイル**: `cleanup-appdynamics.yml`
- **コマンド**: `sudo rm -rf /opt/appdynamics`
- **目的**: /opt/appdynamics ディレクトリの完全な削除
- **バッチ処理**: あり（設定可能）
- **警告**: すべての AppDynamics コンポーネントが完全に削除されます

{{% notice style="danger" %}}
「Cleanup All Agents」ワークフローは `/opt/appdynamics` を完全に削除します。この操作は元に戻せません。注意して使用してください。
{{% /notice %}}

## ワークフローの構造

すべてのバッチ処理ワークフローは、一貫した2ジョブ構成に従います:

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

**目的**: GitHub Variables からターゲットホストを読み込み、バッチマトリックスを作成

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

**目的**: 各バッチに対して並列に実行し、バッチ内のすべてのホストで特定の操作を実行

## バッチ処理の動作

### 仕組み

1. **Prepare ジョブ** が `DEPLOYMENT_HOSTS` を読み込み、バッチに分割
2. **Deploy ジョブ** がバッチごとに1つのマトリックスエントリを作成
3. **バッチはシーケンシャルに処理** され、ランナーの過負荷を防止
4. **各バッチ内** では、バックグラウンドプロセスを使用してすべてのホストが並列にデプロイ

### 設定可能なバッチサイズ

すべてのワークフローは `batch_size` 入力を受け付けます（デフォルト: 256）:

```bash
# Via GitHub CLI
gh workflow run "Deploy Smart Agent" -f batch_size=128

# Via GitHub UI
Actions → Select workflow → Run workflow → Set batch_size
```

### 例

- **100台のホスト、batch_size=256**: 1バッチ、約3分
- **500台のホスト、batch_size=256**: 2バッチ、約6分
- **1,000台のホスト、batch_size=128**: 8バッチ、約16分
- **5,000台のホスト、batch_size=256**: 20バッチ、約60分

## ワークフローの実行順序

### 典型的なデプロイシーケンス

1. **Deploy Smart Agent** - 初期デプロイ
2. **Install Machine Agent** - 必要に応じて特定のエージェントをインストール
3. **Install DB Agent** - データベースモニタリングのインストール
4. （必要に応じて他のインストールワークフローを使用）

### メンテナンス/アップデートシーケンス

1. **Stop and Clean Smart Agent** - サービスの停止とデータのクリーン
2. **Deploy Smart Agent** - 更新バージョンの再デプロイ
3. **エージェントの再インストール** - 必要なエージェントの再インストール

### 完全な削除シーケンス

1. **Stop and Clean Smart Agent** - サービスの停止
2. **Cleanup All Agents** - /opt/appdynamics ディレクトリの削除

## ワークフローコードの確認

リポジトリで完全なワークフロー YAML ファイルを確認できます:

**メインデプロイワークフロー:**
[https://github.com/chambear2809/github-actions-lab/blob/main/.github/workflows/deploy-agent-batched.yml](https://github.com/chambear2809/github-actions-lab/blob/main/.github/workflows/deploy-agent-batched.yml)

**すべてのワークフロー:**
[https://github.com/chambear2809/github-actions-lab/tree/main/.github/workflows](https://github.com/chambear2809/github-actions-lab/tree/main/.github/workflows)

## ワークフローの機能

### 組み込みエラーハンドリング

- ホストごとのエラー追跡
- 失敗したホストのレポート
- バッチレベルの障害処理
- 常に実行されるサマリー

### 並列実行

- バッチ内のすべてのホストが同時にデプロイ
- SSH バックグラウンドプロセス（`&`）を使用
- wait コマンドですべての完了を保証
- リソース制限内での最大並列処理

### セキュリティ

- SSH キーはログに公開されない
- 認証情報は環境変数としてバインド
- 自動化のために厳密なホストキーチェックを無効化
- ワークフロー完了後にキーを削除

## 次のステップ

利用可能なワークフローを理解したところで、最初のデプロイを実行しましょう。
