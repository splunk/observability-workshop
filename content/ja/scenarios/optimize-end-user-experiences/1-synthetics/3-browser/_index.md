---
title: シングルページブラウザテスト
linkTitle:  3. Browser Test
weight: 3
time: 5 minutes
---

エンドポイントのテストを開始しましたので、次はフロントエンドのブラウザ体験をテストしましょう。

シングルページの[ブラウザテスト](https://docs.splunk.com/observability/en/synthetics/browser-test/browser-test.html)から始めることで、ファーストパーティおよびサードパーティのリソースがエンドユーザーのブラウザベースのサイト体験にどのような影響を与えるかを把握できます。また、1つのテストに複数のステップの複雑さを導入する前に、ユーザーエクスペリエンスメトリクスを理解し始めることができます。

ユーザーが一般的に「ランディング」するページは、シングルページテストの開始に適した選択です。これは、サイトのホームページ、セクションのメインページ、またはあなたとエンドユーザーにとって重要な高トラフィックURLが考えられます。

1. {{% button style="blue" %}}Create new test{{% /button %}} をクリックし、Browser test を選択します
![Create new browser test](../_img/create-browser.png)

2. テスト名に**チーム名**と**イニシャル**を含めます。Name と Custom properties にテストの範囲を説明する情報を追加します（デバイスタイプとして Desktop など）。次に {{< button >}}+ Edit steps{{< /button >}} をクリックします
![Browser test content fields](../_img/browser-name.png)

3. トランザクションラベル（左上）とステップ名（右側）を、ステップを説明する読みやすいものに変更します。テストしたいURLを追加します。ワークショップのインストラクターからURLを提供してもらうこともできます。以下の例では、トランザクションは「Home」、ステップ名は「Go to homepage」です。
![Transaction and step label](../_img/single-step.png)

4. テストを検証するには、必要に応じてロケーションを変更し、{{< button >}}Try now{{< /button >}} をクリックします。[Try now 機能](https://docs.splunk.com/observability/en/synthetics/test-config/try-now.html)の詳細についてはドキュメントを参照してください。
![browser test try now buttons](../_img/browser-try-now.png)

5. テストの検証が完了するまで待ちます。テストの検証が失敗した場合は、URLとテストロケーションを再確認して、もう一度試してください。{{< button >}}Try now{{< /button >}} を使用すると、テストがそのまま保存されて実行された場合の結果を確認できます。
![Try Now browser test results](../_img/browser-try-now-result.png)

6. {{% button style="blue" %}}< Return to test{{% /button %}} をクリックして設定を続行します。
![Return to test button](../_img/return.png)

7. サイトに関する地域的なルールを考慮しながら、使用するロケーションを編集します。<p></p>
![Browser test details](../_img/browser-test-details.png)

8. Device と Frequency を編集するか、今のところデフォルト値のままにしておくことができます。フォームの下部にある {{% button style="blue" %}}Submit{{% /button %}} をクリックして、テストを保存し実行を開始します。<p></p>
![browser test submit button](../_img/browser-submit.png)

{{% notice title="ボーナスエクササイズ" style="green" icon="running" %}}
少し時間がありますか？このテストをコピーして、タイトルとデバイスタイプだけを変更して保存してください。これで、別のデバイスと接続速度でのエンドユーザー体験を可視化できます！
{{% /notice %}}

Synthetic テストが実行されている間に、実際のユーザーからデータを取得するために RUM がどのようにインストルメントされているか見てみましょう。
