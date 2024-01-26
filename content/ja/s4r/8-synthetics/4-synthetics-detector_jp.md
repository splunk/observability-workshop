---
title: 4. Synthetics Detector
weight: 4
---

これらのテストを24時間365日実行できるため、テストが失敗したり所定のSLAよりも時間がかかり始めた場合には、ソーシャルメディアやアップタイムのウェブサイトから通知される前に早期に警告を受ける理想的なツールです。

![Social media](../images/social-media-post.png)

それを防ぐために、テストが1.1分以上かかる場合に検出しましょう。

{{% notice title="実習" style="green" icon="running" %}}

* Syntheticsのホームページに戻ります（左のメニューから）。
* ワークショップのテストを再選択し、ページの上部にある {{% button style="white" %}}Create Detector{{% /button %}} ボタンをクリックします。
  ![synth detector](../images/synth-detector.png)
* テキスト **New Synthetics Detector** を編集し、`INITIALS - [WORKSHOPNAME]` に置き換えます。
* {{% button %}}Run duration{{% /button %}} と {{% button %}}Static threshold{{% /button %}} が選択されていることを確認します。
* **Trigger threshold** （**2**）を `65,000` から `68,000` 程度に設定し、Enter キーを押してグラフを更新します。上記のように、しきい値線を貫通するスパイクが複数あることを確認してください（実際の遅延に合わせてしきい値を調整する必要があるかもしれません）。
* それ以外はデフォルトのままにします。
* これで、スパイクの下に赤と白の三角形の列が表示されるようになります（**3**）。赤い三角形は、テストが指定されたしきい値を超えていたことを示し、白い三角形は指定されたしきい値を下回っていたことを示します。赤い三角形ごとにアラートがトリガーされます。
* アラートの重大度（**4**）やアラートの方法を変更できます。 アラートの受信者を追加しないでください。これにより、アラートの嵐にさらされる可能性があります！
* {{% button style="blue" %}}Activate{{% /button %}} をクリックしてディテクターを展開します。
* 作成したディテクターを表示するには、{{% button style="white" %}}Edit Test{{% /button %}} ボタンをクリックします。
* ページの一番下にアクティブなディテクターのリストがあります。

  ![list of detectors](../images/detector-list.png)

* 自分のものが見つからない場合は、*New Synthetic Detector* という名前のものが表示され、名前が正しく保存されていない可能性があります。*New Synthetic Detector* リンクをクリックして、名前を再度変更してください。
* 編集モードを終了するには {{% button %}}Close{{% /button %}} ボタンをクリックします。
{{% /notice %}}
