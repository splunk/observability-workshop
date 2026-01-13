# Splunk Observability Workshop 翻訳システム

このブランチ (`ja-translation-system`) は翻訳自動化ワークフローを管理します。

## ブランチの目的

- upstream (splunk/observability-workshop) の新しいリリースを検出
- 変更された英語コンテンツを日本語に自動翻訳
- 翻訳結果を PR として作成

## 含まれるファイル

```text
.claude/                                    # Claude Code スキル設定
├── settings.json
└── skills/splunk-workshop-ja-translator/
    ├── SKILL.md                            # 翻訳スキル定義
    └── references/translation-guide.md     # 翻訳ガイドライン

.github/workflows/
├── sync-and-translate.yml                  # 翻訳ワークフロー
├── CLAUDE.md                               # ワークフロー用指示
└── README.md                               # ワークフロー説明

.gitignore                                  # Git ignore設定
.last-translated-tag                        # 最後に翻訳したタグ
.markdownlint.json                          # Markdownlint設定
README.md                                   # このファイル
```

## 使用方法

1. upstream で新しいリリースが作成されると、ワークフローが自動実行
2. 変更された英語ファイルを検出し、日本語に翻訳
3. PR が自動作成される

詳細は `.github/workflows/README.md` を参照してください。

## 注意事項

- このブランチにはコンテンツファイル（content/, assets/ 等）は含まれません
- コンテンツは `main` ブランチで管理されます
- 翻訳結果は `translate/*` ブランチに作成され、`main` への PR となります
