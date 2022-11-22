---
title: サンプルトレース
linkTitle: サンプルトレース
weight: 5
isCJKLanguage: true
---

## サンプルトレース

![Example Trace](../../images/example-trace.png)

スパンとともに、選択したトレースの全体が表示されます。エラーが発生したスパンは、その横に赤い！マークが表示されます。グレーのボックスに**x6**などの数字が表示されている場合は、それをクリックすると`paymentservice` スパンを展開することができます。

![Example Trace](../../images/trace-span.png)

赤い！マークが表示された`paymentservice` スパンの一つをクリックすると展開され、関連するメタデータやエラーの詳細が表示されます。このエラーが401エラーによるものであることがわかります。また、「テナント」や「バージョン」などの有用な情報も表示されています。

![Traces and Spans](../../images/trace-metadata.png)

エラーの原因が **無効なリクエスト** であることがわかりましたが、正確なリクエストが何であるかはわかりません。ページの下部に、ログへのコンテキストリンクが表示されます。このリンクをクリックすると、このスパンに関連付けられているログが表示されます。

![Logs Link](../../images/logs_link.png)

下の画像と同様の **Log Observer** ダッシュボードが表示されます。

![Log Observer](../../images/log_observer.png)

フィルタを使用して、エラーログのみを表示できます。右上にある`ERROR`をクリックしてから、`Add to filter`をクリックします。

![Error Filter](../../images/error_filter.png)

You should now have a shorter list of log entries which have a `severity` of `ERROR`
`severity`が`ERROR`であるログエントリに絞り込まれます。


![Filtered Results](../../images/filtered_results.png)

いずれかのエントリを選択して詳細を表示します。これで、開発者が誤って本番環境にプッシュした **無効なAPIトークン** の使用によってエラーがどのように発生したかを確認できます。

![Error Details](../../images/error_details.png)

おめでとうございます。これで、このAPMワークショップは完了です。

