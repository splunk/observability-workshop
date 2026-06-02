---
title: 3. Session Replay
weight: 3
---

{{% notice title="セッションについて" style="info" %}}

セッションとは、1人のユーザーがアプリケーションと対話する際に行った一連のアクションに対応するトレースの集合です。デフォルトでは、セッションでキャプチャされた最後のイベントから15分が経過するとセッションは終了します。セッションの最大継続時間は4時間です。

{{% /notice %}}

{{% exercise title="最長のセッションを開く" %}}

* **User Sessions** テーブルで、**Duration** が最も長い（20秒以上の）**Session ID** をクリックします。RUM Session ビューが表示されます。

{{% /exercise %}}

![RUM Session](../images/rum-session.png)

{{% exercise title="Session Replay を視聴する" %}}

* RUM Session Replay の {{% button icon="play" %}}Replay{{% /button %}} ボタンをクリックします。RUM Session Replay を使うと、ユーザーセッションを再生して確認できます。これは、ユーザーが実際に体験した内容をそのまま把握するのに非常に有効な方法です。
* ボタンをクリックして再生を開始します。

{{% /exercise %}}

RUM Session Replay では情報をマスクできます。デフォルトではテキストがマスクされます。画像をマスクすることも可能です（本ワークショップの例ではマスク済みです）。これは、機密情報を含むセッションを再生する際に役立ちます。再生速度の変更や、再生の一時停止も可能です。

{{% notice title="ヒント" style="primary"  icon="lightbulb" %}}

セッションを再生する際、マウスの動きがどのようにキャプチャされているかに注目してください。ユーザーがどこに注目しているかを把握するのに役立ちます。

{{% /notice %}}
