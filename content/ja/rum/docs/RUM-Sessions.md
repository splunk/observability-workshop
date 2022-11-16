---
title: RUM Sessionの分析
linkTitle: RUM Sessionの分析
weight: 11
isCJKLanguage: true
---

* RUM UIでRUM Sessionの情報を調査する
* ユーザーインタラクションのSpanでJavascriptのエラーを特定する

---

## 1. cart URLを再び選択

タイムセレクタで時間帯を選択した後、以下のように **Url Name**ビューから *cart* URLを再選択する必要があります。

![RUM-Cart-3](../../images/RUM-Cart-All.png)

上の例では `http://34.246.124.162:81/cart` を選択しました。

## 2. Sessionsにドリルダウン

Tag Spotlightで情報を分析し、トレースのサブセットをドリルダウンした後、エンドユーザーのブラウザーで実行された実際のセッションを表示することができます。

以下のように **Example Sessions** というリンクをクリックすることで行います。

![RUM-Header](../../images/RUM-ExampleSessions.png)

これにより、時間フィルタとタグプロファイルで選択したサブセットの両方に一致するセッションのリストが表示されます。

セッションIDをクリックします。最も長い時間（700 ミリ秒以上が望ましい）のものを選択するとよいでしょう。

![RUM-Header](../../images/RUM-Session-Selected.png)

セッションを選択すると、セッションの詳細ページが表示されます。セッションの一部である特定のアクションを選択しているため、セッション内のどこかのインタラクションにたどり着く可能性が高いです。
先ほど選択したURL `http://34.246.124.162:81/cart` が、セッションストリームでフォーカスしている場所であることがわかります。

![RUM-Session-Tag](../../images/Session-Tag.png)

ページを少し下にスクロールすると、以下のように操作の終わりが表示されます。

![RUM-Session-info](../../images/Session-Tag-2.png)

エンドユーザーには検出されなかったか、または表示されなかった可能性のあるいくつかのJavaScript Consoleエラーが発生していることがわかります。これらのエラーを詳しく調べるには、真ん中のエラー **Cannot read properties of undefined (reading 'Prcie')** をクリックしてください。

![RUM-Session-info](../../images/Session-Tag-3.png)

これによってページが展開され、このインタラクションのSpanの詳細が表示されます。このページには、問題を解決するために開発者に渡すことができる詳細な *error.stack* が含まれます。Online Boutiqueで商品を購入した際、最終的な合計金額が常に0ドルであることにお気づきでしょうか。

![RUM-Session-info](../../images/Session-Tag-4.png)
