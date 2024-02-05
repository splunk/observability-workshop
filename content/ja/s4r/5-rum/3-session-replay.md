---
title: 3. Session Replay
weight: 3
---

{{% notice title="Sessions" style="info" %}}

セッションは、あるユーザーがアプリケーションを操作するときに実行するアクションに対応するトレースの集合です。 デフォルトでは、セッションは、セッション内でキャプチャされた最後のイベントから 15 分が経過するまで継続します。 セッションの最大継続時間は 4 時間です。

{{% /notice %}}

{{% notice title="Exercise" style="green" icon="running" %}}

* **User Sessions** テーブルで、最長の **Duration**（20秒以上）を持つトップの **Session ID** をクリックします。これにより、RUM セッションビューに移動します。

{{% /notice %}}

![RUM Session](../images/rum-session.png)

{{% notice title="Exercise" style="green" icon="running" %}}

* RUM セッションリプレイ {{% button icon="play" %}}Replay{{% /button %}} ボタンをクリックします。RUM セッションリプレイを使用すると、ユーザーセッションを再生して表示できます。これはユーザーが実際にどのような体験をしたかを正確に確認するための素晴らしい方法です。
* リプレイを開始するためにボタンをクリックします。

{{% /notice %}}

![RUM Session](../images/rum-session-replay.png)

RUM セッションリプレイでは、デフォルトでテキストがマスキングされますが、画像もマスキングできます（このワークショップの例ではマスキングされています）。これは、セッションに機密情報が含まれている場合に役立ちます。再生速度を変更したり、リプレイを一時停止したりすることもできます。

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}

セッションを再生する際に、マウスの動きがどのようにキャプチャされるかに注目してください。これは、ユーザーがどこに注意を集中しているかを確認するのに役立ちます。

{{% /notice %}}
