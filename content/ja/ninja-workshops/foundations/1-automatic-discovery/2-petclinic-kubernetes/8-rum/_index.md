---
title: Real User Monitoring
linkTitle: 8. Real User Monitoring
weight: 9
time: 10 minutes
archetype: chapter
---

アプリケーションに対して Real User Monitoring (RUM) のインストルメンテーションを有効化するには、Open Telemetry Javascript の [**https://github.com/signalfx/splunk-otel-js-web**](https://github.com/signalfx/splunk-otel-js-web) スニペットをコードベースに追加する必要があります。

Spring PetClinic アプリケーションは、アプリケーションのすべてのビューで再利用される単一の [**index**](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/main/spring-petclinic-api-gateway/src/main/resources/static/index.html) HTML ページを使用しています。このページは、すべてのページで自動的に読み込まれるため、Splunk RUM インストルメンテーションライブラリを挿入するのに最適な場所です。

`api-gateway` サービスではすでにインストルメンテーションが動作しており、RUM トレースを Splunk Observability Cloud に送信しています。次のセクションでこのデータを確認します。

スニペットを確認したい場合は、ブラウザでページを右クリックし、**View Page Source** を選択してページソースを表示できます。

``` html
    <script src="/env.js"></script>  
    <script src="https://cdn.signalfx.com/o11y-gdi-rum/latest/splunk-otel-web.js" crossorigin="anonymous"></script>
    <script src="https://cdn.signalfx.com/o11y-gdi-rum/latest/splunk-otel-web-session-recorder.js" crossorigin="anonymous"></script>
    <script>
        var realm = env.RUM_REALM;
        console.log('Realm:', realm);
        var auth = env.RUM_AUTH;
        var appName = env.RUM_APP_NAME;
        var environmentName = env.RUM_ENVIRONMENT
        if (realm && auth) {
            SplunkRum.init({
                realm: realm,
                rumAccessToken: auth,
                applicationName: appName,
                deploymentEnvironment: environmentName,
                version: '1.0.0',
            });
    
            SplunkSessionRecorder.init({
                applicationName: appName,
                realm: realm,
                rumAccessToken: auth,
                  recorder: "splunk",
                  features: {
                    video: true,
                }
            });
            const Provider = SplunkRum.provider; 
            var tracer=Provider.getTracer('appModuleLoader');
        } else {
        // Realm or auth is empty, provide default values or skip initialization
        console.log("Realm or auth is empty. Skipping Splunk Rum initialization.");
        }
    </script>
     <!-- Section added for  RUM -->
```
