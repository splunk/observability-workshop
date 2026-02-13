---
title: 4. ログビューチャート
weight: 4
---

ログで使用できる次のチャートタイプは**ログビュー**チャートタイプです。このチャートでは、事前定義されたフィルターに基づいてログメッセージを確認できます。

前回のログタイムラインチャートと同様に、このチャートのバージョンをカスタマーヘルスサービスダッシュボードに追加します

{{% notice title="情報" style="green" title="演習" icon="running" %}}

- 前回の演習後、まだ**Log Observer**にいることを確認してください。
- フィルターは前回の演習と同じで、時間選択が**過去 15 分**に設定され、severity=error、`sf_service=paymentservice`、`sf_environment=[WORKSHOPNAME]` でフィルタリングされている必要があります。
- 必要なフィールドのみを含むヘッダーがあることを確認してください。
- 再度**Save**をクリックし、**Save to Dashvoard**をクリックします。
- これによりチャート作成ダイアログが再度表示されます。
- **Chart name**として**ログビュー**を使用します。
- 今回は{{% button style="blue" %}}Select Dashboard{{% /button %}}をクリックし、前回の演習で作成したダッシュボードを検索します。検索ボックス（**1**）にあなたのイニシャルを入力することから始めることができます。
  ![ダッシュボードの検索](../images/search-dashboard.png)
- あなたのダッシュボード名をクリックして強調表示し（**2**）、{{% button style="blue" %}}OK{{% /button %}}（**3**）をクリックします。
- これによりチャート作成ダイアログに戻ります。
- **Chart type**として**Log view**が選択されていることを確認します。
  ![ログビュー](../images/log-view.png?classes=left&width=30vw)
- ダッシュボードを表示するには、{{% button style="blue" %}}Save and go to dashboard{{% /button %}}をクリックします。
- 結果は以下のダッシュボードと同様になるはずです
  ![カスタムダッシュボード](../images/log-observer-custom-dashboard.png)
- この演習の最後のステップとして、あなたのダッシュボードをワークショップチームページに追加しましょう。これにより、ワークショップの後半で簡単に見つけることができます。
- ページ上部で、あなたのダッシュボード名の左にある **_..._** をクリックします。
  ![リンク](../images/linking.png)
- ドロップダウンから**Links to Team**を選択します。
- 次の**Links to Team**ダイアログボックスで、インストラクターが提供したワークショップチームを見つけて{{% button style="blue" %}}Done{{% /button %}}をクリックします。

{{% /notice %}}

次のセッションでは、Splunk Syntheticsを見て、Webベースのアプリケーションのテストを自動化する方法を確認します。
