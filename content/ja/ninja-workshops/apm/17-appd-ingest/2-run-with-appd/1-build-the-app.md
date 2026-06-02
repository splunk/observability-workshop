---
title: 1. アプリケーションのビルド
weight: 1
---

このワークショップには、いくつかの REST エンドポイントを持つシンプルな Spring Boot アプリケーションが含まれています。まずはこれをビルドしましょう。

## Java と Maven の確認

インスタンスには OpenJDK 17 と Maven がプリインストールされています。以下のコマンドで確認します。

{{< tabs >}}
{{% tab title="Command" %}}

```bash
java -version && mvn -version
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
openjdk version "17.0.x" ...
Apache Maven 3.x.x ...
```

{{% /tab %}}
{{< /tabs >}}

## アプリケーションのビルド

ワークショップアプリのディレクトリに移動し、fat JAR をビルドします。

{{< tabs >}}
{{% tab title="Command" %}}

```bash
cd ~/workshop/appd/app
mvn package -DskipTests
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
[INFO] BUILD SUCCESS
```

{{% /tab %}}
{{< /tabs >}}

{{% notice title="初回ビルド" style="info" icon="info-circle" %}}
最初の `mvn package` 実行時には Spring Boot の依存関係をダウンロードします。この処理には 30〜60 秒ほどかかります。2 回目以降のビルドは大幅に高速になります。
{{% /notice %}}

## アプリケーションのテスト（AppD なし）

アプリが起動することを確認するため、短時間実行します。

```bash
java -jar target/ingest-workshop-1.0.0.jar &
```

数秒待ってから return キーを押してプロンプトに戻り、以下のコマンドでテストします。

{{< tabs >}}
{{% tab title="Command" %}}

```bash
curl -s localhost:8080/health | jq .
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```json
{
  "status": "healthy"
}
```

{{% /tab %}}
{{< /tabs >}}

次に進む前に、アプリを停止します。

```bash
kill %1
```

アプリケーションが正常に動作することを確認できました。次に、このプロセスにアタッチするための AppDynamics Java Agent をダウンロードします。
