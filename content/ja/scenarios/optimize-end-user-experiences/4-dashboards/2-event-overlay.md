---
title: チャートデータと連動したイベント表示
linkTitle: 2. Event overlay
weight: 2
hidden: false
---
KPI の可視化は素晴らしいことです。さらに良いのは何でしょうか？イベントと連動した KPI です！[ダッシュボードにイベントをオーバーレイする](https://docs.splunk.com/observability/en/data-visualization/dashboards/dashboards-add.html#overlay-event-markers-on-charts-in-a-dashboard)ことで、デプロイメントなどのイベントがメトリクスの変化を引き起こしたかどうかを、良い方向にも悪い方向にも、より迅速に把握できます。

1. インストラクターがワークショップアプリケーションにコンディション変更をプッシュします。ダッシュボードチャートのイベントマーカーをクリックして、詳細を確認します。
![condition change event](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-04-02/d2dac271-0a85-46b9-b46d-e13e4e759f60/user_cropped_screenshot.jpeg?tl_px=0,0&br_px=1385,827&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=921,460)

1. ディメンションでは、この特定のイベントに関する詳細を確認できます。イベントレコードをクリックすると、必要に応じて削除のマークを付けることができます。
![event record](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-04-02/55a9d0dc-5a44-496d-b44f-60f681b5576b/ascreenshot.jpeg?tl_px=692,626&br_px=2412,1587&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=524,277)
![event details](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-04-02/ee20c9d9-9ea4-4302-af4a-73c8c24df029/user_cropped_screenshot.jpeg?tl_px=13,12&br_px=1733,974&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=832,324)

1. 画面右上のアイコンをクリックし、Event feed を選択することで、イベントフィードでイベントの履歴を確認することもできます。
![event feed](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-04-02/7e7317f6-04b4-404e-8e17-78cf3e319ef9/user_cropped_screenshot.jpeg?tl_px=0,0&br_px=1471,785&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=1056,84)

1. このフィードでは、最近のイベントに関する詳細を確認できます。
![event details](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-04-02/66c575d0-da25-4e4d-bd3b-78b6ce777ef4/user_cropped_screenshot.jpeg?tl_px=41,0&br_px=1760,877&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=815,346)

1. GUI または [API 経由](https://dev.splunk.com/observability/reference/api/ingest_data/latest#endpoint-send-events)で新しいイベントを追加することもできます。GUI で新しいイベントを追加するには、New event ボタンをクリックします。
![GUI add event button](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-04-02/f6707f30-af0e-4aa0-aa60-8272a601c0f7/user_cropped_screenshot.jpeg?tl_px=50,0&br_px=1770,852&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=895,179)

1. チーム名、イニシャル、イベントの種類（デプロイメント、キャンペーン開始など）でイベントに名前を付けます。タイムスタンプを選択するか、現在の時刻を使用する場合はそのままにして、「Create」をクリックします。
![create event form](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-04-02/1280542f-4446-4b9d-8a46-d524e0319572/user_cropped_screenshot.jpeg?tl_px=0,125&br_px=1567,1087&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=858,513)

1. 次に、新しいイベントがこのダッシュボードにオーバーレイされていることを確認する必要があります。1分ほど待ってから（必要に応じてページを更新してください）、Event overlay フィールドでイベントを検索します。
![overlay event](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-04-02/ca2b0b08-a369-473d-ad32-3926bfca934c/user_cropped_screenshot.jpeg?tl_px=0,0&br_px=1601,810&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=408,229)

1. イベントがダッシュボードの時間ウィンドウ内にある場合、チャートにオーバーレイされて表示されるはずです。「Save」をクリックして、イベントオーバーレイがダッシュボードに保存されることを確認してください。
![save dashboard](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-04-02/21dc9ffa-4b33-46b1-81e2-6204924b7ec5/user_cropped_screenshot.jpeg?tl_px=0,0&br_px=1432,732&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=868,67)

{{% notice title="覚えておきましょう" style="primary"  icon="lightbulb" %}}
バグチケットにコンテキストを追加したい場合や、変更によってアプリのパフォーマンスが向上したことをマネージャーに示したい場合はどうすればよいでしょうか？オブザーバビリティデータをイベントと連動して確認することは、トラブルシューティングに役立つだけでなく、他のチームとのコミュニケーションにも役立ちます。
{{% /notice %}}
