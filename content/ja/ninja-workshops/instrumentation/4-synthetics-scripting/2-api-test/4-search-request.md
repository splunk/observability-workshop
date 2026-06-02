---
title: Search Request
linkTitle: 1.4 Search Request
weight: 4
hidden: false
---

## 検索リクエストの追加

有効なアクセストークンが取得できたので、これを利用します。{{< button >}}+ Add Request{{< /button >}} をクリックして次のステップを追加します。ステップ名は **Search for tracks named "Up around the bend"** とします。

これは [Spotify Search endpoint](https://developer.spotify.com/documentation/web-api/reference/search) です。クエリ文字列パラメーターは次の意味を持ちます: "Up around the bend" というフレーズにマッチするトラックを検索し (`type=track`)、最初の結果から取得を開始し (`offset=0`)、最大5件を返す (`limit=5`)。Spotify はクエリフレーズを URL エンコードするため、スペースは `%20` になります。

**Request** セクションを展開し、リクエストメソッドを **GET** に変更して、以下の URL を入力します:

``` text
https://api.spotify.com/v1/search?q=Up%20around%20the%20bend&type=track&offset=0&limit=5
```

次に、以下のキー/値ペアでリクエストヘッダーを2つ追加します:

- **CONTENT-TYPE: application/json** — リクエストボディの形式を宣言します。厳密には GET リクエストはボディを持たないため、ここでのこのヘッダーは情報提供のみの意味合いですが、送信するのが礼儀であり、Spotify も問題視しません。
- **AUTHORIZATION: Bearer {{custom.access_token}}** — ここが肝心な部分です。`{{custom.access_token}}` は実行時に、前のステップで抽出したトークンに展開されます。これにより「認証 → トークン利用」の連鎖が成立します。

これがマルチステップパターンの中核です。ステップ N で抽出したあらゆる値は、ステップ N+1、N+2、... で名前により参照できます。1ステップで必要なだけ値を抽出でき、任意の深さで連鎖させられます — 認証、ユーザー検索、リソース取得、状態変更のアサート、クリーンアップ、というように。

![Search request step with URL and headers configured](../../img/add-search-request.png)

## トラック ID の抽出

検索レスポンスは `tracks.items` 配列を含む JSON ドキュメントで、各エントリーにはトラック ID、名前、アーティスト、アルバムなどが含まれます。最初にマッチしたトラックの ID を抽出します。

**Validation** セクションを展開し、以下の抽出設定を追加します:

- **Extract** from **Response body** **JSON** **$.tracks.items[0].id** **as** **track.id**

JSONPath `$.tracks.items[0].id` はレスポンスを次のようにたどります: ルート (`$`) から開始し、`tracks` オブジェクトに入り、続いて `items` 配列に入り、最初の要素 (`[0]`) を取り、その `id` フィールドを読み取ります。JSONPath の配列構文は負のインデックス (`[-1]` で最後)、スライス (`[0:5]`)、フィルター式もサポートしており、最初の要素ではなく特定の要素のプロパティをアサートしたい場合に役立ちます。

このワークショップでは ID を抽出しますが、それ以降は使用しません — 実運用のチェックでは、通常 `GET /v1/tracks/{{custom.track.id}}` を呼び出し、レスポンスボディに期待するアーティストとアルバムが含まれていることをアサートする3つ目のステップを追加します。これにより、Spotify のカタログが変わった場合や検索ランキングの品質が低下した場合のリグレッションを検出できます。

![Validation panel with JSONPath extraction for $.tracks.items[0].id configured](../../img/add-search-payload.png)

{{< button style="blue" >}}< Return to test{{< /button >}} をクリックしてテスト設定ページに戻り、{{< button style="blue" >}}Save{{< /button >}} をクリックして API テストを保存します。
