---
title: Authentication Request
linkTitle: 1.3 Authentication Request
weight: 3
---

## これから行う内容について

クリックを始める前に、ここでモデル化する OAuth 2 フローを確認しておきます。

1. Spotify は（最近の多くの API と同様に）認証付きリクエストごとに短命の bearer token を要求します。
2. このトークンを取得するため、OAuth トークンエンドポイントに対して 1 回だけ `POST` を行います。HTTP Basic 認証ヘッダーに `client_id:client_secret`（Base64 エンコード済み）を、ボディに `grant_type=client_credentials` を含めて送信します。これが **Client Credentials grant** と呼ばれるもので、OAuth 2 のマシン間通信向けバリアントであり、ログイン中のユーザーに代わってではなく、自分自身として API を呼び出す必要があるバックエンドサービス向けに設計されています。
3. Spotify は `access_token` を含む JSON を返します。これを抽出して Synthetic Monitoring の **custom variable** として保存し、以降のすべてのリクエストで `Authorization: Bearer …` ヘッダーとして使用します。

これは、最近の多くの API がサービス間トラフィックを認証する際の共通パターンなので、ここで構築する内容はあらゆる OAuth で保護されたバックエンドを監視するためのテンプレートになります。

## 認証リクエストを追加する

{{< button >}}+ Add requests{{< /button >}} をクリックし、リクエストステップ名に **Authenticate with Spotify API** と入力します。意味のある名前を付けることは、RBT と同じ理由でここでも重要です。ステップが失敗したときに、アラートメッセージはこの名前をそのまま使用します。

![ステップ名フィールドを入力した新しい API リクエスト](../../img/add-request.png)

**Request** セクションを展開し、ドロップダウンからリクエストメソッドを **POST** に変更して、URL を入力します。

``` text
https://accounts.spotify.com/api/token
```

**Payload body** セクションには次の内容を入力します。

``` text
grant_type=client_credentials
```

`grant_type=client_credentials` という値は、どの OAuth フローを使用するかを Spotify に伝えます。ボディは `application/x-www-form-urlencoded`（古くから使われているフォームポストのエンコーディング）で、これは OAuth トークンエンドポイントの標準です（API ボディで JSON が広く使われるようになるよりも前から存在しています）。

次に、以下のキー/値ペアでリクエストヘッダーを 2 つ追加します。

- **CONTENT-TYPE: application/x-www-form-urlencoded** — 先ほど指定したボディをどのように解析するかを Spotify に伝えます。
- **AUTHORIZATION: Basic {{env.encoded_auth}}** — 前章で設定したワークショップ用のグローバル変数で、テストランナーによってインラインで展開されます。ランナーは Base64 文字列そのものを送信し、変数名がネットワーク上に流れることはありません。

## アクセストークンを抽出する

トークンリクエストが成功したときの Spotify のレスポンスは、おおよそ次のような形になります。

``` json
{
  "access_token": "BQDxx...long-opaque-string...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

次のステップでは `access_token` の値が必要になります。リクエストの **Validation** セクションを展開し、以下の抽出設定を追加します。

- **Extract** from **Response body** **JSON** **$.access_token** **as** **access_token**.

`$.access_token` は [**JSONPath**](https://goessner.net/articles/JsonPath/) 式で、XPath の JSON 版にあたります。`$` がドキュメントのルートを表し、`.access_token` でトップレベルのフィールドを選択します。JSONPath は配列のインデックス指定、ワイルドカード、フィルターもサポートしており、配列形式は次章で使用します。

抽出された値は、以降のすべてのステップから `{{custom.access_token}}` として参照できます。`custom.` 名前空間はこの実行中に生成された変数のためのもので、組織レベルの静的な値のための `env.` 名前空間とは対照的です。

![$.access_token に対する JSONPath 抽出が設定された Validation パネル](../../img/add-payload-token.png)
