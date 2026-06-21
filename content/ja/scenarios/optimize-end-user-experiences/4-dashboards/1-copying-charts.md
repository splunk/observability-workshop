---
title: チャートのコピーと編集
linkTitle: 1. チャートのコピーと編集
weight: 1
hidden: false
---

ダッシュボードにはすでに良いチャートがありますが、さらにいくつか追加しましょう。

1. 画面左側のダッシュボードアイコンをクリックして Dashboards に移動します。**Browser app health dashboard** を見つけて、Largest Contentful Paint (LCP) チャートまでスクロールします。チャートアクションアイコンをクリックしてフライアウトメニューを開き、「Copy」をクリックしてこのチャートをクリップボードに追加します。
![copy chart](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-04-02/60ea6b19-e024-415f-b3da-4f942f343ec3/user_cropped_screenshot.jpeg?tl_px=179,36&br_px=1899,998&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=524,311)

1. 「add to clipboard」アイコンをクリックすることで、他のチャートもクリップボードに追加し続けることができます。
![copy chart inline icon](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-04-02/c05c55b9-0c3e-47fe-ac83-b945839c513c/user_cropped_screenshot.jpeg?tl_px=0,0&br_px=1540,764&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=723,126)

1. ダッシュボードに追加したいチャートを集め終わったら、右上の「create」アイコンをクリックします。別のブラウザタブでチャートを見ていた場合は、ページをリロードする必要があるかもしれません。
![create icon](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-04-02/9cd17fba-a199-4e2c-9f2a-c692a611630d/user_cropped_screenshot.jpeg?tl_px=0,0&br_px=1388,750&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=969,17)

1. 「Paste charts」メニューオプションをクリックします。
![paste charts](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-04-02/1abb0536-3a91-42e5-ae35-4db1311c7c71/ascreenshot.jpeg?tl_px=1160,476&br_px=2880,1437&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=842,276)

これでチャートのサイズ変更や編集が自由にできるようになりました！

## ボーナス: チャートデータの編集

1. チャートアクションアイコンをクリックし、Open を選択してチャートを編集します。
![chart actions menu](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-04-02/653607e9-5a00-42b3-9fd8-37fe3f9ec6ad/ascreenshot.jpeg?tl_px=792,581&br_px=2512,1542&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=524,276)

1. 既存の Test シグナルを削除します。
![edit the test signal](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-04-02/df0ca0c4-bb5a-4348-a6d3-d0d29c5a2ec5/ascreenshot.jpeg?tl_px=0,775&br_px=1719,1736&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=454,277)

1. {{% button style="blue" %}}Add filter{{% /button %}} をクリックし、`test: *yourInitials*` と入力します。これによりワイルドカードマッチが使用され、あなたのイニシャル（または任意の文字列）を含む、作成したすべてのテストがチャートに取り込まれます。
![add filter button](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-04-02/14a6b9be-2e79-4c30-8a98-7e5f29570560/user_cropped_screenshot.jpeg?tl_px=0,0&br_px=1152,518&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=654,229)

1. ファンクションをクリックして、ディメンションの追加や削除によってデータの表示がどのように変わるかを確認します。たとえば、すべてのテストロケーションデータを集約したい場合は、ファンクションからそのディメンションを削除します。
![test signal functions](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-04-02/0e402434-a302-4df3-9c2d-9a9c16a01524/user_cropped_screenshot.jpeg?tl_px=0,0&br_px=1557,725&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=881,212)

1. チャート名と説明を適切に変更し、「Save and close」をクリックして変更を保存するか、「Close」をクリックして変更をキャンセルします。
![chart close buttons](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-04-02/02bc81af-cd81-4ac4-b1d1-f73cf7e62b99/user_cropped_screenshot.jpeg?tl_px=0,0&br_px=999,644&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=682,162)
