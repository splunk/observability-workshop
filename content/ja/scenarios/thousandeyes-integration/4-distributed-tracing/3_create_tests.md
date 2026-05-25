---
title: テストの作成
linkTitle: 4.3 テストの作成
weight: 1
time: 10 minutes
description: テストの作成
---

## 概要

ここでは、この統合を実演するためのテストを作成します。

3つのテストを作成します

* ThousandEyes エージェントからのテスト（クラスター内部）。アプリケーションがパブリックインターネットからアクセスできない場合に便利です
* より詳細なトレース（クラスター内部）
* パブリックインターネットからのテスト。パブリック URL と ThousandEyes Cloud Agent を使用します

### ステップ 1: HTTP テスト（Kubernetes クラスター内）

1. ThousandEyes で、**Network & App Synthetics > Test Settings** に移動します。
2. **Add New Test** をクリックし、**HTTP Server** を選択します。
3. テストを設定します
* **URL**: `http://api-gateway.default.svc.cluster.local:82/`
* **Test Name**: `[Name] Frontend Available (In Cluster)`
* **How often test runs**: 10 minutes
* **Agents**: `Enterprise Agents` タブを選択し、このガイドの前のステップでデプロイしたエージェントを選択します
* **Enable distributed tracing**: 有効にします
* **Verify Content**: オプションです。返されるページコンテンツを検証する場合は `PetClinic` を使用します。
![ThousandEyes Script Settings](../../images/test-distributed-tracing.png?width=20vw)

4. **Instant Test** をクリックします
{{% notice title="Instant Test" style="info" %}}
これにより新しいタブが開き、テストは保存されません。この点にご注意ください。
{{% /notice %}}
6. **Service Map** タブに切り替えます

ThousandEyes でサービスマップビューが表示されるまで少し時間がかかる場合がありますが、Splunk Observability Cloud でトレースを見つけることができるはずです。

7. トレースをコピーします
8. Splunk Observability Cloud で、**APM > Trace Analyzer** に移動し、トレースを貼り付けて **Go** をクリックします

最終的に、以下のような画面が表示されるはずです

![Test 1 - ThousandEyes](../../images/test1-te.png?width=35vw)

![Test 1 - APM](../../images/test1-apm.png?width=35vw)

### ステップ 2: HTTP テスト（Kubernetes クラスター内）- より詳細なトレース

ステップ 1 を繰り返しますが、URL には `http://api-gateway.default.svc.cluster.local:82/api/customer/owners`（Owners List）を使用します。

先ほど作成したテストを編集し、Instant Test を実行できます。

より詳細なマップが得られるはずです。
![Test 2 - ThousandEyes](../../images/test2-te.png?width=35vw)

![Test 2 - APM](../../images/test2-apm.png?width=35vw)

{{% notice title="ThousandEyes Failure" style="note" %}}
ThousandEyes でテストが失敗していることに気づきましたか？これは、Owners List に基づいて **Verify Content** を変更しなかったためです。
![Test 2 - ThousandEyes Verify Content Failure](../../images/test2-te-fail.png?width=20vw)
{{% /notice %}}
