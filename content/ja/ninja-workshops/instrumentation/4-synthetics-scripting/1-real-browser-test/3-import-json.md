---
title: 1.3 JSONのインポート
weight: 3
---

テストの構成を開始するには、Chrome DevTools Recorder からエクスポートした JSON ファイルをインポートする必要があります。Splunk Synthetic Monitoring は Recorder のネイティブな JSON 形式を直接理解できるため、変換手順は不要です。インポーターが記録された各ステップを読み取り、対応する Synthetic テストステップを作成し、セレクター、ビューポート、アサートされたナビゲーションイベントを保持します。

{{% button %}}**Import**{{% /button %}} ボタンを有効化するには、まずテストに名前を付ける必要があります。記録時と同じ命名規則を使用してください。イニシャルの後にジャーニー名を続けます。例えば **`<your initials>` - Online Boutique** のようにします。イニシャルを接頭辞として付けることで、共有された組織内でトレーナーやチームメンバーがお互いの作業を見つけやすくなります。

![Import](../../img/import.png)

{{% button %}}**Import**{{% /button %}} ボタンが有効になったら、それをクリックし、Chrome DevTools Recorder からエクスポートした JSON ファイルをドロップするか、ブラウズして選択してください。

![Import JSON](../../img/import-json.png)

JSON が解析されると、インポートされたステップ数を示す緑色の確認メッセージが表示されます。ここで予期したよりも少ない数が表示された場合、通常は記録されたアクションのいずれかが Synthetics インポーターが認識できる形式ではなかったことを意味します。その特定のインタラクションを再記録すると、通常は解決します。

{{% button style="blue" %}}Continue to edit steps{{% /button %}} をクリックします。

![Import Complete](../../img/import-complete.png)

**Edit steps** ビューには、インポートされた各ステップが順番に表示され、アクションタイプ、ターゲットセレクター、待機条件などが確認できます。ここからステップを並べ替えたり、追加したり、削除したりできますが、それについては後のセクションで扱います。

![Edit Steps](../../img/edit-steps.png)

ステップ自体を編集する前に、まずテストの実行時設定を構成しましょう。どこから実行するか、どの程度の頻度で実行するか、どのデバイスで実行するかを設定します。{{% button style="blue" %}}< Return to test{{% /button %}} をクリックしてください。
