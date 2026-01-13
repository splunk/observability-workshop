# Splunk Observability Workshop 翻訳プロジェクト

## プロジェクト概要

このリポジトリは、[Splunk Observability Workshop](https://github.com/splunk/observability-workshop) の日本語翻訳を自動化するためのシステムです。

**フォーク元**: `splunk/observability-workshop`

## ブランチ構成

```text
gentksb/observability-workshop
├── main                    ← upstreamと完全同期（翻訳システムファイルなし）
├── ja-translation-system   ← このブランチ（翻訳システムのみ、デフォルト）
└── translate/*             ← 翻訳PRブランチ
```

### 重要: ブランチの役割

| ブランチ | 内容 | 用途 |
|---------|------|------|
| `main` | upstreamの完全コピー | 翻訳のベースブランチ |
| `ja-translation-system` | 翻訳システムのみ | **現在のブランチ** |
| `translate/v*` | 翻訳結果 | upstream へのPR |

**注意**: `ja-translation-system` にはコンテンツファイル（content/, assets/等）がありません。翻訳作業は `main` ブランチをベースに `translate/*` ブランチで行います。

## 翻訳スキル

翻訳作業には `/splunk-workshop-ja-translator` スキルを使用します。

**スキル定義**: `.claude/skills/splunk-workshop-ja-translator/SKILL.md`

### 翻訳ルール概要

- **翻訳しないもの**: コードブロック、CLIコマンド、URL、製品名（Splunk, Kubernetes等）
- **文体**: です/ます調（丁寧語）
- **太字**: 機能名・UI要素は英語を維持、文章は翻訳

詳細は `.claude/skills/splunk-workshop-ja-translator/references/translation-guide.md` を参照。

## ファイル構成

```text
.claude/
├── settings.json                           # プロジェクト設定
└── skills/splunk-workshop-ja-translator/
    ├── SKILL.md                            # 翻訳スキル定義
    └── references/translation-guide.md     # 翻訳ガイドライン

.github/workflows/
├── sync-and-translate.yml                  # 翻訳ワークフロー
├── CLAUDE.md                               # ワークフロー詳細ドキュメント
└── README.md                               # ワークフロー説明

.gitignore
.last-translated-tag                        # 最後に翻訳したタグ
.markdownlint.json                          # Markdownlint設定
CLAUDE.md                                   # このファイル
README.md                                   # プロジェクト概要
```

## ワークフロー

自動翻訳ワークフローの詳細は `.github/workflows/CLAUDE.md` を参照してください。

### 手動翻訳時の手順

1. `main` ブランチをチェックアウト
2. 翻訳対象ファイルを `content/en/` から `content/ja/` にコピー
3. `/splunk-workshop-ja-translator` スキルで翻訳を実行
4. `hugo serve` でプレビュー確認
5. PR を作成
