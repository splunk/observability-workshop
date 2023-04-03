---
title: 4. Real User Monitoring
weight: 4
---

## 1. RUMを有効にする

Real User Monitoring (RUM)計装のために、Open Telemetry Javascript [https://github.com/signalfx/splunk-otel-js-web](https://github.com/signalfx/splunk-otel-js-web) スニペットをページ内に追加します。再度ウィザードを使用します **Data Management → Add Integration → RUM Instrumentation → Browser Instrumentation**.

ドロップダウンから設定済みの **RUM ACCESS TOKEN** を選択し、**Next** をクリックします。以下の構文で**アプリ名**と**環境**を入力します：

- ホスト名]-petclinic-service` - [ホスト名]`を実際のホスト名で置き換えます。
- hostname]-petclinic-env` - `[hostname]`を実際のホスト名に置き換えてください。

次に、ワークショップのRUMトークンを選択し、アプリケーション名と環境名を定義する必要があります。ウィザードでは、ページ上部の `<head>` セクションに配置する必要のある HTML コードの断片が表示されます。この例では、次のように記述します：

- アプリケーション名 アプリケーション名： `<ホスト名>-petclinic-service`。
- 環境：`<ホスト名>-petclinic-env`。

ウィザードで編集済みコードスニペットをコピーするか、以下のスニペットをコピーして適宜編集してください：

``` html
<script src="https://cdn.signalfx.com/o11y-gdi-rum/latest/splunk-otel-web.js" crossorigin="anonymous"></script> です。
<script>
SplunkRum.init({)
    beaconUrl： "https://rum-ingest.<REALM>.signalfx.com/v1/rum" です、
    rumAuth: "<RUM_ACCESS_TOKEN>"、
    アプリになります： "<ホスト名>-petclinic-service "です、
    の環境下で使用することができます： "<ホスト名>-petclinic-env "です。
    });
</script>
```

Spring PetClinicアプリケーションでは、1つのHTMLページを「レイアウト」ページとして使用し、アプリケーションのすべてのページで再利用しています。これは、Splunk RUM計装ライブラリを挿入するのに最適な場所であり、すべてのページで自動的に読み込まれます。

では、レイアウトページを編集してみましょう：

```bash
nano src/main/resources/templates/fragments/layout.html
```

そして、上で生成したスニップをページの `<head>` セクションに挿入してみましょう。さて、アプリケーションを再構築して、再び実行する必要があります：

## 2. PetClinicをリビルドする

mavenコマンドを実行して、PetClinicをコンパイル/ビルド/パッケージ化します：

バッシュ
./mvnw パッケージ -Dmaven.test.skip=true
```

(`・ω・´)バシッ
ジャバ
-Dotel.service.name=$(hostname)-petclinic.service \
-Dsplunk.profiler.enabled=true◎。
-Dsplunk.メトリクス.enabled=true ㊤。
-jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```

次に、より多くのトラフィックを生成するために、アプリケーションに再度アクセスしてみましょう。http://<VM_IP_ADDRESS>:8080`、今度はRUMトレースが報告されるはずです。

RUMにアクセスして、トレースとメトリクスのいくつかを見てみましょう **Hamburger Menu → RUM** すると、UIに表示されるSpring PetClinicのURLのいくつかが表示されます。

---
title: 4. Real User Monitoring
weight: 4
---

## 1. Enable RUM

For the Real User Monitoring (RUM) instrumentation, we will add the Open Telemetry Javascript [https://github.com/signalfx/splunk-otel-js-web](https://github.com/signalfx/splunk-otel-js-web) snippet in the pages, we will use the wizard again **Data Management → Add Integration → RUM Instrumentation → Browser Instrumentation**.

Select the preconfigured **RUM ACCESS TOKEN** from the dropdown, click **Next**. Enter **App name** and **Environment** using the following syntax:

- `[hostname]-petclinic-service` - replacing `[hostname]` with your actual hostname.
- `[hostname]-petclinic-env` - replacing `[hostname]` with your actual hostname.

Then you'll need to select the workshop RUM token and define the application and environment names. The wizard will then show a snipped of HTML code that needs to be place at the top at the pages in the `<head>` section. In this example we are using:

- Application Name: `<hostname>-petclinic-service`
- Environment: `<hostname>-petclinic-env`

Copy the generated code snippet in the wizard or copy and edit the snippet below accordingly:

``` html
<script src="https://cdn.signalfx.com/o11y-gdi-rum/latest/splunk-otel-web.js" crossorigin="anonymous"></script>
<script>
SplunkRum.init({
    beaconUrl: "https://rum-ingest.<REALM>.signalfx.com/v1/rum",
    rumAuth: "<RUM_ACCESS_TOKEN>",
    app: "<hostname>-petclinic-service",
    environment: "<hostname>-petclinic-env"
    });
</script>
```

The Spring PetClinic application uses a single HTML page as the "layout" page, that is reused across all pages of the application. This is the perfect location to insert the Splunk RUM Instrumentation Library as it will be loaded in all pages automatically.

Let's then edit the layout page:

```bash
vi src/main/resources/templates/fragments/layout.html
```

and let's insert the snipped we generated above in the `<head>` section of the page. Now we need to rebuild the application and run it again:

## 2. Rebuild PetClinic

run the maven command to compile/build/package PetClinic:

```bash
./mvnw package -Dmaven.test.skip=true
```

```bash
java \
-Dotel.service.name=$(hostname)-petclinic.service \
-Dsplunk.profiler.enabled=true \
-Dsplunk.metrics.enabled=true \
-jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```

Then let's visit the application again to generate more traffic `http://<VM_IP_ADDRESS>:8080`, now we should see RUM traces being reported

Let's visit RUM and see some of the traces and metrics **Hamburger Menu → RUM** and you will see some of the Spring PetClinic URLs showing up in the UI.
