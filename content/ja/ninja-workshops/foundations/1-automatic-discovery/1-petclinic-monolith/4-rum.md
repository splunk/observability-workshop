---
title: 3. Real User Monitoring
weight: 3
---

Real User Monitoring (RUM) のインストルメンテーションでは、Open Telemetry Javascript [**https://github.com/signalfx/splunk-otel-js-web**](https://github.com/signalfx/splunk-otel-js-web) のスニペットをページに追加します。再びウィザード **Data Management → Add Integration → RUM Instrumentation → Browser Instrumentation** を使用します。

ドロップダウンから使用するトークンについてはインストラクターから案内があります。トークンを選択したら **Next** をクリックします。**App name** と **Environment** を以下の構文で入力してください。

- `<INSTANCE>-petclinic-service` - `<INSTANCE>` は先ほどメモした値に置き換えてください。
- `<INSTANCE>-petclinic-env` - `<INSTANCE>` は先ほどメモした値に置き換えてください。

ウィザードでは、ページの `<head>` セクション先頭に配置する HTML コードのスニペットが表示されます。以下はその例です（このスニペットは使用せず、ウィザードで生成されたものを使用してください）。

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

Spring PetClinic アプリケーションでは、単一の HTML ページを「レイアウト」ページとして使用しており、これがアプリケーションのすべてのページで再利用されています。Splunk RUM Instrumentation Library を挿入するには最適な場所であり、すべてのページで自動的に読み込まれます。

それでは、レイアウトページを編集しましょう。

```bash
vi src/main/resources/templates/fragments/layout.html
```

次に、上で生成したスニペットをページの `<head>` セクションに挿入します。コメント部分は含めないようにし、source URL の `<version>` を `latest` に置き換えてください。例：

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

コードの変更が完了したら、アプリケーションをリビルドして再度実行する必要があります。`maven` コマンドを実行して PetClinic をコンパイル/ビルド/パッケージ化します。

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

次にブラウザで `http://<IP_ADDRESS>:8083` にアクセスし、実ユーザーのトラフィックを生成します。

RUM では、上記の RUM スニペットで定義した environment で絞り込み、ダッシュボードまでクリックして進みます。

RUM トレースをドリルダウンすると、スパン内に APM へのリンクが表示されます。trace ID をクリックすると、現在の RUM トレースに対応する APM トレースに移動できます。
