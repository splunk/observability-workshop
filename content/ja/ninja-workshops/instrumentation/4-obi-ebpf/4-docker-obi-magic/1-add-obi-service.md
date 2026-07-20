---
title: 1. OBIサービスの追加
weight: 1
---

## docker-compose.yamlにOBIを追加する

{{% notice title="Exercise" style="green" icon="running" %}}

エディタで `docker-compose.yaml` を開きます。

``` bash
cd ~/workshop/obi/02-obi-docker
docker-compose down
vim docker-compose.yaml #or editor of choice
```

ファイルの一番下までスクロールすると、`PHASE 2` というコメントブロックがあります。そのコメントの **直下** に以下のブロックを貼り付けます。他のサービス（`frontend:`、`load-generator:` など）と揃うように **2スペースのインデント** を維持してください。

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

**注意:** vimで貼り付ける場合、事前に `:set paste` を実行するとフォーマットが維持されます

ファイルを保存します。

{{% /notice %}}

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
`obi:` が2スペースでインデントされていることを確認してください（`frontend:`、`load-generator:` などと同じレベル）。インデントなしで左端に配置されている場合、Docker Composeは `Additional property obi is not allowed` というエラーで拒否します。`services:` ブロックの **内側** に配置する必要があります。
{{% /notice %}}

### 各行の説明

| 行 | 内容 | 重要な理由 |
|---|---|---|
| `image: otel/ebpf-instrument:main` | [OBIコンテナイメージ](https://hub.docker.com/r/otel/ebpf-instrument) | スタックに追加する唯一のものです |
| `pid: host` | ホストのPID名前空間を共有します | OBIは **他の** コンテナで実行中のプロセスを確認する必要があります |
| `privileged: true` | カーネルレベルのアクセスを許可します | eBPFプログラムはカーネル関数にプローブをアタッチする必要があります |
| `network_mode: host` | ホストのネットワークスタックを共有します | コンテキスト伝播に必要です -- OBIはネットワークレベルでトレースコンテキストを注入します |
| `volumes: ./obi-config.yaml:...` | サービスディスカバリ設定をマウントします | どのプロセスを計装し、どのような名前を付けるかをOBIに伝えます |
| `volumes: /sys/fs/cgroup:...` | cgroupファイルシステムをマウントします | OBIはこれを使用してコンテナ内で実行中のプロセスを検出します |
| `OTEL_EBPF_CONFIG_PATH` | コンテナ内の設定ファイルを指定します | OBIの標準的な設定用環境変数です |

## OBIの起動

Docker Composeは `obi` サービスのみが新しいことを検出し、それを起動します。既存のサービスは稼働し続けます。

{{< tabs >}}
{{% tab title="Script" %}}

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
