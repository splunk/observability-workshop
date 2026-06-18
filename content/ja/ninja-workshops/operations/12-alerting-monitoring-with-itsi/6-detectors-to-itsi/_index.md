---
title: ITSI での Observability Cloud Detector の使用
linkTitle: 6. ITSI での Observability Cloud Detector の使用
weight: 1
---

## パート 2: Splunk Observability Cloud から Splunk ITSI へのアラート送信

先ほど設定した Splunk Observability Cloud の Detector があるので、次のステップはアラートがトリガーされた際に、そのアラートが Splunk IT Service Intelligence (ITSI) に送信されるようにすることです。この統合により、ITSI はこれらのアラートを Notable Event として取り込み、他のイベントと相関付けてサービスヘルススコアに反映させることができます。これを実現する最も一般的な方法は、Splunk Observability Cloud の Webhook を使用して、Splunk ITSI に設定された HTTP Event Collector (HEC) エンドポイントにアラートデータを送信することです。

**ステップ 1: Splunk (ITSI) で HTTP Event Collector (HEC) を設定する**

Splunk Observability Cloud が ITSI にアラートを送信できるようにするには、Splunk インスタンス（ITSI が稼働している環境）にアラートを受信するための HEC エンドポイントが必要です。

1. ITSI をホストしている Splunk Enterprise または Splunk Cloud インスタンスにログインします。
2. **Settings > Data Inputs** に移動します。
3. **HTTP Event Collector** をクリックします。
4. **Global Settings** をクリックします。HEC が有効になっていることを確認します。有効でない場合は、有効にしてデフォルトポート（例: 8088、ただし Splunk Cloud では異なる管理方法の場合があります）を指定します。
5. **New Token** をクリックします。
6. HEC トークンにわかりやすい名前を付けます。例: `o11y_alerts_for_itsi`
7. **Source name override** には、オプションで sourcetype を指定するか、空白のままにして Observability Cloud で指定するかデフォルトのままにします。
8. **Default Index** には、ITSI がこれらのイベントにアクセスできる適切なインデックスを選択します。多くの場合、ITSI イベント用の専用インデックスがあるか、`main` や `itsi_event_management` のような汎用イベントインデックスを使用します。
9. トークンが有効になっていることを確認し、**Submit** をクリックします。
10. 生成された **Token Value** をコピーします。これは Splunk Observability Cloud での Webhook 設定に必要です。

**ステップ 2: Splunk Observability Cloud で Webhook インテグレーションを設定する**

次に、Splunk Observability Cloud に戻り、先ほど作成した HEC トークンを使用する Webhook を設定します。

1. Splunk Observability Cloud で **Data Management > Available Integrations** に移動します。
2. **Splunk platform** を追加するオプションを探します。
3. インテグレーションに名前を付けます。例: `Splunk ITSI HEC`
4. **URL** フィールドに、Splunk インスタンスの HEC エンドポイント URI を入力します。通常、`https://<your-splunk-hec-host-or-ip>:<hec-port>/services/collector/event` の形式になります。
5. 先ほど作成した **HEC token** を追加する必要があります。
6. **Payload** には、ITSI が理解できる JSON ペイロードを構成する必要があります。Splunk Observability Cloud は、ITSI イベント相関に必要なフィールドを含むように設定された標準のペイロードを提供しています。
7. インテグレーションを確認し、**Save** をクリックします。

**ステップ 3: Detector を更新して Webhook を使用する**

次に、パート 1 で作成した Detector に戻り、新しく設定した Webhook を使用するように通知設定を更新します。

1. Splunk Observability Cloud で **Detectors & SLOs** に移動します。
2. EC2 CPU 使用率用に作成した Detector を見つけて編集します。
3. 先ほど作成した Alert rule をクリックします。
4. **Alert Recipients** セクションに移動します。
5. **Add recipient > Splunk platform** をクリックし、目的のアラート重大度（例: Critical、Warning）に対して先ほど設定したインテグレーション（`Splunk ITSI HEC`）を選択します。
6. Detector への変更を保存します。

**ステップ 4: 検証**

インテグレーションをテストするには、実際のアラートがトリガーされるのを待つか、Detector の設定が許可する場合はテストアラートを手動でトリガーするか、一時的にしきい値を下げてアラートを強制的に発生させることができます。Splunk Observability Cloud でアラートがトリガーされると、Webhook 経由で Splunk HEC エンドポイントにペイロードが送信されます。

Splunk でターゲットインデックスを検索して確認します（例: `index=itsi_event_management sourcetype=o11y:itsi:alert host=<your-ec2-instance-id>`）。Splunk Observability Cloud からイベントデータが到着していることを確認できるはずです。

これらのステップにより、Splunk Observability Cloud の Detector からのアラートが Splunk ITSI に送信されるようになりました。イベントの相関付けと Notable の生成は、このワークショップで先ほど説明したものとまったく同じように機能します。
