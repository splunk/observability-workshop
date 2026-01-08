# GitHub Actions ワークフロー

このディレクトリには、Splunk Observability Workshopのビルドとメンテナンスに使用されるGitHub Actionsワークフローが含まれています。

## ワークフロー一覧

### 1. Deploy Workshop to GitHub Pages (`deploy-workshop.yml`)

ワークショップサイトをGitHub Pagesにデプロイします。

- **トリガー**: 手動実行 (`workflow_dispatch`)
- **用途**: リリースバージョンを作成し、GitHub Pagesにデプロイ
- **実行者**: メンテナー

### 2. Sync Upstream and Translate (`sync-and-translate.yml`)

フォーク元リポジトリの変更を定期的に取り込み、日本語に自動翻訳します。

- **トリガー**:
  - スケジュール: 毎週月曜日 9:00 JST (00:00 UTC)
  - 手動実行 (`workflow_dispatch`)
- **処理内容**:
  1. upstream (`splunk/observability-workshop`) から最新の変更を取得
  2. 前回の同期以降に変更された英語コンテンツを検出
  3. 未翻訳のコンテンツを検出（手動実行時のオプション）
  4. Claude Code (Bedrock) を使用して日本語に翻訳
  5. 翻訳結果をコミットし、ドラフトPRを作成

#### 手動実行オプション

- `translate_all_untranslated`: すべての未翻訳コンテンツも翻訳する（デフォルト: false）

#### 必要なシークレット

- `AWS_ROLE_ARN`: AWS BedrockへのアクセスにOIDCで使用するIAMロールARN

### 3. Translate Content on Release (`translate-on-release.yml`)

このフォークリポジトリでリリースが公開されたときに、変更された英語コンテンツを日本語に自動翻訳します。

- **トリガー**: リリース公開時 (`release.published`)
- **処理内容**:
  1. 前回のリリースタグとの差分を検出
  2. 変更された英語コンテンツを特定
  3. Claude Code (Bedrock) を使用して日本語に翻訳
  4. 翻訳結果をコミットし、ドラフトPRを作成

#### 注意事項

このワークフローは、このフォークリポジトリ内でのリリースに対して実行されます。upstream (`splunk/observability-workshop`) のリリースには反応しません。

#### 必要なシークレット

- `AWS_ROLE_ARN`: AWS BedrockへのアクセスにOIDCで使用するIAMロールARN

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

翻訳が完了すると、ドラフトPRが自動的に作成されます。レビュー後、以下を確認してください：

- [ ] Markdownが正しくレンダリングされる
- [ ] すべてのリンクが機能する
- [ ] コードブロックが変更されていない
- [ ] 用語が一貫している
- [ ] 太字マークアップが正しく表示される

## ローカルでの翻訳テスト

```bash
# Hugoサーバーを起動
hugo serve

# ブラウザで http://localhost:1313/ja/ にアクセス
```

## トラブルシューティング

### 翻訳が失敗する

- AWS認証情報が正しく設定されているか確認
- Claude Code CLIが最新バージョンか確認
- ログを確認し、エラーメッセージを特定

### マージコンフリクトが発生する

`sync-and-translate.yml` でupstreamとのマージでコンフリクトが発生した場合：

1. ローカルで手動マージを実行
2. コンフリクトを解決
3. 解決後、手動でワークフローを再実行

## フォーク元との関係

このリポジトリはupstream (`splunk/observability-workshop`) からフォークされています。

- **フォーク元**: https://github.com/splunk/observability-workshop
- **同期方針**: 定期的にupstreamの変更を取り込み、日本語翻訳を維持
- **マージ方針**: 日本語翻訳はこのフォークリポジトリ内でのみ管理し、upstreamにはマージしません

## 参考リンク

- [Claude Code](https://claude.ai/claude-code)
- [Splunk Observability Workshop](https://splunk.github.io/observability-workshop/)
- [Hugo Documentation](https://gohugo.io/documentation/)
