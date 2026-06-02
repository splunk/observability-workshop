---
title: Global Variables
linkTitle: 1.1 Global Variables
weight: 1
---

## グローバル変数とは

Splunk Synthetic Monitoring の [**global variables**](https://docs.splunk.com/Observability/synthetics/test-config/global-variables.html) は、組織レベルでスコープされた再利用可能な値です。値を一度定義すれば、任意のテストから名前で参照できます。グローバル変数を使う主な理由は次の 2 つです。

- **重複の回避。** API キー、テナント ID、ベース URL、テスト用ユーザー名など、複数のテストに登場する値はグローバル変数に格納することで、変更時に 1 か所で更新できます。
- **シークレットの秘匿。** 変数は **concealed** としてマークでき、その場合は値が UI 上で隠され、テスト定義を閲覧する誰からも見えなくなります。concealed 変数はテストから参照可能ですが（テストランナーはアクセスできます）、設定から値を読み戻すことはできません。API キー、OAuth クライアントシークレット、HTTP Basic 認証情報を保存する適切な方法です。

カスタム変数は次の 2 つの章で扱いますが、これとは異なります。カスタム変数はテスト実行*中*に、あるレスポンスから値を抽出して設定し、後続のステップで使用します。グローバル変数は静的、カスタム変数は動的であり、両者を組み合わせることで必要なデータ受け渡しパターンの大半をカバーできます。

## ワークショップ用に事前設定されたグローバル変数を確認する

このワークショップでは、`env.encoded_auth` という名前のグローバル変数が事前に 1 つ設定されています。これは Spotify API クライアントの `client_id:client_secret` を Base64 エンコードした値で、Spotify の [Client Credentials OAuth flow](https://developer.spotify.com/documentation/web-api/tutorials/client-credentials-flow) においてトークンリクエストの `Authorization: Basic …` ヘッダーに要求される形式そのものです。

Synthetics ページの右上にある歯車アイコンをクリックし、**Global Variables** を選択して一覧を表示します。`env.encoded_auth` が表示されているはずです。

![Global Variables list with env.encoded_auth shown](../../img/global-variables.png)

変数名の `env.` プレフィックスに注目してください。グローバル変数は `env.` 名前空間に属し、テストからは `{{env.encoded_auth}}` として参照します。カスタム変数（テスト実行中に作成します）は `custom.` 名前空間に属し、`{{custom.access_token}}` のように参照します。

ここで編集する必要はありません。次の 2 つの章で、認証リクエストからこの変数を参照します。
