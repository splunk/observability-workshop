---
title: Petclinic アプリの RUM ビューを選択する
linkTitle: 1. RUM データを確認する
weight: 1
---

まずは RUM の概要をざっと見ていきましょう。左側のメニューから **RUM** をクリックしてください。次に **Environment** フィルター **(1)** を、ドロップダウンボックスからワークショップインスタンスの名前に変更し、**`<INSTANCE>-workshop`** **(1)** を選択します（**`INSTANCE`** は先ほど実行したシェルスクリプトの値です）。これだけが選択されている状態にしてください。

続いて、**App** **(2)** ドロップダウンボックスをアプリの名前（**`<INSTANCE>-store`**）に変更します。

![rum select](../../images/rum-env-select.png)

**Environment** と **App** を選択すると、アプリケーションの RUM ステータスを示す概要ページが表示されます。（Summary Dashboard が数値の 1 行だけになっている場合は、縮小表示の状態です。アプリケーション名の前にある **> (1)** をクリックして展開できます。）JavaScript エラーが発生していた場合は、以下のように表示されます。

![rum overview](../../images/rum-overview.png)

続けるには、青いリンク（ワークショップ名が表示されているもの）をクリックして詳細ページに移動します。すると、UX Metrics、Front-end Health、Back-end Health、Custom Events ごとにインタラクションを分解し、過去のメトリクス（デフォルトでは 1 時間）と比較する新しいダッシュボードビューが表示されます。

![rum  main](../../images/rum-main.png)
通常、最初のチャートには 1 本の線だけが表示されます。Petclinic ショップに関連するリンクをクリックしてください。この例では <http://198.19.249.202:81> です。

これにより、Tag Spotlight ページに移動します。
