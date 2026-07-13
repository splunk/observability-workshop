---
title: LLMアプリケーションのデプロイ
linkTitle: 10. LLMアプリケーションのデプロイ
weight: 10
time: 10 minutes
---

## LLMアプリケーションのデプロイ

以下のコマンドを使用して、このアプリケーションをOpenShiftクラスターにデプロイします。

``` bash
cd ~/workshop/cisco-ai-pods
oc apply -f ./llm-app/k8s-manifest.yaml
```

> [!NOTE]
> このPythonアプリケーションのDockerイメージをビルドするために、以下のコマンドを実行しました:
>
> ``` bash
> cd workshop/cisco-ai-pods/llm-app
> docker build --platform linux/amd64 -t ghcr.io/splunk/cisco-ai-pod-workshop-app:1.0 .
> docker push ghcr.io/splunk/cisco-ai-pod-workshop-app:1.0
> ```

## LLMアプリケーションのテスト

アプリケーションが期待通りに動作していることを確認しましょう。

curlコマンドにアクセスできるPodを起動します。

``` bash
oc run curl --rm -it --image=curlimages/curl:latest \
  --overrides='{
    "spec": {
      "containers": [{
        "name": "curl",
        "image": "curlimages/curl:latest",
        "stdin": true,
        "tty": true,
        "command": ["sh"],
        "resources": {
          "limits": {
            "cpu": "50m",
            "memory": "100Mi"
          },
          "requests": {
            "cpu": "50m",
            "memory": "100Mi"
          }
        }
      }]
    }
  }'
```

次に、以下のコマンドを実行してLLMに質問を送信します。

{{< tabs >}}
{{% tab title="スクリプト" %}}

``` bash
curl -X "POST" \
 'http://llm-app:8080/askquestion' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "question": "How much memory does the NVIDIA H200 have?"
  }'
```

{{% /tab %}}
{{% tab title="出力例" %}}

``` bash
The NVIDIA H200 has 141GB of HBM3e memory, which is twice the capacity of the NVIDIA H100 Tensor Core GPU with 1.4X more memory bandwidth.
```

{{% /tab %}}
{{< /tabs >}}
