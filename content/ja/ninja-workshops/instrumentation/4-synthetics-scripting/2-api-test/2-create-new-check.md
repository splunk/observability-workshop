---
title: Create new API test
linkTitle: 1.2 Create new API test
weight: 2
---

{{< step "Create a new API test" "1" >}}

**Synthetics** ランディングページから {{< button style="blue" >}}Add new test{{< /button >}} をクリックし、ドロップダウンから **API test** を選択します。

テスト名には、**ご自身のイニシャル** に続けて **Spotify API** を付けてください（例: **RWC - Spotify API**）。Part 1 と同じ命名規則を踏襲します。共有組織内でテストを見つけやすくするためにイニシャルをプレフィックスとして付け、アラートメッセージだけで内容が把握できるようにテスト対象システム名も含めます。

![Add new API test dialog with the test name field filled in](../../img/new-api-check.png)

{{< button style="blue" >}}Submit{{< /button >}} をクリックすると、**API Test content** ページに遷移します。このページで、シンセティックなビジネストランザクションを構成する 2 つのリクエストを追加していきます。

1. **Authenticate with Spotify API** — OAuth トークンエンドポイントへの `POST` リクエストで、クライアントクレデンシャルをアクセストークンと交換し、そのトークンをカスタム変数として抽出・保存します。
2. **Search for tracks** — 検索エンドポイントへの `GET` リクエストで、ステップ 1 で取得したトークンを Bearer クレデンシャルとして送信し、JSON レスポンスから項目を抽出します。

次の 2 つの章で、これらを 1 つずつ構築していきます。

{{</ step >}}
