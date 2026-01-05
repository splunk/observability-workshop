---
title: 検索リクエスト
linkTitle: 1.4 Search Request
weight: 4
hidden: false
---

## 検索リクエストの追加

{{< button >}}+ Add Request{{< /button >}} をクリックして次のステップを追加します。ステップ名を **Search for Tracks named "Up around the bend"** とします。

**Request** セクションを展開し、リクエストメソッドを **GET** に変更して、以下の URL を入力します:

``` text
https://api.spotify.com/v1/search?q=Up%20around%20the%20bend&type=track&offset=0&limit=5
```

次に、以下のキー/値のペアで2つのリクエストヘッダーを追加します:

- **CONTENT-TYPE: application/json**
- **AUTHORIZATION: Bearer {{custom.access_token}}**

![Add search request](../../img/add-search-request.png)

**Validation** セクションを展開し、以下の抽出を追加します:

- **Extract** from **Response body** **JSON** **$.tracks.items[0].id** **as** **track.id**

![Add search payload](../../img/add-search-payload.png)

{{< button style="blue" >}}< Return to test{{< /button >}} をクリックしてテスト設定ページに戻ります。次に {{< button style="blue" >}}Save{{< /button >}} をクリックして API テストを保存します。
