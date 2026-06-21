---
title: 1. OBI サービスの追加
weight: 1
---

## docker-compose.yaml に OBI を追加する

{{% notice title="Exercise" style="green" icon="running" %}}

エディタで `docker-compose.yaml` を開きます:

``` bash
cd ~/workshop/obi/02-obi-docker
docker-compose down
vim docker-compose.yaml #or editor of choice
```

ファイルの一番下までスクロールすると、`PHASE 2` というコメントブロックがあります。そのコメントの**直下**に以下のブロックを貼り付けてください。他のサービス（`frontend:`、`load-generator:` など）と揃うように **2スペースのインデント**を維持してください:

``` yaml
  obi:
    image: otel/ebpf-instrument:main
    pid: host
    privileged: true
    network_mode: host
    volumes:
      - ./obi-config.yaml:/config/obi-config.yaml
      - /sys/fs/cgroup:/sys/fs/cgroup
    environment:
      OTEL_EBPF_CONFIG_PATH: /config/obi-config.yaml
```

**注意:** vim で貼り付ける際は、事前に `:set paste` を実行するとフォーマットが崩れません

ファイルを保存します。

{{% /notice %}}

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
`obi:` が2スペースでインデントされていることを確認してください（`frontend:`、`load-generator:` などと同じレベル）。インデントなしで左端に配置されている場合、Docker Compose は `Additional property obi is not allowed` というエラーで拒否します。`services:` ブロックの**内側**に配置する必要があります。
{{% /notice %}}

### 各行の意味

| 行 | 動作 | 重要な理由 |
|---|---|---|
| `image: otel/ebpf-instrument:main` | [OBI コンテナイメージ](https://hub.docker.com/r/otel/ebpf-instrument) | スタックに追加する唯一のものです |
| `pid: host` | ホストの PID 名前空間を共有します | OBI は**他の**コンテナで実行されているプロセスを確認する必要があります |
| `privileged: true` | カーネルレベルのアクセスを付与します | eBPF プログラムはカーネル関数にプローブをアタッチする必要があります |
| `network_mode: host` | ホストのネットワークスタックを共有します | コンテキスト伝播に必要です -- OBI はネットワークレベルでトレースコンテキストを注入します |
| `volumes: ./obi-config.yaml:...` | サービスディスカバリ設定をマウントします | どのプロセスを計装し、どのような名前を付けるかを OBI に指示します |
| `volumes: /sys/fs/cgroup:...` | cgroup ファイルシステムをマウントします | OBI はこれを使用してコンテナ内で実行されているプロセスを検出します |
| `OTEL_EBPF_CONFIG_PATH` | コンテナ内の設定ファイルを指定します | OBI の標準設定用環境変数です |

## OBI の起動

Docker Compose は `obi` サービスのみが新しいことを検出し、それを起動します。既存のサービスはそのまま実行され続けます。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
docker-compose up -d
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
[+] Running 6/6
 ✔ Container 02-obi-docker-payment-service-1      Running
 ✔ Container 02-obi-docker-order-processor-1       Running
 ✔ Container 02-obi-docker-frontend-1              Running
 ✔ Container 02-obi-docker-splunk-otel-collector-1 Running
 ✔ Container 02-obi-docker-load-generator-1        Running
 ✔ Container 02-obi-docker-obi-1                   Started
```

{{% /tab %}}
{{< /tabs >}}
