---
title: 1.5 Advanced 設定
weight: 5
---

**Advanced** をクリックします。これらの設定はオプションで、テストをさらに詳細に構成するために使用できます。

{{% notice note %}}
このワークショップでは、これらの設定は情報提供のみを目的としており、実際には使用しません。
{{% /notice %}}

![Advanced Settings](../../img/advanced-settings.png)

- **Security**:
  - **TLS/SSL validation**: 有効にすると、SSL/TLS証明書の有効期限切れ、無効なホスト名、信頼できない発行者の検証を強制します
  - **Authentication**: 企業ネットワーク内など、追加のセキュリティプロトコルを必要とするサイトで認証するための資格情報を追加します。Authenticationフィールドで [concealed global variables](https://docs.splunk.com/Observability/synthetics/test-config/global-variables.html) を使用することで、資格情報のセキュリティレイヤーを追加し、チェック間で資格情報を共有しやすくなります
- **Custom Content**:
  - **Custom headers**: 各リクエストで送信するカスタムヘッダーを指定します。たとえば、リクエストに特定のヘッダーを送信することで、バックエンドの分析からリクエストを除外するヘッダーを追加できます。カスタムヘッダーを使用してCookieを設定することもできます
  - **Cookies**: テスト開始前にブラウザにCookieを設定します。たとえば、ポップアップモーダルがランダムに表示されてテストに干渉するのを防ぐためにCookieを設定できます。設定されたCookieは、チェックの開始URLのドメインに適用されます。Splunk Synthetics Monitoringはpublic suffix listを使用してドメインを判定します
  - **Host overrides**: あるホストから別のホストにリクエストをリルーティングするホストオーバーライドルールを追加します。たとえば、既存の本番サイトを開発サイトや特定のCDNエッジノードから読み込まれたページリソースに対してテストするホストオーバーライドを作成できます

次に、テストステップを編集して、各ステップにより意味のある名前を付けます。
