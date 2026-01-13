---
name: splunk-workshop-ja-translator
description: Splunk Observability Workshopの英日翻訳・ローカライゼーション。Hugoベースの技術ドキュメントを日本語に翻訳する際に使用。翻訳依頼、日本語化、ローカライズ、i18n作業時にトリガーされる。Markdown構文を維持しながら、コードブロックや製品名を保持し、日本の開発者向けに自然な表現に変換する。
context: fork
hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: 'if echo "$CLAUDE_FILE_PATH" | grep -qE "\.md$"; then npx markdownlint-cli --fix "$CLAUDE_FILE_PATH" 2>/dev/null || true; fi'
---

# Splunk Workshop 日本語翻訳スキル

## 概要

Splunk Observability Workshop を英語から日本語に翻訳するためのガイドライン。単なる翻訳ではなく、日本の開発者向けにローカライズする。

## ディレクトリ構造

- ソース: `/content/en/` (最新版)
- 出力先: `/content/ja/` (同じ構造をミラーリング)

## 翻訳ワークフロー

1. 対象セクションのファイルを `/content/en/` から `/content/ja/` にコピー。対象セクションが不明な場合、Skill 利用者に確認すること
   1. Markdown ファイルだけでなく、リンクされている画像もコピーする必要があります。通常`./img/`に配置されていますが、セクション配下を丸ごとコピーすることを推奨します
2. `/content/ja/` で未翻訳ファイルを確認
3. 翻訳ルールに従って翻訳
4. `hugo serve` でプレビュー確認 (`http://localhost:1313/`)

## 自動翻訳ワークフロー（CI/CD用）

GitHub Actions からの自動実行時:

1. 翻訳対象ファイルのパスが引数として渡される
2. 対象ファイルを読み込み、翻訳ルールに従って翻訳
3. 翻訳結果を同じファイルに上書き保存
4. 処理完了を報告

## 翻訳ルール

### 翻訳しないもの

- コードブロック内のコード
- CLI コマンド
- ファイルパス、URL
- 製品名: Splunk, Kubernetes, Docker, Helm, AWS, OpenTelemetry など

### 文体

- です/ます形（丁寧語）を使用
- 技術用語は日本の開発者に馴染みのある表現を優先

### 太字（強調）の扱い

太字で強調されている単語（例: **Log Observer**）は機能名や UI 上の単語を示していることがほとんど。

- **単語の場合**: 元の英語表現を維持
- **文章の場合**: 翻訳する

### Markdown 強調と役物の問題

日本語で役物（括弧や句読点）を強調ブロック内に含めると、太字マークアップが正しく表示されない。

**対処法**: 役物が強調ブロック内に含まれる場合、前後に半角スペースを入れる

```markdown
# 悪い例（太字が効かない）

日本語で**役物（括弧文字）**を挟んだ際に

# 良い例（太字が正しく表示される）

日本語で **役物（括弧文字）** を挟んだ際に
```

## 品質チェックリスト

翻訳完了後、以下を確認:

- [ ] Markdown が正しくレンダリングされる
- [ ] すべてのリンクが機能する
- [ ] コードブロックが変更されていない
- [ ] 用語が一貫している
- [ ] 太字マークアップが正しく表示される
- [ ] Markdownlint, Prettier などのフォーマッターを実行した

## よくある翻訳パターン

詳細な翻訳パターンと用語集は [references/translation-guide.md](references/translation-guide.md) を参照。
