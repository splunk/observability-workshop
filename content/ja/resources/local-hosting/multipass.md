---
title: Multipass
weight: 1
description: Multipass を使用したローカルホスティング環境の作成方法 - Windows/Linux/Mac(Intel)
---

お使いのオペレーティングシステムに [Multipass](https://multipass.run/) と Terraform をインストールします。Mac (Intel) では、[Homebrew](https://brew.sh/) を使用してインストールすることもできます。例

```text
brew install multipass terraform jq
```

ワークショップリポジトリをクローンします

```bash
git clone https://github.com/splunk/observability-workshop
```

Multipass ディレクトリに移動します

```bash
cd observability-workshop/local-hosting/multipass
```

Log Observer Connect:

独自の Splunk Observability Cloud Suite Org や Splunk インスタンスを使用する場合は、新しい **Log Observer Connect** 接続を作成する必要があります。
[Splunk Cloud](https://docs.splunk.com/observability/en/logs/scp.html#logs-scp) または [Splunk Enterprize](https://docs.splunk.com/observability/en/logs/set-up-logconnect.html) の[ドキュメント](https://docs.splunk.com/observability/en/logs/lo-connect-landing.html)に記載されている手順に従ってください。

独自の **Log Observer Connect** 接続を実行するための追加要件は以下のとおりです

- **splunk4rookies-workshop** というインデックスを作成します
- **Log Observer Connect** 接続で使用されるサービスアカウントユーザーが **splunk4rookies-workshop** インデックスにアクセスできることを確認します（すべてのワークショップログデータはこのインデックスに送信されるため、他のすべてのインデックスを削除できます）。

Terraform を初期化します

{{< tabs >}}
{{% tab title="Command" %}}

```bash
terraform init -upgrade
```

{{< /tab >}}
{{< tab title="Example Output" >}}

```text
Initializing the backend...

Initializing provider plugins...
- Finding latest version of hashicorp/random...
- Finding latest version of hashicorp/local...
- Finding larstobi/multipass versions matching "~> 1.4.1"...
- Installing hashicorp/random v3.5.1...
- Installed hashicorp/random v3.5.1 (signed by HashiCorp)
- Installing hashicorp/local v2.4.0...
- Installed hashicorp/local v2.4.0 (signed by HashiCorp)
- Installing larstobi/multipass v1.4.2...
- Installed larstobi/multipass v1.4.2 (self-signed, key ID 797707331BF3549C)
```

{{< /tab >}}
{{< /tabs >}}

Terraform 変数ファイルを作成します。変数はファイル `terrform.tfvars` に保存されます。テンプレート `terraform.tfvars.template` が提供されているので、コピーして編集します

```bash
cp terraform.tfvars.template terraform.tfvars
```

以下の Terraform 変数が必要です

- `swipe_id`: インスタンスの [SWiPE ID](https://swipe.splunk.com/)
- `splunk_index`: ログの送信先の Splunk Index。デフォルトは `splunk4rookies-workshop` です。

インスタンスタイプ変数

- `splunk_presetup`: 事前設定済みのインスタンスを提供します（OTel Collector と Online Boutique が RUM 有効でデプロイされます）。デフォルトは `false` です。
- `splunk_diab`: Demo-in-a-Box をインストールして実行します。デフォルトは `false` です。
- `tagging_workshop`: Tagging Workshop をインストールして設定します。デフォルトは `false` です。
- `otel_demo` : OpenTelemetry Astronomy Shop Demo をインストールして設定します。これには `splunk_presetup` が `false` に設定されている必要があります。デフォルトは `false` です。

オプションの詳細変数

- `wsversion`: ワークショップの開発作業中の場合は `main` に設定します。それ以外の場合は省略できます。
- `architecture`: 正しいアーキテクチャ（`arm64` または `amd64`）に設定します。デフォルトは Apple Silicon に適した `arm64` です。

`terraform plan` を実行してすべての設定が正しいことを確認します。問題がなければ `terraform apply` を実行してインスタンスを作成します。

{{< tabs >}}
{{% tab title="Command" %}}

```bash
terraform apply
```

{{< /tab >}}
{{% tab title="Example Output" %}}

``` text
random_string.hostname: Creating...
random_string.hostname: Creation complete after 0s [id=cynu]
local_file.user_data: Creating...
local_file.user_data: Creation complete after 0s [id=46a5c50e396a1a7820c3999c131a09214db903dd]
multipass_instance.ubuntu: Creating...
multipass_instance.ubuntu: Still creating... [10s elapsed]
multipass_instance.ubuntu: Still creating... [20s elapsed]
...
multipass_instance.ubuntu: Still creating... [1m30s elapsed]
multipass_instance.ubuntu: Creation complete after 1m38s [name=cynu]
data.multipass_instance.ubuntu: Reading...
data.multipass_instance.ubuntu: Read complete after 1s [name=cynu]

Apply complete! Resources: 3 added, 0 changed, 0 destroyed.

Outputs:

instance_details = [
  {
    "image" = "Ubuntu 22.04.2 LTS"
    "image_hash" = "345fbbb6ec82 (Ubuntu 22.04 LTS)"
    "ipv4" = "192.168.205.185"
    "name" = "cynu"
    "state" = "Running"
  },
]
```

{{% /tab %}}
{{< /tabs >}}

インスタンスが正常に作成されたら（数分かかる場合があります）、上記の出力に表示された `name` を使用してインスタンスに `exec` で接続します。Multipass インスタンスのパスワードは `Splunk123!` です。

{{< tabs >}}
{{% tab title="Command" %}}

```bash
multipass exec cynu -- su -l splunk
```

{{< /tab >}}
{{% tab title="Example Output" %}}

```text
$ multipass exec kdhl -- su -l splunk
Password:
Waiting for cloud-init status...
Your instance is ready!
```

{{% /tab %}}
{{< /tabs >}}

インスタンスを検証します

```bash
kubectl version --output=yaml
```

インスタンスを削除するには、まずインスタンスから退出し、次のコマンドを実行します

```bash
terraform destroy
```
