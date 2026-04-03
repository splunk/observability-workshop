# GitHub Actions ワークフロー

このディレクトリには、Splunk Observability Workshopの日本語翻訳を自動化するGitHub Actionsワークフローが含まれています。

ブランチ構成の概要はリポジトリルートの `CLAUDE.md` を参照してください。

## sync-and-translate.yml

upstreamリポジトリの新しいリリースを検出し、日本語に自動翻訳してPRを作成します。

### トリガー

- **スケジュール**: 毎週月曜日9:00 JST (00:00 UTC)
- **手動実行**: `workflow_dispatch`

### 手動実行オプション

| オプション | 説明 | デフォルト |
| --------- | ---- | --------- |
| `force_translate` | 新しいタグがなくても翻訳を実行 | false |
| `translate_all_untranslated` | すべての未翻訳コンテンツも翻訳 | false |

### 処理フロー

1. **新リリースチェック**: upstreamの最新タグを取得し、`.last-translated-tag` と比較
2. **mainブランチ同期**: 新しいタグがあれば、mainをupstreamのタグにリセット
3. **新ワークショップ検出**: 翻訳対象ファイルから新しいワークショップディレクトリを検出
4. **翻訳**: 変更されたファイルをClaude Code (Bedrock)で翻訳
5. **PR作成**: upstreamリポジトリにPRを作成（新ワークショップがある場合はドラフトPR）
6. **タグ記録**: 翻訳したタグを `.last-translated-tag` に記録
7. **Slack通知**: ワークフロー実行結果を Slack に通知（新リリースなし・翻訳対象なしの場合も含む）

### 新ワークショップ検出とドラフトPR

翻訳対象ファイルに新しいワークショップが含まれる場合、PRをドラフト状態で作成し、人間のレビューを促します。

**新ワークショップの判定基準**: 以下の2つのケースで「リリース済み新規ワークショップ」を検出します。

- **ケース1（新規ディレクトリ）**: `content/en/{category}/{workshop-name}/` レベルのディレクトリが前回翻訳タグ時点で存在せず、かつ `_index.md` の frontmatter に `draft: true` / `hidden: true` がない場合
- **ケース2（draft解除）**: 前回翻訳タグ時点で `draft: true` / `hidden: true` だったが、現在は解除または `false` に変更された場合

WorkshopはHugoの `draft: true` で開発を開始し、リリース時に削除または `false` に変更するフローのため、ディレクトリ作成だけでなくdraftステータスの変化もリリース検出の基準としています。

**動作**:

- 新ワークショップ検出時: `--draft` フラグ付きでPRを作成、PR本文に検出されたワークショップ一覧を記載
- 新ワークショップなし: 通常のPRを作成
- 初回実行（前回タグなし）: 検出をスキップし、通常のPRを作成

### Slack通知

`notify-slack` ジョブは `check-new-release` ジョブが成功した場合に常に実行され、ワークフローの実行結果を Slack Webhook に送信します。

**発火条件**: `check-new-release` ジョブが成功した場合（新リリースの有無に関わらず）

**ペイロード**:

| フィールド | 型 | 内容 |
| --------- | -- | ---- |
| `reason` | string | 実行結果の理由（下記参照） |
| `status` | string | `success` または `failure` |
| `hasNewWorkshopTranslation` | string | 新規ワークショップが含まれるか（`yes`/`no`） |
| `translatedMarkdownFileCount` | string | 翻訳成功ファイル数 |
| `failedFileCount` | string | 翻訳失敗ファイル数 |
| `pullRequestNumber` | string | 作成されたPR番号 |

**`reason` フィールドの値**:

| 値 | 意味 |
| -- | ---- |
| `translated` | 新バージョンあり・翻訳ファイルあり（通常フロー） |
| `no_translation_targets` | 新バージョンはあったが翻訳対象ファイルが0件 |
| `no_new_release` | スケジュール実行されたが新バージョンのリリースがなかった |

**必要なシークレット**: `SLACK_WEBHOOK_URL`

### 必要なシークレット

| シークレット | 用途 |
| ---------- | ---- |
| `AWS_ROLE_ARN` | AWS BedrockへのOIDCアクセス用IAMロールARN |
| `UPSTREAM_PAT` | upstreamリポジトリへのPR作成用PAT（`Pull requests: Read and write` 権限が必要） |

### 必要な権限

| 権限 | 用途 |
| --- | ---- |
| `id-token: write` | AWS OIDC認証 |
| `contents: write` | ブランチの作成・プッシュ |
| `pull-requests: write` | PRの作成 |

## 翻訳

- **翻訳モデル**: Claude Opus 4.5 (via AWS Bedrock)
- **翻訳スキル**: `.claude/skills/splunk-workshop-ja-translator/`
- **翻訳対象**: `content/en/**/*.md` → `content/ja/**/*.md`（関連する `img/` も含む）

### PRレビューチェックリスト

- [ ] Markdownが正しくレンダリングされる
- [ ] すべてのリンクが機能する
- [ ] コードブロックが変更されていない
- [ ] 用語が一貫している
- [ ] 太字マークアップが正しく表示される

## セットアップ手順

### 1. ブランチ構成の設定

```bash
git checkout -b ja-translation-system
git checkout main
git remote add upstream https://github.com/splunk/observability-workshop.git
git fetch upstream
git reset --hard upstream/main
git push origin main --force
```

### 2. GitHubリポジトリ設定

1. **デフォルトブランチの変更**: Settings → General → Default branch → `ja-translation-system`
2. **ブランチ保護ルール**: `main` と `ja-translation-system` を保護（`main` はforce pushを許可）

### 3. シークレットの設定

- `AWS_ROLE_ARN`: AWS BedrockへのOIDCアクセス用IAMロールARN
- `UPSTREAM_PAT`: GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens
  - Resource owner: `splunk`
  - Repository access: `splunk/observability-workshop`
  - Permissions: `Pull requests: Read and write`

### 4. AWS OIDC設定

GitHub ActionsからAWS Bedrockにアクセスするために、OIDCプロバイダーとIAMロールを設定します。

## トラブルシューティング

| 問題 | 確認事項 |
| ---- | ------- |
| 翻訳が実行されない | upstreamに新しいタグがあるか確認。手動実行で `force_translate` を有効化。`.last-translated-tag` の内容を確認 |
| 翻訳が失敗する | AWS認証情報の設定を確認。Claude Code CLIのバージョンを確認。ログでエラーメッセージを特定 |
| upstream へのPR作成失敗 | `UPSTREAM_PAT` の設定・有効期限・権限を確認 |
