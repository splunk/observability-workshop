---
title: Multipass
weight: 1
description: Windows、Linux、Intel Mac での Multipass によるローカルホスティング。
---

お使いの OS 用の [Multipass](https://multipass.run/) と Terraform をインストールしてください。Mac (Intel) では、[Homebrew](https://brew.sh/) 経由でもインストールできます。例えば次のように実行します。

```text
brew install multipass terraform jq
```

ワークショップのリポジトリをクローンします。

```bash
git clone https://github.com/splunk/observability-workshop
```

Multipass ディレクトリに移動します。

```bash
cd observability-workshop/local-hosting/multipass
```

Log Observer Connect:

ご自身の Splunk Observability Cloud Suite Org または Splunk インスタンスを使用する場合は、新しい **Log Observer Connect** 接続の作成が必要になることがあります。
[Splunk Cloud](https://docs.splunk.com/observability/en/logs/scp.html#logs-scp) または [Splunk Enterprize](https://docs.splunk.com/observability/en/logs/set-up-logconnect.html) 用の[ドキュメント](https://docs.splunk.com/observability/en/logs/lo-connect-landing.html)に記載されている手順に従ってください。

ご自身の **Log Observer Connect** 接続を実行する際の追加要件は次のとおりです。

- **splunk4rookies-workshop** という名前のインデックスを作成する
- **Log observer Connect** 接続で使用するサービスアカウントユーザーが **splunk4rookies-workshop** インデックスにアクセスできることを確認する（すべてのワークショップのログデータはこのインデックスに送信されるため、他のインデックスはすべて削除して構いません）

Terraform を初期化します。

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

Terraform 変数ファイルを作成します。変数は `terrform.tfvars` ファイルに保存されており、コピーして編集するためのテンプレート `terraform.tfvars.template` が提供されています。

```bash
cp terraform.tfvars.template terraform.tfvars
```

以下の Terraform 変数が必須です。

- `swipe_id`: インスタンスの [SWiPE ID](https://swipe.splunk.com/)
- `splunk_index`: ログ送信先の Splunk Index。デフォルトは `splunk4rookies-workshop`。

インスタンスタイプ変数:

- `splunk_presetup`: 事前構成済みのインスタンス（OTel Collector と RUM 有効化済みの Online Boutique がデプロイされた状態）を提供します。デフォルトは `false` です。
- `splunk_diab`: Demo-in-a-Box をインストールして実行します。デフォルトは `false` です。
- `tagging_workshop`: Tagging Workshop をインストールして構成します。デフォルトは `false` です。
- `otel_demo` : OpenTelemetry Astronomy Shop Demo をインストールして構成します。これには `splunk_presetup` が `false` に設定されている必要があります。デフォルトは `false` です。

任意の高度な変数:

- `wsversion`: ワークショップの開発作業を行う場合は `main` に設定し、それ以外の場合は省略できます。
- `architecture`: 適切なアーキテクチャ（`arm64` または `amd64`）を設定します。デフォルトは `arm64` で、Apple Silicon に適しています。

`terraform plan` を実行してすべての構成に問題がないか確認します。問題がなければ `terraform apply` を実行してインスタンスを作成します。

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

インスタンスの作成が成功したら（数分かかる場合があります）、上記の出力にある `name` を使用して `exec` でインスタンスに入ります。Multipass インスタンスのパスワードは `Splunk123!` です。

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

インスタンスを検証します。

```bash
kubectl version --output=yaml
```

インスタンスを削除する場合は、まずインスタンスから抜けたことを確認してから、次のコマンドを実行します。

```bash
terraform destroy
```
