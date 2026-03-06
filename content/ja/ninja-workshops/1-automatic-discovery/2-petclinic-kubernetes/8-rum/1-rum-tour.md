---
title: Select the RUM view for the Petclinic App
linkTitle: 1. Verify RUM Data
weight: 1
---

左側のメニューで **RUM** をクリックして、RUMの簡単な概要ツアーを始めましょう。次に、**Environment** フィルター **(1)** をドロップダウンボックスから変更し、ワークショップインスタンスの名前 **`<INSTANCE>-workshop`** **(1)** を選択します (ここで **`INSTANCE`** は、以前に実行したシェルスクリプトの値です)。これのみが選択されていることを確認してください。

次に、**App** **(2)** ドロップダウンボックスをアプリの名前に変更します。これは **`<INSTANCE>-store`** になります。

![rum select](../../images/rum-env-select.png)

**Environment** と **App** を選択すると、アプリケーションのRUMステータスを示す概要ページが表示されます。(Summary Dashboardが単一行の数値だけの場合は、縮小表示になっています。アプリケーション名の前にある **> (1)** をクリックして展開できます)。JavaScriptエラーが発生した場合は、以下のように表示されます:

![rum overview](../../images/rum-overview.png)

続けるには、青いリンク (ワークショップ名) をクリックして詳細ページに移動します。これにより、UX Metrics、Front-end Health、Back-end Health、Custom Eventsによるインタラクションの内訳が表示され、過去のメトリクス (デフォルトでは1時間) と比較される新しいダッシュボードビューが表示されます。

![rum  main](../../images/rum-main.png)
通常、最初のチャートには1つの線のみがあります。Petclinicショップに関連するリンクをクリックしてください。
この例では http://198.19.249.202:81 です:

これにより、Tag Spotlightページに移動します。
