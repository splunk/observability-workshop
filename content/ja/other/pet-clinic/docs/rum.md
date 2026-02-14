---
title: Real User Monitoring
linkTitle: 4. Real User Monitoring
weight: 4
---

## 1. RUMを有効にする

Real User Monitoring (RUM)計装のために、Open Telemetry Javascript [https://github.com/signalfx/splunk-otel-js-web](https://github.com/signalfx/splunk-otel-js-web) スニペットをページ内に追加します。再度ウィザードを使用します **Data Management → Add Integrationボタン → Monitor user experience（画面上部タブ） → Browser Instrumentation**を開きます。

ドロップダウンから設定済みの **RUM ACCESS TOKEN** を選択し、**Next** をクリックします。以下の構文で **App name** と**Environment** を入力します：

次に、ワークショップのRUMトークンを選択し、 App nameとEnvironmentを定義します。ウィザードでは、ページ上部の `<head>` セクションに配置する必要のあるHTMLコードの断片が表示されます。この例では、次のように記述していますが、ウィザードでは先程入力した値が反映されてるはずです。

- Application Name: `<hostname>-petclinic-service`
- Environment: `<hostname>-petclinic-env`

ウィザードで編集済みコードスニペットをコピーするか、以下のスニペットをコピーして適宜編集してください。ただし：

- `[hostname]-petclinic-service` - `[hostname]` をお使いのホスト名に書き換えてください
- `[hostname]-petclinic-env` - `[hostname]` をお使いのホスト名に書き換えてください

``` html
  <script src="https://cdn.signalfx.com/o11y-gdi-rum/latest/splunk-otel-web.js" crossorigin="anonymous"></script>
  <script>
  SplunkRum.init({
      beaconUrl: "https://rum-ingest.<REALM>.signalfx.com/v1/rum",
      rumAuth: "<RUM_ACCESS_TOKEN>",
      app: "<hostname>.service",
      environment: "<hostname>"
    });
  </script>
```

Spring PetClinicアプリケーションでは、1つのHTMLページを「レイアウト」ページとして使用し、アプリケーションのすべてのページで再利用しています。これは、Splunk RUM計装ライブラリを挿入するのに最適な場所であり、すべてのページで自動的に読み込まれます。

では、レイアウトページを編集してみましょう：

```bash
nano src/main/resources/templates/fragments/layout.html
```


そして、上で生成したスニップをページの `<head>` セクションに挿入してみましょう。さて、アプリケーションを再構築して、再び実行する必要があります。

## 2. PetClinicを再ビルドする

mavenコマンドを実行して、PetClinicをコンパイル/ビルド/パッケージ化します：

```bash
./mvnw package -Dmaven.test.skip=true
```


そして、アプリケーションを動かしてみましょう。バージョンを `version=0.316` とするのをお忘れなく。

```bash
java -javaagent:./splunk-otel-javaagent.jar \
-Dserver.port=8083 \
-Dotel.service.name=$(hostname).service \
-Dotel.resource.attributes=deployment.environment=$(hostname),version=0.316 \
-Dsplunk.profiler.enabled=true \
-Dsplunk.profiler.memory.enabled=true \
-Dsplunk.metrics.enabled=true \
-jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```


{{% notice title="versionを自動で設定する" style="info" %}}
ここまできて `version` を毎回変えるためにコマンドラインを修正するのは大変だと思うことでしょう。実際、修正が漏れた人もいるかもしれません。
本番環境では、環境変数でアプリケーションバージョンを与えたり、コンテナイメージの作成時にビルドIDを与えたりすることになるはずです。
{{% /notice %}}

次に、より多くのトラフィックを生成するために、アプリケーションに再度アクセスしてみましょう。 `http://<VM_IP_ADDRESS>:8083` にアクセスすると、今度はRUMトレースが報告されるはずです。

RUMにアクセスして、トレースとメトリクスのいくつかを見てみましょう。左のメニューから **RUM** を選ぶと、Spring Pet Clinicでのユーザー（あなたです！）が体験したパフォーマンスが表示されます。
