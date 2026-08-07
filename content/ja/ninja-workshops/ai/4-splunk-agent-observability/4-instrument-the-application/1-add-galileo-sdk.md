---
title: Galileo SDKと設定の追加
linkTitle: 1. Galileo SDKの追加
weight: 1
time: 3 minutes
---


まず、Galileoパッケージと、SDKがTraceの送信先を知るために必要な設定を追加します。

{{< exercise title="SDKと設定の追加" >}}

{{< step title="Galileoパッケージの追加" >}}

GalileoのLangChainコールバックは `galileo` パッケージに含まれています。

`~/workshop/healthcare-assistant/2-app-with-instrumentation/requirements.txt` ファイルを開き、ファイルの末尾に以下を追加します。

````
galileo
````

{{< /step >}}

{{< step title="環境変数の設定" >}}

ワークショップのインストラクターから提供されたコマンドを実行して、EC2インスタンスに環境変数を設定します。コマンドは以下のようになります。

````
export PARTICIPANT_NUMBER=<your participant number>  
export GALILEO_API_KEY=<provided by workshop instructor>  
export GALILEO_CONSOLE_URL=<provided by workshop instructor>
````

{{< /step >}}

{{< step title="Galileo Secretの作成" >}}

以下のコマンドを実行して、Galileo APIキーを格納するKubernetes Secretを作成します。

```bash
kubectl create secret generic galileo-secret \
  --from-literal=GALILEO_API_KEY="$GALILEO_API_KEY"
```

{{< /step >}}

{{< step title="Galileo Config Mapの作成" >}}

以下のコマンドを実行して、Kubernetes Config Mapを作成します。アプリケーションはこれを使用してGalileoへのTrace送信方法を決定します。

```bash
kubectl create configmap galileo-config \
  --from-literal=GALILEO_CONSOLE_URL="$GALILEO_CONSOLE_URL" \
  --from-literal=GALILEO_PROJECT="project-$PARTICIPANT_NUMBER" \
  --from-literal=GALILEO_LOG_STREAM="default"
```

{{% notice title="Projectとlog stream" style="info" %}}

`GALILEO_PROJECT` と `GALILEO_LOG_STREAM` は、GalileoコンソールでTraceが表示される場所を決定します。空のままにすると、SDKはProjectとlog streamの両方が `default` という名前にフォールバックします。

{{% /notice %}}

{{< /step >}}

{{< /exercise >}}

{{< checkpoint title="確認テスト" >}}

`galileo-config` Config Mapから `GALILEO_PROJECT` と `GALILEO_LOG_STREAM` を削除した場合、Traceはどこに表示されますか？

{{< details summary="回答を表示" >}}
`default` という名前のProjectと `default` という名前のlog streamに表示されます。これらのキーが空の場合、`setup_env.py` は空の `GALILEO_PROJECT` / `GALILEO_LOG_STREAM` 値をエクスポートし、Galileo SDKは組み込みの `default` Projectと `default` log streamにフォールバックします。
{{< /details >}}
