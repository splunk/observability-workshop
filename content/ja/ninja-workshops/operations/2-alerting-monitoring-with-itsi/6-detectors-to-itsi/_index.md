---
title: Observability CloudのDetectorをITSIで使用する
linkTitle: 6. Observability CloudのDetectorをITSIで使用する
weight: 1
---

## パート2: Splunk Observability CloudからSplunk ITSIへアラートを送信する

先ほどSplunk Observability Cloudで設定したDetectorがあるため、次のステップはアラートがトリガーされた際にSplunk IT Service Intelligence（ITSI）へ送信されるようにすることです。この連携により、ITSIはこれらのアラートをNotableイベントとして取り込み、他のイベントと相関させてサービスのヘルススコアに反映できます。最も一般的な方法は、Splunk Observability CloudのWebhookを使用して、Splunk ITSIに設定されたHTTP Event Collector（HEC）エンドポイントにアラートデータを送信することです。

**ステップ1: Splunk（ITSI）でHTTP Event Collector（HEC）を設定する**

Splunk Observability CloudからITSIにアラートを送信する前に、Splunkインスタンス（ITSIが稼働している環境）にアラートを受信するためのHECエンドポイントが必要です。

1. ITSIをホストしているSplunk EnterpriseまたはSplunk Cloudインスタンスにログインします。
2. **Settings > Data Inputs** に移動します。
3. **HTTP Event Collector** をクリックします。
4. **Global Settings** をクリックします。HECが有効になっていることを確認します。有効になっていない場合は、有効にしてデフォルトポートを指定します（例: 8088、ただしSplunk Cloudでは管理方法が異なる場合があります）。
5. **New Token** をクリックします。
6. HECトークンにわかりやすい名前を付けます。例: `o11y_alerts_for_itsi`
7. **Source name override** では、オプションでsourcetypeを指定するか、空白のままにしてObservability Cloudで指定するかデフォルトを使用します。
8. **Default Index** では、ITSIがこれらのイベントにアクセスできる適切なインデックスを選択します。通常、ITSIイベント用の専用インデックスがあるか、`main`や`itsi_event_management`などの汎用イベントインデックスを使用します。
9. トークンが有効になっていることを確認し、**Submit** をクリックします。
10. 生成された **Token Value** をコピーします。これはSplunk Observability CloudでのWebhook設定に必要です。

**ステップ2: Splunk Observability CloudでWebhookインテグレーションを設定する**

次に、Splunk Observability Cloudに戻り、先ほど作成したHECトークンを使用するWebhookを設定します。

1. Splunk Observability Cloudで **Data Management > Available Integrations** に移動します。
2. **Splunk platform** を追加するオプションを探します。
3. インテグレーションに名前を付けます。例: `Splunk ITSI HEC`
4. **URL** フィールドに、SplunkインスタンスのHECエンドポイントURIを入力します。通常、`https://<your-splunk-hec-host-or-ip>:<hec-port>/services/collector/event`の形式になります。
5. 先ほど作成した **HEC token** を追加します。
6. **Payload** では、ITSIが理解できるJSONペイロードを構成する必要があります。Splunk Observability Cloudは、ITSIのイベント相関に必要なフィールドを含むペイロードをすぐに使える形で提供しています。
7. インテグレーションを確認し、**Save** をクリックします。

**ステップ3: DetectorをWebhookを使用するように更新する**

次に、パート1で作成したDetectorに戻り、新しく設定したWebhookを使用するように通知設定を更新します。

1. Splunk Observability Cloudで **Detectors & SLOs** に移動します。
2. EC2 CPU使用率用に作成したDetectorを見つけて編集します。
3. 先ほど作成したAlert ruleをクリックします。
4. **Alert Recipients** セクションに移動します。
5. **Add recipient > Splunk platform** をクリックし、目的のアラート重大度（例: Critical、Warning）に対して先ほど設定したインテグレーション（`Splunk ITSI HEC`）を選択します。
6. Detectorの変更を保存します。

**ステップ4: 検証する**

インテグレーションをテストするには、実際のアラートがトリガーされるのを待つか、Detectorの設定で許可されている場合はテストアラートを手動でトリガーするか、一時的にしきい値を下げてアラートを強制的に発生させます。Splunk Observability Cloudでアラートがトリガーされると、Webhook経由でペイロードがSplunk HECエンドポイントに送信されます。

Splunkでターゲットインデックスを検索して確認します（例: `index=itsi_event_management sourcetype=o11y:itsi:alert host=<your-ec2-instance-id>`）。Splunk Observability Cloudからイベントデータが到着していることが表示されます。

これらのステップにより、Splunk Observability CloudのDetectorからのアラートがSplunk ITSIに送信されるようになりました。イベントの相関とNotableの生成は、このワークショップで先ほど説明したものとまったく同じように機能します。
