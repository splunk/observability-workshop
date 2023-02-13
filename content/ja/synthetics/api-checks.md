---
title: API Checks
linkTitle:  2. API Checks
weight: 2
isCJKLanguage: true
---

API Checkは、APIエンドポイントの機能およびパフォーマンスをチェックする柔軟な方法を提供します。APIファーストの開発へのシフトにより、フロントエンドのコア機能を提供するバックエンドサービスを監視する必要性が高まっています。複数ステップのAPIインタラクションのテストに興味がある場合でも、エンドポイントのパフォーマンスを可視化したい場合でも、API Checkは目標の達成に役立ちます。

## 1. グローバル変数の作成

API Checkを行うために使用するグローバル変数を表示します。 **Admin Tools** の下にある **Global Variables** をクリックします。 spotifyのAPIトランザクションを行うために使用するグローバル変数を確認してください。

![placeholder](../images/global-variable.png)

## 2. API Check の作成

新しい API Check を作成し、`<あなたのイニシャル>` の後に Splunk REST API Check をつけた名前にします （例: **AP - Spotify API**）

![placeholder](../images/new-api-check.png)

チェックに名前を付けたら、notificationタブを開いて、どのような設定があるか眺めてみましょう。

次に、以下のAPI Check Stepsを追加します。

 ![placeholder](../images/api-check-steps.png)

変数はこちらから選ぶことができます:

![placeholder](../images/available-variables.png)

**[Request Step](https://help.rigor.com/hc/en-us/articles/115004583747-API-Check-Request-Step)**

- リクエストステップは、あるエンドポイントにHTTPリクエストを行い、そのレスポンスからデータを取得します。他のチェックタイプとは異なり、APIチェックでは、チェックを開始するための初期URLは必要ありません。すべてのHTTPリクエストは、リクエストステップ内で設定されます。

**[Extract Step](https://help.rigor.com/hc/en-us/articles/115004582607-API-Check-Extract-Step)**

- Extractステップでは、JSON、XML、HTML形式のデータからデータを抽出します。

- JSONからデータを抽出するには、次の3つを用意します:

- JSONを含むソース

- データを抽出するためのJSONPath式

- 保存先のカスタム変数名

- ソースはどのようなJSONでもかまいませんが、たいていはレスポンスのBodyから取得するでしょう。レスポンスヘッダから取得することもできますし、また、カスタムの値も可能です。ソースは、整形されたJSONでなければなりません。

**[Save Step](https://help.rigor.com/hc/en-us/articles/115004743868-API-Check-Save-Step)**

- Saveステップでは、チェックの後で再利用するためのデータを保存します。データを保存するには、ソースと保存先のカスタム変数名を指定します。ソースは、応答ヘッダを含むプリセットから選択するか、カスタム値を指定します。

- その他の使用例としては、他のステップで簡単に再利用できるように情報を追加したり、リクエストの結果を保存して別のリクエストで再利用できるようにするなどがあります。

- リクエスト変数は、リクエストが作成された後にのみ使用可能であることを覚えておくことが重要です。もし、リクエストから値を保存しようとしても、まだリクエストを行っていない場合は、空の文字列が保存されます。

**[Assert Step](https://help.rigor.com/hc/en-us/articles/115004742408-API-Check-Assert-Step)**

- Assertステップは、2つの値に対してアサーションを行います。アサーションを行うには、2つのパラメータと、その2つの比較方法を指定します。

**[Comparisons](https://help.rigor.com/hc/en-us/articles/115004742408-API-Check-Assert-Step)**

- 現在、**string（文字列）**、 **numeric（数値）**、**regular expression（正規表現）** の3種類の比較をサポートしています。

- **string** と **numeric** では、値が比較タイプに強制されます。

- **reqular expression** での比較の場合、最初のパラメータは文字列で、2番目のパラメータは正規表現になります。

API Check に Splunk と API のタグを付けて SAVE します。

![placeholder](../images/tags.png)

## 3. REST API Checkのテスト

edit configuration に戻り、ページの下にある 'test' を押して、エラーがないことを確認します。

![placeholder](../images/test-api-check.png)

ウィンドウを上にスライドさせると、正常に実行された場合の詳細が表示されます

![placeholder](../images/successful-run.png)

![placeholder](../images/request-step.png)

さて、モニターにもう少し機能を追加してみましょう。詳細ウィンドウを下にスライドさせ、手順5～8を追加します。

**BONUS**：ステップ6を使用して、以下のレスポンスがタイムリーに戻ってきたことをアサートします（1000 ms)

![placeholder](../images/additional-steps.png)

ステップを追加したら、モニターをテストして保存します。

## 4. リソース

- [How to Create an API Check](https://help.rigor.com/hc/en-us/articles/115004817308-How-to-Create-an-API-Check)

- [API Check Overview](https://help.rigor.com/hc/en-us/articles/115004952508-API-Check-Overview)

- [How Do I Use Business Transactions?](https://help.rigor.com/hc/en-us/articles/360049442854-How-Do-I-Use-Business-Transactions)
