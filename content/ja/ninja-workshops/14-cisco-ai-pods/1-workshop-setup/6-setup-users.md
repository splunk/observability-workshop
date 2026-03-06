---
title: ユーザーのセットアップ
linkTitle: 6. ユーザーのセットアップ
weight: 6
time: 5 minutes
---

このセクションでは、ワークショップの各参加者用にユーザーを作成し、それぞれに Namespace とリソースクォータを割り当てます。

## ユーザーの Namespace とリソースクォータの作成

``` bash
cd user-setup
./create-namespaces.sh
```

## ユーザーの作成

参加者の認証情報を含む HTPasswd ファイルを作成し、ROSA が管理する HTPasswd IdP をカスタムのものに置き換えます。

``` bash
./create-users.sh
```

## cluster-admin ユーザーの再作成と再ログイン

cluster-admin ユーザーを再作成し、再度ログインします。

``` bash
rosa create admin -c rosa-test
oc login <Cluster API URL> --username cluster-admin --password <cluster admin password>
```

## ユーザーへのロールの追加

各ユーザーに自分の Namespace のみへのアクセス権を付与します。

``` bash
./add-role-to-users.sh
```

注意: 以下のようなエラーが表示された場合、安全に無視できます。
````
Warning: User 'participant1' not found
clusterrole.rbac.authorization.k8s.io/admin added: "participant1"
````

## ログインのテスト

### OpenShift CLI のインストール

ローカルマシンからログインをテストするには、OpenShift CLI をインストールする必要があります。

MacOS の場合、Homebrew パッケージマネージャーを使用して OpenShift CLI をインストールできます。

``` bash
brew install openshift-cli
```

その他のインストールオプションについては、[OpenShift のドキュメント](https://docs.redhat.com/en/documentation/openshift_container_platform/4.8/html/cli_tools/openshift-cli-oc)を参照してください。

### ワークショップユーザーとしてログイン

ローカルマシンからワークショップユーザーの1人としてログインしてみます。

``` bash
oc login https://api.<cluster-domain>:443 -u participant1 -p 'TempPass123!'
```

以下のように表示されるはずです。

````
Login successful.

You have one project on this server: "workshop-participant-1"
````

### LLM へのアクセスの確認

ワークショップユーザーアカウントから LLM にアクセスできることを確認します。

curl コマンドを使用できる Pod を起動します。

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

次に、以下のコマンドを実行して LLM にプロンプトを送信します。

{{< tabs >}}
{{% tab title="スクリプト" %}}

``` bash
curl -X "POST" \
 'http://meta-llama-3-2-1b-instruct.nim-service:8000/v1/chat/completions' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
        "model": "meta/llama-3.2-1b-instruct",
        "messages": [
        {
          "content":"What is the capital of Canada?",
          "role": "user"
        }],
        "top_p": 1,
        "n": 1,
        "max_tokens": 1024,
        "stream": false,
        "frequency_penalty": 0.0,
        "stop": ["STOP"]
      }'
```

{{% /tab %}}
{{% tab title="出力例" %}}

``` bash
{
  "id": "chatcmpl-2ccfcd75a0214518aab0ef0375f8ca21",
  "object": "chat.completion",
  "created": 1758919002,
  "model": "meta/llama-3.2-1b-instruct",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "reasoning_content": null,
        "content": "The capital of Canada is Ottawa.",
        "tool_calls": []
      },
      "logprobs": null,
      "finish_reason": "stop",
      "stop_reason": null
    }
  ],
  "usage": {
    "prompt_tokens": 42,
    "total_tokens": 50,
    "completion_tokens": 8,
    "prompt_tokens_details": null
  },
  "prompt_logprobs": null
}
```

{{% /tab %}}
{{< /tabs >}}
