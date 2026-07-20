---
title: 1.3 JSONのインポート
weight: 3
---

テストの設定を開始するには、Chrome DevTools RecorderからエクスポートしたJSONファイルをインポートする必要があります。Splunk Synthetic MonitoringはレコーダーのネイティブJSON形式を直接理解するため、変換ステップは不要です。インポーターは記録された各ステップを読み取り、対応するSyntheticテストのステップを作成し、セレクター、ビューポート、およびアサートされたナビゲーションイベントを保持します。

{{% button %}}**Import**{{% /button %}} ボタンを有効にするには、まずテストに名前を付ける必要があります。レコーディングと同じ命名規則を使用します。イニシャルの後にジャーニー名を続けます（例: **`<your initials>` - Online Boutique**）。イニシャルをプレフィックスとして付けることで、共有組織内でトレーナーやチームメイトがお互いの作業を簡単に見つけられるようになります。

![Import](../../img/import.png)

{{% button %}}**Import**{{% /button %}} ボタンが有効になったら、クリックして、Chrome DevTools RecorderからエクスポートしたJSONファイルをドロップするか、参照して選択します。

![Import JSON](../../img/import-json.png)

JSONが解析されると、インポートされたステップ数を示す緑色の確認メッセージが表示されます。予想よりも少ないステップ数が表示された場合、通常はSyntheticsインポーターが認識できない形式の記録されたアクションがあったことを意味します。その特定のインタラクションを再記録すると、通常は解決します。

{{% button style="blue" %}}Continue to edit steps{{% /button %}} をクリックします。

![Import Complete](../../img/import-complete.png)

**Edit steps** ビューには、インポートされた各ステップがアクションタイプ、ターゲットセレクター、および待機条件とともに順番に表示されます。ここからステップの並べ替え、追加、削除ができますが、これについては後のセクションで説明します。

![Edit Steps](../../img/edit-steps.png)

ステップ自体を編集する前に、まずテストのランタイム設定（実行場所、頻度、デバイス）を構成しましょう。 {{% button style="blue" %}}< Return to test{{% /button %}} をクリックします。
