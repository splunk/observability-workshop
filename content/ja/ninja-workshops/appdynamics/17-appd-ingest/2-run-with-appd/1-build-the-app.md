---
title: 1. アプリのビルド
weight: 1
---

このワークショップには、いくつかの REST エンドポイントを持つシンプルな Spring Boot アプリケーションが含まれています。それをビルドしましょう。

## Java と Maven の確認

インスタンスには OpenJDK 17 と Maven がプリインストールされています。確認します

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

ワークショップアプリのディレクトリに移動し、fat JAR をビルドします

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
初回の `mvn package` では Spring Boot の依存関係をダウンロードします。これには 30〜60 秒かかります。2 回目以降のビルドはより高速です。
{{% /notice %}}

## アプリケーションのテスト（AppD なし）

アプリを短時間実行して、起動することを確認します

```bash
java -jar target/ingest-workshop-1.0.0.jar &
```

数秒待ち、Return キーを押してプロンプトに戻り、テストします

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

次に進む前にアプリを停止します

```bash
kill %1
```

アプリケーションが動作することを確認できました。次に、AppDynamics Java Agent をダウンロードして、このプロセスにアタッチします。
