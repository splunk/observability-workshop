# GitHub Actions ワークフロー

このディレクトリには、Splunk Observability Workshopの日本語翻訳を自動化するGitHub Actionsワークフローが含まれています。

## アーキテクチャ

```
フォークリポジトリ
├── main                    ← upstreamと完全同期（翻訳システムファイルなし）
├── ja-translation-system   ← 翻訳ワークフロー、.claude/などを管理（デフォルトブランチ）
└── translate/*             ← upstreamへのPR用ブランチ（content/ja/のみ）
```

### ブランチの役割

| ブランチ | 役割 |
|---------|------|
| `main` | upstreamリポジトリと完全に同期。翻訳システムのファイルは含まない |
| `ja-translation-system` | 翻訳ワークフロー、Claude Codeスキル、設定ファイルを管理。デフォルトブランチとして設定 |
| `translate/*` | 翻訳結果をupstreamにPRするためのブランチ。`content/ja/`のみを含む |

## ワークフロー

### Sync Upstream and Translate (`sync-and-translate.yml`)

upstreamリポジトリの新しいリリースを検出し、日本語に自動翻訳してPRを作成します。

#### トリガー

- **スケジュール**: 毎週月曜日 9:00 JST (00:00 UTC)
- **手動実行**: `workflow_dispatch`

#### 手動実行オプション

| オプション | 説明 | デフォルト |
|-----------|------|-----------|
| `force_translate` | 新しいタグがなくても翻訳を実行 | false |
| `translate_all_untranslated` | すべての未翻訳コンテンツも翻訳 | false |

#### 処理フロー

1. **新リリースチェック**: upstreamの最新タグを取得し、前回翻訳したタグと比較
2. **mainブランチ同期**: 新しいタグがあれば、mainをupstreamのタグにリセット
3. **翻訳**: 変更されたファイルをClaude Code (Bedrock)で翻訳
4. **PR作成**: upstreamリポジトリにドラフトPRを作成
5. **タグ記録**: 翻訳したタグを`.last-translated-tag`に記録

#### 必要なシークレット

- `AWS_ROLE_ARN`: AWS BedrockへのアクセスにOIDCで使用するIAMロールARN
- `UPSTREAM_PAT`: upstreamリポジトリへのPR作成に使用するPersonal Access Token（Fine-grained PAT推奨、`Pull requests: Read and write`権限が必要）

#### 必要な権限

- `id-token: write` - AWS OIDC認証
- `contents: write` - ブランチの作成・プッシュ
- `pull-requests: write` - PRの作成

## 翻訳について

### 翻訳の仕組み

翻訳は[Claude Code CLI](https://github.com/anthropics/claude-code)とAWS Bedrockを使用して自動的に行われます。

- **翻訳モデル**: Claude Opus 4.5 (via AWS Bedrock)
- **翻訳スキル**: `.claude/skills/splunk-workshop-ja-translator/`
- **翻訳ガイドライン**: [translation-guide.md](../../.claude/skills/splunk-workshop-ja-translator/references/translation-guide.md)

### 翻訳対象

- `content/en/**/*.md` → `content/ja/**/*.md`
- 関連する画像ファイル (`img/` ディレクトリ)

### 翻訳されないもの

- コードブロック内のコード
- CLIコマンド
- ファイルパス、URL
- 製品名 (Splunk, Kubernetes, Docker など)

### 翻訳結果の確認

翻訳が完了すると、upstreamリポジトリにドラフトPRが自動的に作成されます。レビュー後、以下を確認してください：

- [ ] Markdownが正しくレンダリングされる
- [ ] すべてのリンクが機能する
- [ ] コードブロックが変更されていない
- [ ] 用語が一貫している
- [ ] 太字マークアップが正しく表示される

## セットアップ手順

### 1. ブランチ構成の設定

```bash
# ja-translation-systemブランチを作成（現在のブランチから）
git checkout -b ja-translation-system

# mainブランチをupstreamと同期
git checkout main
git remote add upstream https://github.com/splunk/observability-workshop.git
git fetch upstream
git reset --hard upstream/main
git push origin main --force
```

### 2. GitHubリポジトリ設定

1. **デフォルトブランチの変更**:
   - Settings → General → Default branch
   - `ja-translation-system`に変更

2. **ブランチ保護ルール**:
   - `main`ブランチを保護（force pushを許可）
   - `ja-translation-system`ブランチを保護

### 3. シークレットの設定

- `AWS_ROLE_ARN`: AWS BedrockへのアクセスにOIDCで使用するIAMロールARN
- `UPSTREAM_PAT`: upstreamリポジトリへのPR作成用Personal Access Token
  - GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens
  - Resource owner: `splunk`
  - Repository access: `splunk/observability-workshop`
  - Permissions: `Pull requests: Read and write`

### 4. AWS OIDC設定

GitHub ActionsからAWS Bedrockにアクセスするために、OIDCプロバイダーとIAMロールを設定します。

## トラブルシューティング

### 翻訳が実行されない

- upstreamに新しいタグがあるか確認
- 手動実行で`force_translate`を有効にして実行
- `.last-translated-tag`ファイルの内容を確認

### 翻訳が失敗する

- AWS認証情報が正しく設定されているか確認
- Claude Code CLIが最新バージョンか確認
- ログを確認し、エラーメッセージを特定

### upstream へのPRが作成できない

- `UPSTREAM_PAT`シークレットが正しく設定されているか確認
- PATの有効期限が切れていないか確認
- PATに`Pull requests: Read and write`権限があるか確認
- upstreamリポジトリへのPR作成権限を確認

## フォーク元との関係

このリポジトリはupstream (`splunk/observability-workshop`) からフォークされています。

- **フォーク元**: https://github.com/splunk/observability-workshop
- **同期方針**: upstreamの新リリース時にmainブランチを同期
- **翻訳方針**: 翻訳結果はupstreamリポジトリにPRとして提出

## 参考リンク

- [Claude Code](https://claude.ai/claude-code)
- [Splunk Observability Workshop](https://splunk.github.io/observability-workshop/)
- [Hugo Documentation](https://gohugo.io/documentation/)
- [GitHub Actions OIDC](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
