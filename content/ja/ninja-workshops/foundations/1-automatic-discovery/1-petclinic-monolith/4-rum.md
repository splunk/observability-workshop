---
title: 3. Real User Monitoring
weight: 3
---

Real User Monitoring (RUM) の計装では、Spring PetClinic アプリケーションが返すページに OpenTelemetry Javascript [**https://github.com/signalfx/splunk-otel-js-web**](https://github.com/signalfx/splunk-otel-js-web) スニペットを追加します。これを行うには、Splunk Observability Cloud で **Data Management → Available Integrations → RUM Instrumentation → Browser Instrumentation** に移動します。

**Next** をクリックします。インストラクターが Access token ドロップダウンから選択するトークンを案内します。再度 **Next** をクリックします。以下の構文を使用して **App name** と **Environment** を入力します

- `<INSTANCE>-petclinic-service` - `<INSTANCE>` を先ほどメモした値に置き換えてください。
- `<INSTANCE>-petclinic-env` - `<INSTANCE>` を先ほどメモした値に置き換えてください。

ウィザードは、ページの `<head>` セクションの先頭に配置する必要がある HTML コードのスニペットを表示します。以下はスニペットの例です（この例は使用せず、ウィザードで生成されたバージョンを使用してください）

``` html
/*

IMPORTANT: Replace the <version> placeholder in the src URL with a
version from https://github.com/signalfx/splunk-otel-js-web/releases

*/
<script src="https://cdn.signalfx.com/o11y-gdi-rum/latest/splunk-otel-web.js" crossorigin="anonymous"></script>
<script>
    SplunkRum.init({
        realm: "eu0",
        rumAccessToken: "<redacted>",
        applicationName: "petclinic-1be0-petclinic-service",
        deploymentEnvironment: "petclinic-1be0-petclinic-env"
    });
</script>
```

スニペットをクリップボードまたはテキストエディタにコピーします。

Spring PetClinic アプリケーションは、アプリケーションのすべてのページで再利用される単一の HTML ページを「レイアウト」ページとして使用しています。これは Splunk RUM Instrumentation Library を挿入するのに最適な場所です。すべてのページで自動的に読み込まれるためです。

レイアウトページを編集してスニペットを追加しましょう

```bash
vi src/main/resources/templates/fragments/layout.html
```

次に、前のステップで生成したスニペットをページの `<head>` セクションに挿入します。スニペットに自動的に追加されたコメントは含めず、ソース URL の `<version>` を `latest` に置き換えてください。例

```html
<!doctype html>
<html th:fragment="layout (template, menu)">

<head>
<script src="https://cdn.signalfx.com/o11y-gdi-rum/latest/splunk-otel-web.js" crossorigin="anonymous"></script>
<script>
    SplunkRum.init({
        realm: "eu0",
        rumAccessToken: "<redacted>",
        applicationName: "petclinic-1be0-petclinic-service",
        deploymentEnvironment: "petclinic-1be0-petclinic-env"
    });
</script>
...
```

コード変更が完了したら、アプリケーションを再ビルドして再度実行する必要があります。`maven` コマンドを実行して PetClinic をコンパイル、ビルド、パッケージします

```bash
./mvnw package -Dmaven.test.skip=true
```

次に、更新されたアプリケーションを起動します

```bash
java \
-Dserver.port=8083 \
-Dotel.service.name=$INSTANCE-petclinic-service \
-Dotel.resource.attributes=deployment.environment=$INSTANCE-petclinic-env,version=0.314 \
-jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```

次に、ブラウザを使用してアプリケーションにアクセスし、実際のユーザートラフィックを生成します`http://<IP_ADDRESS>:8083`

RUM で、上記の RUM スニペットで定義した環境にフィルタリングし、ダッシュボードをクリックして表示します。

RUM トレースをドリルダウンすると、スパン内に APM へのリンクが表示されます。トレース ID をクリックすると、現在の RUM トレースに対応する APM トレースに移動します。
