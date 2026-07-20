---
title: 新しいAPIテストの作成
linkTitle: 1.2 新しいAPIテストの作成
weight: 2
---

{{< step "新しいAPIテストを作成する" "1" >}}

**Synthetics** のランディングページから、 {{< button style="blue" >}}Add new test{{< /button >}} をクリックし、ドロップダウンから **API test** を選択します。

**自分のイニシャル** に続けて **Spotify API** を使ってテストに名前を付けます。例: **RWC - Spotify API** 。Part 1と同じ命名規則が適用されます。共有組織内でテストを見つけやすくするためにイニシャルをプレフィックスとして付け、アラートメッセージが自己説明的になるようにテスト対象のシステム名を含めます。

![テスト名フィールドが入力された新しいAPIテストダイアログ](../../img/new-api-check.png)

{{< button style="blue" >}}Submit{{< /button >}} をクリックすると、 **API Test content** ページに移動します。ここで、合成ビジネストランザクションを構成する2つのリクエストを追加します。

1. **Authenticate with Spotify API** — OAuthトークンエンドポイントへの `POST` で、クライアント資格情報をアクセストークンに交換し、それをカスタム変数として抽出・保存します。
2. **Search for tracks** — 検索エンドポイントへの `GET` で、ステップ1のトークンをBearer資格情報として送信し、JSONレスポンスからアイテムを抽出します。

次の2つのチャプターで、1つずつ構築していきます。

{{</ step >}}
