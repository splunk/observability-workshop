---
title: APM Trace
linkTitle: 2. APM Trace
weight: 2
---

トレース (trace) を選択するには、`Service Requests & Errors`チャート**(1)**の線を選択します。関連するトレースの選択肢が表示されます。

関連するトレースのリストが表示されたら、青い**(2)** Trace ID Linkをクリックします。選択するトレースがServicesカラムに記載されている3つのサービスと同じものであることを確認してください。

![workflow-trace-pick](../../images/selecting-a-trace.png)

これにより、ウォーターフォール (Waterfall) ビュー (view) で選択されたトレースが表示されます：

ここにはいくつかのセクションがあります：

* Waterfall Pane **(1)**：トレースとスパン (span) として表示されるすべてのインストルメント (instrument) された関数が、その期間表示と順序/関係とともに表示されます。
* Trace Info Pane **(2)**：選択されたスパン情報が表示されます（Waterfall Pane内でスパンの周りにボックスでハイライトされています）。
* Span Pane **(3)**：選択されたスパンで送信されたすべてのタグ (tag) を見つけることができます。下にスクロールしてすべてを確認できます。
* Process Pane：スパンを作成したプロセス (process) に関連するタグが表示されます（スクリーンショットに含まれていないため、下にスクロールして確認してください）。
* Trace Properties：ペインの右上にあり、デフォルトでは折りたたまれています。

![waterfall](../../images/waterfall-view.png)
