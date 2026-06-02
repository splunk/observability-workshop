---
title: ITSIにおけるObservability Cloudディテクターの活用
linkTitle: 6. ITSIにおけるObservability Cloudディテクターの活用
weight: 1
---

## Part 2: Splunk Observability CloudからSplunk ITSIへのアラート送信

先ほど設定したディテクターがSplunk Observability Cloudに構成されているため、次のステップでは、アラートがトリガーされた際にそのアラートがSplunk IT Service Intelligence（ITSI）に送信されるようにします。この連携により、ITSIはこれらのアラートをnotable eventとして取り込み、他のイベントと相関付けてサービスヘルススコアに反映できるようになります。これを実現する最も一般的な方法は、Splunk Observability CloudのWebhookを使用して、Splunk ITSIに設定されたHTTP Event Collector（HEC）エンドポイントへアラートデータを送信することです。

**Step 1: Splunk（ITSI）でHTTP Event Collector（HEC）を設定する**

Splunk Observability CloudからITSIにアラートを送信する前に、ITSIが稼働しているSplunkインスタンス上に、それらを受信するためのHECエンドポイントが必要です。

1. ITSIをホストしているSplunk EnterpriseまたはSplunk Cloudインスタンスにログインします。
2. **Settings > Data Inputs** に移動します。
3. **HTTP Event Collector** をクリックします。
4. **Global Settings** をクリックします。HECが有効になっていることを確認します。有効になっていない場合は有効にし、デフォルトのポート（例: 8088、ただしSplunk Cloudでは管理方法が異なる場合があります）を指定します。
5. **New Token** をクリックします。
6. HECトークンに分かりやすい名前を付けます。例えば `o11y_alerts_for_itsi` などです。
7. **Source name override** には、必要に応じてsourcetypeを指定するか、空欄のままにしてObservability Cloud側で指定するか、デフォルトに任せます。
8. **Default Index** には、ITSIがこれらのイベントにアクセスできる適切なインデックスを選択します。多くの場合、ITSIイベント用に専用のインデックスがあるか、`main` や `itsi_event_management` などの汎用イベントインデックスを使用することもあります。
9. トークンが有効になっていることを確認し、**Submit** をクリックします。
10. 生成された **Token Value** をコピーします。これはSplunk Observability CloudでのWebhook設定に必要となります。

**Step 2: Splunk Observability CloudでWebhook連携を設定する**

次にSplunk Observability Cloudに戻り、先ほど作成したHECトークンを使用するWebhookをセットアップします。

1. Splunk Observability Cloudで **Data Management > Available Integrations** に移動します。
2. 新しい **Splunk platform** を追加するオプションを探します。
3. Integrationに名前を付けます。例えば `Splunk ITSI HEC` などです。
4. **URL** フィールドに、SplunkインスタンスのHECエンドポイントURIを入力します。通常は `https://<your-splunk-hec-host-or-ip>:<hec-port>/services/collector/event` という形式になります。
5. 先ほど作成した **HEC token** を追加する必要があります。
6. **Payload** については、ITSIが理解できるJSONペイロードを構築する必要があります。Splunk Observability Cloudには、ITSIイベント相関に必要なフィールドを含む標準のペイロードが用意されています。
7. Integrationを確認し、**Save** をクリックします。

**Step 3: ディテクターを更新してWebhookを使用する**

次に、Part 1で作成したディテクターに戻り、新しく設定したWebhookを使用するように通知設定を更新します。

1. Splunk Observability Cloudで **Detectors & SLOs** に移動します。
2. EC2のCPU使用率用に作成したディテクターを見つけて編集します。
3. 先ほど作成したAlert ruleをクリックします。
4. **Alert Recipients** セクションに移動します。
5. **Add recipient > Splunk platform** をクリックし、対象のアラート重要度（例: Critical、Warning）に対して、先ほど設定したIntegration（`Splunk ITSI HEC`）を選択します。
6. ディテクターへの変更を保存します。

**Step 4: 検証**

連携をテストするには、実際のアラートがトリガーされるのを待つか、ディテクターの設定で許可されていれば、手動でテストアラートをトリガーするか、アラートを強制的に発生させるためにしきい値を一時的に下げることもできます。Splunk Observability Cloudでアラートがトリガーされると、Webhook経由でペイロードがSplunk HECエンドポイントに送信されるはずです。

Splunkで対象のインデックス（例: `index=itsi_event_management sourcetype=o11y:itsi:alert host=<your-ec2-instance-id>`）を検索して確認します。Splunk Observability Cloudから到着したイベントデータが表示されるはずです。

これらの手順により、Splunk Observability CloudのディテクターからのアラートがSplunk ITSIに送信されるようになりました。イベントの相関付けやNotableの生成は、本ワークショップの前半で説明した内容とまったく同じように機能します。
