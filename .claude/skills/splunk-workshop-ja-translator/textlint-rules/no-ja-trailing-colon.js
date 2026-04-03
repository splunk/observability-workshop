"use strict";

/**
 * textlint rule: no-ja-trailing-colon
 *
 * 日本語文の行末に全角コロン「：」があるのは不自然なため除去する。
 * translation-guide.md の「行末コロンの除去」ルールを機械的に適用する。
 *
 * コードブロック（Syntax.CodeBlock / Syntax.Code）は textlint が自動スキップするため
 * コードブロック外のテキストのみを対象とする。
 */

function reporter(context) {
  const { Syntax, RuleError, report, fixer, getSource } = context;

  return {
    [Syntax.Str](node) {
      const text = getSource(node);
      // 行末（文字列末尾 or 改行前）の全角「：」を検出
      const pattern = /：(\n|$)/g;
      let match;
      while ((match = pattern.exec(text)) !== null) {
        const index = match.index;
        report(
          node,
          new RuleError("行末に全角コロン「：」があります。日本語文では行末コロンは除去してください。", {
            index: index,
            fix: fixer.replaceTextRange([index, index + 1], "")
          })
        );
      }
    }
  };
}

module.exports = { linter: reporter, fixer: reporter };
