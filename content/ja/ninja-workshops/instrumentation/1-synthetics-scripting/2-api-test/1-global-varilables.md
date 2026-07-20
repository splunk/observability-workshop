---
title: グローバル変数
linkTitle: 1.1 グローバル変数
weight: 1
---

## グローバル変数とは

Splunk Synthetic Monitoringの [**global variables**](https://docs.splunk.com/Observability/synthetics/test-config/global-variables.html) は、組織レベルで再利用可能な値です。一度値を定義すれば、任意のテストから名前で参照できます。グローバル変数を使用する主な理由は次の2つです。

- **重複の回避。** APIキー、テナントID、ベースURL、テスト用ユーザー名など、複数のテストで使用する値はグローバル変数に格納することで、変更時に一箇所だけ更新すれば済みます。
- **シークレットの隠蔽。** 変数は **concealed** としてマークでき、UIで値が隠され、テスト定義を閲覧する人には表示されません。Concealedな変数はテストから引き続き参照可能で、テストランナーはアクセスできますが、設定から値を読み取ることはできません。APIキー、OAuthクライアントシークレット、HTTP Basic認証の資格情報を保存するのに適した方法です。

カスタム変数（次の2つの章で紹介します）は異なります。テスト実行 *中に* レスポンスから値を抽出して設定し、後続のステップで使用します。グローバル変数は静的で、カスタム変数は動的です。この2つを組み合わせることで、必要なデータ受け渡しパターンのほとんどをカバーできます。

## ワークショップで事前設定されたグローバル変数を確認する

このワークショップでは、`env.encoded_auth` という名前のグローバル変数が事前に設定されています。この変数には、Spotify APIクライアントの `client_id:client_secret` をBase64エンコードした値が含まれています。これはSpotifyの [Client Credentials OAuthフロー](https://developer.spotify.com/documentation/web-api/tutorials/client-credentials-flow) がトークンリクエストの `Authorization: Basic …` ヘッダーで期待する形式です。

Syntheticsページの右上にある歯車アイコンをクリックし、**Global Variables** を選択してリストを表示します。`env.encoded_auth` が表示されます。

![env.encoded_authが表示されたGlobal Variablesリスト](../../img/global-variables.png)

変数名の `env.` プレフィックスに注目してください。グローバル変数は `env.` 名前空間に属し、テストからは `{{env.encoded_auth}}` として参照します。カスタム変数（テスト実行中に作成します）は `custom.` 名前空間に属し、`{{custom.access_token}}` として参照します。

ここでは何も編集する必要はありません。次の2つの章で、認証リクエストからこの変数を参照します。
