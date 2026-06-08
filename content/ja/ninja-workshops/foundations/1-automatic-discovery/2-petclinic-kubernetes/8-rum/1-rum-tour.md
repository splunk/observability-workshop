---
title: Petclinic アプリの RUM ビューを選択する
linkTitle: 1. RUM データの確認
weight: 1
---

左側のメニューで **Digital Experience → Real user monitoring → Overview** をクリックして、RUM の概要を簡単に確認しましょう。次に、**Environment** フィルター **(1)** をドロップダウンボックスからワークショップインスタンスの名前に変更し、**`<INSTANCE>-workshop`** **(1)** を選択します（**`INSTANCE`** は先ほど実行したシェルスクリプトの値です）。それだけが選択されていることを確認してください。

次に、**App** **(2)** ドロップダウンボックスをアプリの名前に変更します。**`<INSTANCE>-store`** になります。

![rum select](../../images/rum-env-select.png)

**Environment** と **App** を選択すると、アプリケーションの RUM ステータスを示す概要ページが表示されます。（Summary Dashboard が単一行の数値だけの場合は、簡略表示になっています。アプリケーション名の前にある **> (1)** をクリックして展開できます）。JavaScript エラーが発生した場合は、以下のように表示されます

![rum overview](../../images/rum-overview.png)

続けるには、青いリンク（ワークショップ名が表示されています）をクリックして詳細ページに移動します。これにより、UX Metrics、Front-end Health、Back-end Health、Custom Workflows ごとにインタラクションを分類し、過去のメトリクスと比較する新しいダッシュボードビューが表示されます。

![rum  main](../../images/rum-main.png)
通常、最初のチャート内には1行だけ表示されます。Petclinic ショップに関連するリンクをクリックしてください。この例では
<http://198.19.249.202:81> です

これにより、Tag Spotlight ページに移動します。
