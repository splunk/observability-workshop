---
title: 認証リクエスト
linkTitle: 1.3 Authentication Request
weight: 3
---

## 認証リクエストの追加

{{< button >}}+ Add requests{{< /button >}} をクリックし、リクエストステップ名を入力します（例: **Authenticate with Spotify API**）。

![placeholder](../../img/add-request.png)

Request セクションを展開し、ドロップダウンからリクエストメソッドを **POST** に変更して、以下の URL を入力します:

``` text
https://accounts.spotify.com/api/token
```

**Payload body** セクションに以下を入力します:

``` text
grant_type=client_credentials
```

次に、以下のキー/値のペアで2つのリクエストヘッダーを追加します:

- **CONTENT-TYPE: application/x-www-form-urlencoded**
- **AUTHORIZATION: Basic {{env.encoded_auth}}**

**Validation** セクションを展開し、以下の抽出を追加します:

- **Extract** from **Response body** **JSON** **$.access_token** **as** **access_token**

これにより、Spotify API から受信した JSON ペイロードを解析し、アクセストークンを抽出してカスタム変数として保存します。

![Add payload token](../../img/add-payload-token.png)
