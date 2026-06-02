---
title: Create Tests
linkTitle: 4.3 Create Tests
weight: 1
time: 10 minutes
description: Create Tests
---

## 概要

それでは、この統合をデモンストレーションするためのテストを作成します。

3つのテストを作成します。

* ThousandEyes エージェントからのテスト (クラスター内)。アプリケーションがパブリックインターネットからアクセスできない場合に有用です
* より興味深いトレース (クラスター内)
* パブリック URL と ThousandEyes Cloud Agent を使用した、パブリックインターネットからのテスト

### Step 1: HTTP Test (Kubernetesクラスター内)

1. ThousandEyes で **Network & App Synthetics > Test Settings** に移動します。
2. **Add New Test** をクリックし、**HTTP Server** を選択します。
3. テストを設定します。

    * **URL**: `http://api-gateway.default.svc.cluster.local:82/`
    * **Test Name**: `[Name] Frontend Available (In Cluster)`
    * **How often test runs**: 10 minutes
    * **Agents**: `Enterprise Agents` タブを選択し、本ガイドの前段でデプロイしたエージェントを選択します
    * **Enable distributed tracing**: 有効化します
    * **Verify Content**: 任意です。返されたページコンテンツを検証する場合は `PetClinic` を使用します。

    ![ThousandEyes Script Settings](../../images/test-distributed-tracing.png?width=20vw)

4. **Instant Test** をクリックします

    {{% notice title="Instant Test" style="info" %}}
    これは新しいタブを開き、テストは保存されない点に注意してください。
    {{% /notice %}}

5. **Service Map** タブに切り替えます

ThousandEyes でサービスマップビューが表示されるまで少し時間がかかる場合がありますが、Splunk Observability Cloud でトレースを見つけられるはずです。

1. トレースをコピーします
2. Splunk Observability Cloud で **APM > Trace Analyzer** に移動し、トレースを貼り付けて **Go** をクリックします

最終的に、以下のような画面が表示されるはずです。

![Test 1 - ThousandEyes](../../images/test1-te.png?width=35vw)

![Test 1 - APM](../../images/test1-apm.png?width=35vw)

### Step 2: HTTP Test (Kubernetesクラスター内) - より興味深いトレース

それでは、Step 1 を繰り返しますが、URL には `http://api-gateway.default.svc.cluster.local:82/api/customer/owners` (Owners List) を使用します。

作成済みの同じテストを編集して、インスタントテストを実行できます。

より興味深いマップが得られるはずです。
![Test 2 - ThousandEyes](../../images/test2-te.png?width=35vw)

![Test 2 - APM](../../images/test2-apm.png?width=35vw)

{{% notice title="ThousandEyes Failure" style="note" %}}
ThousandEyes 上のテストが失敗していることにお気づきでしょうか。これは Owners List に応じて **Verify Content** を変更しなかったためです。
![Test 2 - ThousandEyes Verify Content Failure](../../images/test2-te-fail.png?width=20vw)
{{% /notice %}}
