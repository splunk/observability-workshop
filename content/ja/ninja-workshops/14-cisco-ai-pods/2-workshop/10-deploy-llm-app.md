---
title: LLM アプリケーションのデプロイ
linkTitle: 10. LLM アプリケーションのデプロイ
weight: 10
time: 10 minutes
---

## LLM アプリケーションのデプロイ

以下のコマンドを使用して、このアプリケーションを OpenShift クラスターにデプロイします:

``` bash
oc apply -f ./llm-app/k8s-manifest.yaml
```

> 注意: この Python アプリケーションの Docker イメージをビルドするために、以下のコマンドを実行しました:
> ``` bash
> cd workshop/cisco-ai-pods/llm-app
> docker build --platform linux/amd64 -t ghcr.io/splunk/cisco-ai-pod-workshop-app:1.0 .
> docker push ghcr.io/splunk/cisco-ai-pod-workshop-app:1.0
> ```

## LLM アプリケーションのテスト

アプリケーションが期待どおりに動作していることを確認しましょう。

curl コマンドにアクセスできる Pod を起動します:

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

次に、以下のコマンドを実行して LLM に質問を送信します:

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
