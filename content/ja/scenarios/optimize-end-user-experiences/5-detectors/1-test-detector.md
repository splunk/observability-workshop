---
title: テストディテクター
linkTitle: 1. テストディテクター
weight: 1
hidden: false
---

[単一の Synthetic テストにディテクター](https://docs.splunk.com/observability/en/synthetics/test-config/synth-alerts.html)を設定する理由は何でしょうか？いくつかの例を挙げます

- エンドポイント、APIトランザクション、またはブラウザジャーニーが非常に重要である
- コード変更をデプロイした後、結果の KPI が期待通りかどうかを確認したい
- テスト中の特定の変更を一時的に注視する必要があるが、大量のノイズを生成したくない。後でディテクターを無効にする予定である
- 実際のユーザーが遭遇する前に、予期しない問題を把握したい

1. テスト概要ページで、右上の {{% button %}}Create Detector{{% /button %}} をクリックします。
![単一の Synthetic テストにディテクターを作成](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-16/5ff84106-52ac-4519-8835-999446227709/user_cropped_screenshot.jpeg?tl_px=1144,0&br_px=2864,961&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=902,79)

1. ディテクターに**チーム名**、**イニシャル**、および **LCP**（最終的に使用するシグナル）を含む名前を付けます。これにより、インストラクターが全員の進捗状況をより簡単に把握できます。

1. シグナルを First byte time に変更します。
![シグナルの変更](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-16/e443d816-7608-4073-905f-45f36d189665/ascreenshot.jpeg?tl_px=440,240&br_px=2160,1201&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=524,276)

1. アラートの詳細を変更し、右側のチャートがその条件下でのアラートイベントの量をどのように表示するかを確認します。ここで、チームが許容できるアラートノイズの量に基づいて、どの程度のアラートノイズを生成するかを決定できます。設定を変更して、推定アラートノイズにどのように影響するかを確認してください。
![アラートノイズのプレビュー](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-16/35b475b5-4e66-498d-971a-06c5368bc0ce/ascreenshot.jpeg?tl_px=0,233&br_px=1719,1194&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=404,277)

1. 次に、**シグナルを Largest contentful paint に変更します**。これは、読み込み時間に関連するユーザーエクスペリエンスに関わる重要な Web Vital です。しきい値を **2500ms** に変更します。ディテクタープレビューにサンプルアラートイベントが表示されなくても問題ありません。

1. このウィンドウを下にスクロールして、重大度や受信者などの通知オプションを確認します。
![通知オプション](../_img/detector-notifications.png)

1. 通知リンクをクリックして、アラートの件名、メッセージ、ヒント、およびランブックリンクをカスタマイズします。
![通知カスタマイズダイアログ](../_img/notification-custom.png)

1. このディテクターが生成するアラートノイズの量に満足したら、Activate をクリックします。
![ディテクターの有効化](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-16/6a80893a-fffc-475b-a22c-98c89c239095/ascreenshot.jpeg?tl_px=0,838&br_px=1719,1799&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=168,451)
