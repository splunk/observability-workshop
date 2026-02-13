---
title: ITSI での Observability Cloud Detectors の使用
linkTitle: 6. ITSI での Observability Cloud Detectors の使用
weight: 1
---

## パート 2: Splunk Observability Cloud から Splunk ITSI へのアラート送信

先ほど設定したSplunk Observability CloudのDetectorがあるため、次のステップは、アラートがトリガーされたときに、そのアラートがSplunk IT Service Intelligence (ITSI) に送信されるようにすることです。この統合により、ITSIはこれらのアラートをNotable Eventとして取り込み、他のイベントと相関させてサービスヘルススコアに貢献させることができます。これを実現する最も一般的な方法は、Splunk Observability CloudのWebhookを使用して、Splunk ITSIで設定されたHTTP Event Collector (HEC) エンドポイントにアラートデータを送信することです。

**ステップ 1: Splunk (ITSI) で HTTP Event Collector (HEC) を設定**

Splunk Observability CloudがITSIにアラートを送信する前に、それらを受信するためにSplunkインスタンス（ITSIが実行されている場所）にHECエンドポイントが必要です。

1. ITSIをホストしているSplunk EnterpriseまたはSplunk Cloudインスタンスにログインします。
2. **Settings > Data Inputs** に移動します。
3. **HTTP Event Collector** をクリックします。
4. **Global Settings** をクリックします。HECが有効になっていることを確認します。有効になっていない場合は、有効にしてデフォルトポート（例: 8088、ただしSplunk Cloudでは異なる管理方法の場合があります）を指定します。
5. **New Token** をクリックします。
6. HECトークンにわかりやすい名前を付けます。例: `o11y_alerts_for_itsi`。
7. **Source name override** については、オプションでsourcetypeを指定するか、空白のままにしてObservability Cloudで指定するか、デフォルトを使用できます。
8. **Default Index** については、ITSIがこれらのイベントにアクセスできる適切なインデックスを選択します。多くの場合、ITSIイベント専用のインデックスがあるか、`main` や `itsi_event_management` などの一般的なイベントインデックスを使用することがあります。
9. トークンが有効になっていることを確認し、**Submit** をクリックします。
10. 生成された **Token Value** をコピーします。これはSplunk Observability CloudでのWebhook設定に必要です。

**ステップ 2: Splunk Observability Cloud で Webhook 統合を設定**

次に、Splunk Observability Cloudに戻り、作成したHECトークンを使用するWebhookを設定します。

1. Splunk Observability Cloudで **Data Management > Available Integrations** に移動します。
2. 新しい **Splunk platform** を追加するオプションを探します。
3. 統合に名前を付けます。例: `Splunk ITSI HEC`。
4. **URL** フィールドに、SplunkインスタンスのHECエンドポイントURIを入力します。通常、`https://<your-splunk-hec-host-or-ip>:<hec-port>/services/collector/event` の形式になります。
5. 先ほど作成した **HEC token** を追加する必要があります。
6. **Payload** については、ITSIが理解できるJSONペイロードを構築する必要があります。Splunk Observability Cloudは、ITSIイベント相関に必要なフィールドを含むように設定された、すぐに使えるペイロードを提供しています。
7. 統合を確認し、**Save** をクリックします

**ステップ 3: Webhook を使用するように Detector を更新**

次に、パート1で作成したDetectorに戻り、新しく設定したWebhookを使用するように通知設定を更新します。

1. Splunk Observability Cloudで **Detectors & SLOs** に移動します。
2. EC2 CPU使用率用に作成したDetectorを見つけて編集します。
3. 先ほど作成したAlert ruleをクリックします
4. **Alert Recipients** セクションに移動します。
5. **Add recipient > Splunk platform** をクリックし、設定した統合（`Splunk ITSI HEC`）を目的のアラート重大度（例: Critical、Warning）に対して選択します。
6. Detectorへの変更を保存します。

**ステップ 4: 検証**

統合をテストするには、本物のアラートがトリガーされるのを待つか、Detectorの設定で許可されている場合は、テストアラートを手動でトリガーするか、しきい値を一時的に下げてアラートを強制的に発生させることができます。Splunk Observability Cloudでアラートがトリガーされると、Webhookを介してSplunk HECエンドポイントにペイロードが送信されるはずです。

Splunkでターゲットインデックスを検索して確認します（例: `index=itsi_event_management sourcetype=o11y:itsi:alert host=<your-ec2-instance-id>`）。Splunk Observability Cloudからのイベントデータが到着していることが確認できるはずです。

これらの手順により、Splunk Observability CloudのDetectorからのアラートがSplunk ITSIに送信されるようになりました。イベントの相関とNotableの生成は、このワークショップで先ほど説明したのとまったく同じように機能します。
