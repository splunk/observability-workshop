---
title: 1. アプリケーションのビルド
weight: 1
---

このワークショップには、いくつかのRESTエンドポイントを持つシンプルなSpring Bootアプリケーションが含まれています。ビルドしましょう。

## JavaとMavenの確認

インスタンスにはOpenJDK 17とMavenがプリインストールされています。確認します。

{{< tabs >}}
{{% tab title="コマンド" %}}

```bash
java -version && mvn -version
```

{{% /tab %}}
{{% tab title="出力例" %}}

```text
openjdk version "17.0.x" ...
Apache Maven 3.x.x ...
```

{{% /tab %}}
{{< /tabs >}}

## アプリケーションのビルド

ワークショップのアプリケーションディレクトリに移動し、fat JARをビルドします。

{{< tabs >}}
{{% tab title="コマンド" %}}

```bash
cd ~/workshop/appd/app
mvn package -DskipTests
```

{{% /tab %}}
{{% tab title="出力例" %}}

```text
[INFO] BUILD SUCCESS
```

{{% /tab %}}
{{< /tabs >}}

{{% notice title="初回ビルド" style="info" icon="info-circle" %}}
初回の `mvn package` ではSpring Bootの依存関係をダウンロードします。30〜60秒かかります。2回目以降のビルドはより高速です。
{{% /notice %}}

## アプリケーションのテスト（AppDなし）

アプリケーションが起動することを確認するため、簡単に実行します。

```bash
java -jar target/ingest-workshop-1.0.0.jar &
```

数秒待ってからEnterキーを押してプロンプトに戻り、テストします。

{{< tabs >}}
{{% tab title="コマンド" %}}

```bash
curl -s localhost:8080/health | jq .
```

{{% /tab %}}
{{% tab title="出力例" %}}

```json
{
  "status": "healthy"
}
```

{{% /tab %}}
{{< /tabs >}}

次に進む前にアプリケーションを停止します。

```bash
kill %1
```

アプリケーションは正常に動作しています。次に、AppDynamics Java Agentをダウンロードしてこのプロセスにアタッチします。
