---
title: チャートディテクター
linkTitle: 3. Chart Detectors
weight: 3
hidden: false
---

カスタムダッシュボードチャートを使用して、関心のあるデータや条件に直接フォーカスしたディテクターを作成できます。チャートを構築する過程で、アラートをトリガーできるシグナルも構築しました。

## 静的ディテクター

多くの KPI では、しきい値として静的な値を念頭に置いています。

1. カスタム End User Experience ダッシュボードで、「LCP - all tests」チャートに移動します。

1. チャートの右上にあるベルアイコンをクリックし、「New detector from chart」を選択します。
![new detector from chart](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-17/2e7a0adf-f4f7-4183-b7e9-08bbe7350232/ascreenshot.jpeg?tl_px=1160,297&br_px=2880,1258&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=886,277)

1. ディテクター名に**チーム名**と**イニシャル**を含めるように変更し、アラートの詳細を調整します。しきい値を 2500 または 4000 に変更して、アラートノイズのプレビューがどのように変化するか確認します。
![alert details](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-17/4a6f44da-2559-49bf-8c5a-a58220c6e64d/ascreenshot.jpeg?tl_px=0,152&br_px=1719,1113&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=444,277)

1. 重大度を変更し、このディテクターを保存する前に自分自身を受信者として追加します。{{% button style="blue" %}}Activate{{% /button %}} をクリックします。
![activate the detector](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-17/1c2a7f23-c076-45e8-80b0-3a99e3989048/user_cropped_screenshot.jpeg?tl_px=0,652&br_px=1719,1614&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=216,453)

## 上級: 動的ディテクター

メトリクスが自然に変動する場合があるため、その時点で決定した静的なしきい値に制限されない、より動的なディテクターを作成したいことがあります。

1. チャートに動的ディテクターを作成するには、「old」ディテクターウィザードへのリンクをクリックします。
![click the link to open this detector in the old editor](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-17/877e9402-3634-4b44-8585-fe27331674c6/user_cropped_screenshot.jpeg?tl_px=901,0&br_px=2621,961&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=524,109)

1. ディテクター名に**チーム名**と**イニシャル**を含めるように変更し、{{% button style="blue" %}}Create alert rule{{% /button %}} をクリックします。
![name and create alert rule](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-17/fa9714b1-1fa0-47c4-9361-5753c0c5d4b4/ascreenshot.jpeg?tl_px=978,191&br_px=2698,1152&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=524,277)

1. シグナルが正しいことを確認し、Alert condition に進みます。
![alert signal details](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-17/d8dc6a69-f559-4399-b71d-583555266e35/ascreenshot.jpeg?tl_px=0,630&br_px=1719,1591&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=246,277)

1. 「Sudden Change」条件を選択し、Alert settings に進みます。
![list of dynamic conditions](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-17/3a4e5b88-befc-4af8-8736-5f4a5529d0aa/ascreenshot.jpeg?tl_px=0,838&br_px=1719,1799&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=486,340)

1. 設定を変更して、推定アラートノイズが上のチャートでどのようにプレビューされるか確認します。設定を調整し、必要に応じて詳細設定を変更してから、Alert message に進みます。
![alert noise marked on chart based on settings](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-17/8a01627f-2287-494e-a2a3-20ff1592b641/ascreenshot.jpeg?tl_px=381,782&br_px=2101,1743&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=524,277)

1. 重大度、Runbook URL、ヒント、メッセージペイロードをカスタマイズしてから、受信者の追加に進みます。
![alert message options](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-17/0af4f210-2202-4daf-9754-c8719867b388/ascreenshot.jpeg?tl_px=94,838&br_px=1813,1799&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=524,485)

1. このワークショップでは、受信者として自分のメールアドレスのみを追加してください。実際の環境では、Webhook、チケットシステム、Slack チャンネルなどの他のオプションを追加する場所です。
![recipient options](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-17/006bf87f-d5cb-4b17-9658-4f381aff9c9e/ascreenshot.jpeg?tl_px=87,838&br_px=1807,1799&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=524,457)

1. 最後に、{{% button style="blue" %}}Activate Alert Rule{{% /button %}} をクリックする前にディテクター名を確認します。
![activate alert rule button](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-17/146b3a5c-3c08-4fe8-a3fb-af44176963ca/ascreenshot.jpeg?tl_px=1160,838&br_px=2880,1799&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=890,468)
