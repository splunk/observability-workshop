---
title: Search Request
linkTitle: 2.4 Search Request
weight: 4
hidden: false
---

{{< button >}}+ Add Request{{< /button >}} をクリックして次のステップを追加します。ステップ名を **Search for Tracks named "Up around the bend"** にします。

**Request** セクションを展開し、リクエストメソッドを **GET** に変更して、以下の URL を入力します

``` text
https://api.spotify.com/v1/search?q=Up%20around%20the%20bend&type=track&offset=0&limit=5
```

次に、以下のキー/値のペアで2つのリクエストヘッダーを追加します

- **CONTENT-TYPE: application/json**
- **AUTHORIZATION: Bearer {{custom.access_token}}**
  - これは前のステップで作成したカスタム変数を使用します！

![Add search request](../../_img/api-search-request.png)

**Validation** セクションを展開し、以下の抽出を追加します

- **Extract** from **Response body** **JSON** **$.tracks.items[0].id** as **track.id**

![Add search payload](../../_img/api-search-payload.png)

保存前にテストを検証するには、ページの上部にスクロールし、必要に応じてロケーションを変更します。{{< button >}}Try now{{< /button >}} をクリックします。[Try now 機能](https://docs.splunk.com/observability/en/synthetics/test-config/try-now.html)の詳細についてはドキュメントを参照してください。

![try now](../../_img/api-try-now.png)

検証が成功したら、{{< button style="blue" >}}< Return to test{{< /button >}} をクリックしてテスト設定ページに戻ります。次に {{< button style="blue" >}}Save{{< /button >}} をクリックして API テストを保存します。

{{% notice title="Extra credit" style="green" icon="running" %}}
このテストにもっと時間をかけられますか？実行結果の Response Body を確認してみてください。このテストをより徹底的にするには、どのようなステップを追加すればよいでしょうか？テストを編集し、{{< button >}}Try now{{< /button >}} 機能を使用して、保存前に変更内容を検証してください。
{{% /notice %}}
