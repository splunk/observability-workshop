---
title: 4. Synthetics Detector
weight: 4
---

これらのテストは24時間365日実行できます。そのため、テストが失敗したり所定のSLAよりも処理時間がかかるようになりつつある場合に早期に警告を受けることができる理想的なツールです。ソーシャルメディアやウェブサイトの稼働チェックサイトなどから状態を通知されるような事態を防ぐことができます。

![Social media](../images/social-media-post.png)

それでは、テストが1.1分以上かかる場合にエラーを検出しましょう。

{{% notice title="Exercise" style="green" icon="running" %}}

* 左のメニューから Synthetics のホームページに戻ります。
* ワークショップのテストをもう一度選択し、ページの上部の {{% button style="white" %}}Create Detector{{% /button %}} ボタンをクリックします。
  ![synth detector](../images/synth-detector.png)
* **New Synthetics Detector** (**1**) と表示されているテキストを編集し、`<受講者のイニシャル> - [WORKSHOPNAME]` に置き換えます。
* 次に、{{% button %}}Run duration{{% /button %}} と {{% button %}}Static threshold{{% /button %}} が選択されていることを確認します。
* **Trigger threshold** （**2**）を `65,000` から `68,000` 程度に設定し、Enter キーを押してグラフを更新します。上記のように、しきい値を超えるスパイクが複数あることを確認してください（実際の処理時間に合わせてしきい値を調整する必要があるかもしれません）。
* それ以外はデフォルトのままにします。
* これで、スパイクの下に赤と白の三角形の列が表示されるようになります（**3**）。赤い三角形は、テストが指定されたしきい値を超過したことを示し、白い三角形は指定されたしきい値以下に戻ったことを示します。赤い三角形ごとにアラートがトリガーされます。
* アラートの重大度（**4**）やアラートの方法を変更できます。 アラート受信者は追加しないでください。大量のアラート通知にさらされる可能性があります！
* Detector を有効化するために、{{% button style="blue" %}}Activate{{% /button %}} をクリックします。
* 作成した Detector を表示するには、{{% button style="white" %}}Edit Test{{% /button %}} ボタンをクリックします。
* ページの一番下にアクティブな Detector のリストがあります。

  ![list of detectors](../images/detector-list.png)

* 自分のものが見つからない場合は、*New Synthetic Detector* という名前のものが表示され、名前が正しく保存されていない可能性があります。*New Synthetic Detector* リンクをクリックして、名前を再度変更してください。
* 編集モードを終了するには {{% button %}}Close{{% /button %}} ボタンをクリックします。
{{% /notice %}}
