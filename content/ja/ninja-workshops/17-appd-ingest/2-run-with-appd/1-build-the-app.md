---
title: 1. アプリのビルド
weight: 1
---

このワークショップには、いくつかのRESTエンドポイントを持つシンプルなSpring Bootアプリケーションが含まれています。ビルドしましょう。

## Java と Maven の確認

インスタンスにはOpenJDK 17とMavenがプリインストールされています。確認してください：

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

ワークショップのアプリディレクトリに移動し、fat JARをビルドします：

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
最初の `mvn package` はSpring Bootの依存関係をダウンロードします。30〜60秒かかります。2回目以降のビルドはずっと速くなります。
{{% /notice %}}

## アプリケーションのテスト（AppD なし）

アプリを短時間実行して、起動を確認します：

```bash
java -jar target/ingest-workshop-1.0.0.jar &
```

数秒待ってからテストします：

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

次に進む前にアプリを停止します：

```bash
kill %1
```

アプリケーションは正常に動作しています。次に、AppDynamics Java Agentをダウンロードして、このプロセスにアタッチします。
