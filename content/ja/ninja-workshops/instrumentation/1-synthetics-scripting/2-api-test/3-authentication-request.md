---
title: 認証リクエスト
linkTitle: 1.3 認証リクエスト
weight: 3
---

## ここで行うことの概要

何かをクリックする前に、これからモデル化するOAuth 2フローを確認します。

1. Spotify（他の多くのモダンAPIと同様に）は、認証が必要なすべてのリクエストに短命のBearerトークンを要求します。
2. そのトークンを取得するために、OAuthトークンエンドポイントに対して1回の `POST` を行います。その際、`client_id:client_secret`（Base64エンコード済み）をHTTP Basic認証ヘッダーに、`grant_type=client_credentials` をボディに含めて送信します。これが **Client Credentials grant** です。OAuth 2のマシン間通信用バリアントであり、ログインユーザーの代わりではなく、バックエンドサービス自身の代わりにAPIを呼び出す必要がある場合に設計されています。
3. SpotifyはJSON形式で `access_token` を含むレスポンスを返します。それを抽出し、Synthetic Monitoringの **カスタム変数** として保存し、以降のすべてのリクエストで `Authorization: Bearer …` ヘッダーとして使用します。

このパターンは、ほとんどのモダンAPIがサービス間トラフィックを認証する方法と同じです。ここで構築するものは、OAuth保護されたバックエンドを監視するためのテンプレートとして活用できます。

## 認証リクエストの追加

{{< button >}}+ Add requests{{< /button >}} をクリックし、リクエストステップ名に **Authenticate with Spotify API** と入力します。ここでわかりやすい名前が重要なのは、RBTの場合と同じ理由です。ステップが失敗した際、アラートメッセージにこの名前がそのまま使われます。

![ステップ名フィールドが入力された新しいAPIリクエスト](../../img/add-request.png)

**Request** セクションを展開し、リクエストメソッドをドロップダウンから **POST** に変更して、URLを入力します。

``` text
https://accounts.spotify.com/api/token
```

**Payload body** セクションに以下を入力します。

``` text
grant_type=client_credentials
```

`grant_type=client_credentials` の値は、使用するOAuthフローをSpotifyに伝えます。ボディは `application/x-www-form-urlencoded` 形式です。これはレガシーなフォームポストエンコーディングであり、OAuthトークンエンドポイントの標準です（APIボディでJSONが広く使われるようになる前から存在しています）。

次に、以下のキー/値のペアで2つのリクエストヘッダーを追加します。

- **CONTENT-TYPE: application/x-www-form-urlencoded** — 先ほど指定したボディの解析方法をSpotifyに伝えます。
- **AUTHORIZATION: Basic {{env.encoded_auth}}** — 前の章で設定したワークショップの事前構成済みグローバル変数で、テストランナーによってインラインで展開されます。ランナーはリテラルのBase64文字列を送信し、変数名がネットワーク上に露出することはありません。

## アクセストークンの抽出

トークンリクエストが成功した場合のSpotifyのレスポンスは以下のようになります。

``` json
{
  "access_token": "BQDxx...long-opaque-string...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

次のステップで `access_token` の値が必要です。リクエストの **Validation** セクションを展開し、以下の抽出を追加します。

- **Extract** from **Response body** **JSON** **$.access_token** **as** **access_token**

`$.access_token` は [**JSONPath**](https://goessner.net/articles/JsonPath/) 式です。JSONにおけるXPathに相当するものです。`$` はドキュメントのルートを表し、`.access_token` はトップレベルのフィールドを選択します。JSONPathは配列のインデックス、ワイルドカード、フィルターもサポートしています。配列形式は次の章で使用します。

抽出された値は、以降のすべてのステップで `{{custom.access_token}}` として利用可能になります。`custom.` 名前空間は、この実行 *中に* 生成された変数用であり、組織レベルの静的な値を格納する `env.` 名前空間とは異なります。

![$.access_tokenのJSONPath抽出が設定されたValidationパネル](../../img/add-payload-token.png)
