---
title: テスト結果の確認
linkTitle: 7. テスト結果の確認
weight: 7
---


1\. テスト実行結果のスパイクまたは失敗をクリックします。

![Spike in the browser test performance KPIs chart](../_img/browser-spike.png)

2\. このテスト実行から何がわかりますか？失敗した場合は、エラーメッセージ、フィルムストリップ、ビデオリプレイ、ウォーターフォールを使用して何が起こったかを理解します。

![Single test run result, with an error message and screenshots](../_img/browser-fail-result.png)

3\. リソースに何が表示されていますか？すべてのページ（またはトランザクション）タブをクリックして確認してください。

![resources in the browser test waterfall, with a long request highlighted](../_img/browser-resources.png)

{{% notice title="Workshop Question" style="tip" icon="question" %}}
何か興味深いものが見つかりましたか？よく見つかる問題には、予期しないレスポンスコード、重複リクエスト、忘れられたサードパーティ、大きいまたは遅いファイル、リクエスト間の長いギャップなどがあります。
{{% /notice %}}

特定のパフォーマンス改善についてもっと学びたいですか？[Google](https://web.dev/learn/performance/welcome) と [Mozilla](https://developer.mozilla.org/en-US/docs/Web/Performance/How_browsers_work) には、フロントエンドパフォーマンスの構成要素を理解し、最適化する方法の詳細を学ぶための優れたリソースがあります。
