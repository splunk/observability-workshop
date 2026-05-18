---
title: テストの作成
linkTitle: 4.3 テストの作成
weight: 1
time: 10 minutes
description: テストの作成
---

## 概要

ここでは、このインテグレーションを実証するためのテストを作成します。

3つのテストを作成します

* ThousandEyes エージェント（クラスター内部）からのテスト。アプリケーションがパブリックインターネットからアクセスできない場合に有用です
* より興味深いトレース（クラスター内部）
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
* **Verify Content**: オプションです。返されるページコンテンツを検証したい場合は `PetClinic` を使用します。
![ThousandEyes Script Settings](../../images/test-distributed-tracing.png?width=20vw)

4. **Instant Test** をクリックします
{{% notice title="Instant Test" style="info" %}}
これにより新しいタブが開き、テストは保存されませんのでご注意ください。
{{% /notice %}}
6. **Service Map** タブに切り替えます

ThousandEyes でサービスマップビューが表示されるまで少し時間がかかる場合がありますが、Splunk Observability Cloud でトレースを確認できるはずです。

7. トレースをコピーします
8. Splunk Observability Cloud で、**APM > Trace Analyzer** に移動し、トレースを貼り付けて **Go** をクリックします

最終的に、以下のような表示が確認できるはずです

![Test 1 - ThousandEyes](../../images/test1-te.png?width=35vw)

![Test 1 - APM](../../images/test1-apm.png?width=35vw)

### ステップ 2: HTTP テスト（Kubernetes クラスター内）- より興味深いトレース

ステップ 1 を繰り返しますが、URL には `http://api-gateway.default.svc.cluster.local:82/api/customer/owners`（Owners List）を使用します。

同じテストを編集して、Instant Test を実行できます。

より興味深いマップが得られるはずです。
![Test 2 - ThousandEyes](../../images/test2-te.png?width=35vw)

![Test 2 - APM](../../images/test2-apm.png?width=35vw)

{{% notice title="ThousandEyes の失敗" style="note" %}}
ThousandEyes でテストが失敗していることに気づきましたか？これは、Owners List に基づいて **Verify Content** を変更しなかったためです。
![Test 2 - ThousandEyes Verify Content Failure](../../images/test2-te-fail.png?width=20vw)
{{% /notice %}}

### ステップ 3: HTTP テスト（パブリック）

最後に、パブリックインターネットからこのページにアクセスできるか確認しましょう。

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
