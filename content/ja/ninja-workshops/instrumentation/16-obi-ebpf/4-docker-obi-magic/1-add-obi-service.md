---
title: 1. OBI サービスの追加
weight: 1
---

## docker-compose.yaml に OBI を追加する

{{% notice title="演習" style="green" icon="running" %}}

エディタで `docker-compose.yaml` を開きます。

``` bash
cd ~/workshop/obi/02-obi-docker
docker-compose down
vim docker-compose.yaml #or editor of choice
```

ファイルの一番下までスクロールすると、`PHASE 2` というコメントブロックがあります。**そのコメントの直下**に以下のブロックを貼り付けます。`frontend:` や `load-generator:` などの他のサービスと揃うように、**2スペースのインデント**を維持してください。

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

**注意:** vim で貼り付ける際は、貼り付け前に `:set paste` を実行するとフォーマットが維持されます。

ファイルを保存します。

{{% /notice %}}

{{% notice title="ヒント" style="primary" icon="lightbulb" %}}
`obi:` が 2 スペースインデントされていること（`frontend:` や `load-generator:` などと同じレベル）を確認してください。インデントなしで一番左にある場合、Docker Compose は `Additional property obi is not allowed` というエラーで拒否します。`services:` ブロックの**内側**に配置する必要があります。
{{% /notice %}}

### 各行の役割

| 行 | 内容 | 重要性 |
|---|---|---|
| `image: otel/ebpf-instrument:main` | [OBI コンテナイメージ](https://hub.docker.com/r/otel/ebpf-instrument) | スタックに追加するのはこれだけです |
| `pid: host` | ホストの PID 名前空間を共有します | OBI が**他の**コンテナで実行されているプロセスを参照できる必要があります |
| `privileged: true` | カーネルレベルのアクセス権を付与します | eBPF プログラムはカーネル関数にプローブをアタッチする必要があります |
| `network_mode: host` | ホストのネットワークスタックを共有します | コンテキスト伝播に必要です。OBI はネットワークレベルでトレースコンテキストを注入します |
| `volumes: ./obi-config.yaml:...` | サービスディスカバリ設定をマウントします | OBI に対して、計装するプロセスとその名前を指定します |
| `volumes: /sys/fs/cgroup:...` | cgroup ファイルシステムをマウントします | OBI はこれを使用して、コンテナ内で実行されているプロセスを検出します |
| `OTEL_EBPF_CONFIG_PATH` | コンテナ内の設定ファイルを指定します | OBI 設定用の標準環境変数です |

## OBI を起動する

Docker Compose は `obi` サービスのみが新規であることを検出し、それを起動します。既存のサービスはそのまま実行され続けます。

{{< tabs >}}
{{% tab title="スクリプト" %}}

``` bash
docker-compose up -d
```

{{% /tab %}}
{{% tab title="出力例" %}}

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
