---
title: ミューティングルールを利用する
linkTitle: ミューティングルールの作成
weight: 3
isCJKLanguage: true
---

* ミューティングルールを設定する
* 通知を再開する
  
---

## 1. ミューティングルールの設定

特定の通知をミュートする必要がある場合があります。例えば、サーバーやサーバー群のメンテナンスのためにダウンタイムを設定したい場合や、新しいコードや設定をテストしている場合などがあります。このような場合には、Splunk Observability Cloud でミューティングルールを使用できます。それでは作成してみましょう。

ナビバーにある ![alerts and detectors](../../../images/alerts-and-detectors.png) ボタンをクリックし、**Detectors** を選択します。現在設定されているディテクターの一覧が表示されます。フィルタを使ってディテクターを探すこともできます。

![detectors list](../../../images//detectors.png)

**Creating a Detector** でディテクターを作成した場合は、右端の3つの点 **`...`** をクリックすると、そのディテクターが表示されます。

ドロップダウンから **Create Muting Rule...** をクリックします。

![Create Muting Rule](../../../images/create-muting-rule.png)

**Muting Rule** ウィンドウで、 **Mute Indefinitely** をチェックし、理由を入力します。

{{% notice title="Important" style="info" %}}
この操作をすると、ここに戻ってきてこのボックスのチェックを外すか、このディテクターの通知を再開するまで、通知が永久的にミュートされます。
{{% /notice %}}

![Mute Indefinitely](../../../images//mute-indefinitely.png)

**Next** をクリックして、新しいモーダルウィンドウでミュートルールの設定を確認します。

![Confirm Rule](../../../images//confirm-rule.png)

{{% labelbutton color="ui-button-blue" %}}**Mute Indefinitely**{{% /labelbutton %}} をクリックして、設定を確定させます。

![List muted rule](../../../images/alert-muted.png)

これで、通知を再開するまで、ディテクターからのEメール通知は受け取ることがなくなりました。では、再開する方法を見てみましょう。

---

## 2. 通知を再開する

**Muting Rules** をクリックして、**Detector** の見出しの下に、通知をミュートしたディテクターの名前が表示されます。

右端にあるドット **`...`** を開いて、**Resume Notifications** をクリックします。

![Resume](../../../images//muting-list.png)

{{% labelbutton color="ui-button-blue" %}}**Resume**{{% /labelbutton %}} をクリックして、このディテクターの通知を確認し、再開します。

![Resume](../../../images//resume.png)

**おめでとうございます！** これでアラート通知が再開されました。
