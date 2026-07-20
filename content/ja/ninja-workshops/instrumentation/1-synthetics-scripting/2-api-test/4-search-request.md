---
title: Search Request
linkTitle: 1.4 Search Request
weight: 4
hidden: false
---

## 検索リクエストの追加

有効なアクセストークンを取得できたので、それを使用します。 {{< button >}}+ Add Request{{< /button >}} をクリックして次のステップを追加します。ステップ名を **Search for tracks named "Up around the bend"** にします。

これは[Spotify Search endpoint](https://developer.spotify.com/documentation/web-api/reference/search)です。クエリ文字列パラメータは、"Up around the bend"というフレーズに一致するトラック（`type=track`）を検索し、最初の結果から開始（`offset=0`）して、最大5件（`limit=5`）を返すことを指定しています。SpotifyはクエリフレーズをURLエンコードするため、スペースは `%20` になります。

**Request** セクションを展開し、リクエストメソッドを **GET** に変更して、URLを入力します。

``` text
https://api.spotify.com/v1/search?q=Up%20around%20the%20bend&type=track&offset=0&limit=5
```

次に、以下のキー/値のペアで2つのリクエストヘッダーを追加します。

- **CONTENT-TYPE: application/json** — リクエストボディの形式を宣言します。厳密にはGETリクエストにはボディがないため、このヘッダーは情報提供のみですが、送信しても問題なくSpotifyもエラーにしません。
- **AUTHORIZATION: Bearer {{custom.access_token}}** — ここが重要なポイントです。 `{{custom.access_token}}` は実行時に前のステップで抽出したトークンに展開されるため、「認証 → トークン使用」のチェーンが接続されます。

これがマルチステップパターンの核心です。ステップNで抽出された値は、ステップN+1、N+2などで名前で利用できます。ステップごとに必要なだけ値を抽出でき、任意の深さでチェーンできます（認証、ユーザー検索、リソース取得、状態変更のアサーション、クリーンアップなど）。

![URLとヘッダーが設定された検索リクエストステップ](../../img/add-search-request.png)

## トラックIDの抽出

検索レスポンスは `tracks.items` 配列を含むJSONドキュメントで、各エントリにはトラックID、名前、アーティスト、アルバムなどが含まれています。最初に一致したトラックのIDを抽出します。

**Validation** セクションを展開し、以下の抽出を追加します。

- **Extract** from **Response body** **JSON** **$.tracks.items[0].id** **as** **track.id**

JSONPath `$.tracks.items[0].id` はレスポンスを次のように走査します。ルート（`$`）から開始し、 `tracks` オブジェクトに入り、次に `items` 配列に入り、最初の要素（`[0]`）を取得して、その `id` フィールドを読み取ります。JSONPathの配列構文は、負のインデックス（`[-1]` で最後の要素）、スライス（`[0:5]`）、フィルター式もサポートしており、最初の項目だけでなく特定の項目のプロパティをアサートしたい場合に便利です。

このワークショップではIDを抽出しますが再利用しません。本番チェックでは通常、 `GET /v1/tracks/{{custom.track.id}}` を呼び出す3番目のステップを追加し、レスポンスボディに期待するアーティストとアルバムが含まれていることをアサートします。これにより、Spotifyのカタログが変更されたり検索ランキングが低下した場合のリグレッションを検出できます。

![$.tracks.items[0].idのJSONPath抽出が設定されたValidationパネル](../../img/add-search-payload.png)

{{< button style="blue" >}}< Return to test{{< /button >}} をクリックしてテスト設定ページに戻り、 {{< button style="blue" >}}Save{{< /button >}} をクリックしてAPIテストを保存します。
