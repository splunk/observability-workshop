---
title: 3. Real User Monitoring
weight: 3
---

Real User Monitoring (RUM) の計装では、ページに OpenTelemetry Javascript スニペット [**https://github.com/signalfx/splunk-otel-js-web**](https://github.com/signalfx/splunk-otel-js-web) を追加します。ウィザードを使用して **Data Management → Add Integration → RUM Instrumentation → Browser Instrumentation** の順に進みます。

インストラクターがドロップダウンから使用するトークンを指示します。**Next** をクリックしてください。以下の形式で **App name** と **Environment** を入力します：

- `<INSTANCE>-petclinic-service` - `<INSTANCE>` を先ほどメモした値に置き換えてください。
- `<INSTANCE>-petclinic-env` - `<INSTANCE>` を先ほどメモした値に置き換えてください。

ウィザードは、ページの `<head>` セクションの先頭に配置する必要がある HTML コードスニペットを表示します。以下は例です（このスニペットは使用せず、ウィザードが生成したものを使用してください）：

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

Spring PetClinic アプリケーションは、アプリケーションのすべてのページで再利用される単一の HTML ページを「レイアウト」ページとして使用しています。Splunk RUM 計装ライブラリを挿入するには、すべてのページで自動的に読み込まれるため、この場所が最適です。

それでは、レイアウトページを編集しましょう：

```bash
vi src/main/resources/templates/fragments/layout.html
```

次に、上記で生成したスニペットをページの `<head>` セクションに挿入します。コメントは含めず、ソース URL の `<version>` を `latest` に置き換えてください：

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

コード変更が完了したら、アプリケーションを再ビルドして再度実行する必要があります。`maven` コマンドを実行して PetClinic をコンパイル/ビルド/パッケージ化します：

```bash
./mvnw package -Dmaven.test.skip=true
```

```bash
java \
-Dserver.port=8083 \
-Dotel.service.name=$INSTANCE-petclinic-service \
-Dotel.resource.attributes=deployment.environment=$INSTANCE-petclinic-env,version=0.314 \
-jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```

次に、ブラウザを使用してアプリケーション `http://<IP_ADDRESS>:8083` にアクセスし、実際のユーザートラフィックを生成します。

RUM で、上記の RUM スニペットで定義された環境にフィルタリングし、ダッシュボードをクリックして開きます。

RUM トレースをドリルダウンすると、スパン内に APM へのリンクが表示されます。トレース ID をクリックすると、現在の RUM トレースに対応する APM トレースに移動します。
