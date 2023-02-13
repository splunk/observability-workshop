---
title: Monitoring as Code 
linkTitle: Plan, Apply, Destroy
weight: 6
isCJKLanguage: true
---

* Terraform[^1] を使用して Observability Cloud のダッシュボードとディテクターを管理します。
* Terraform のSplunk Provider[^2] を初期化します
* Terraformを実行して、Splunk Terraform Provider を使用してコードからディテクターとダッシュボードを作成します。
* Terraformでディテクターやダッシュボードを削除する方法を確認します。

---

## 1. 初期設定

Monitoring as Codeは、infrastructure as Codeと同じアプローチを採用しています。アプリケーション、サーバー、その他のインフラコンポーネントと同じようにモニタリングを管理できます。

Monitoring as Codeでは、可視化したり、何を監視するか定義したり、いつアラートを出すかなどを管理します。つまり、監視設定、プロセス、ルールをバージョン管理、共有、再利用することができます。

Splunk Terraform Providerの完全なドキュメントは[こちら](https://registry.terraform.io/providers/splunk-terraform/signalfx/latest/docs)にあります。

AWS/EC2 インスタンスにログインして、`o11y-cloud-jumpstart` ディレクトリに移動します

{{< tabs >}}
{{% tab name="Change directory" %}}
cd observability-content-contrib/integration-examples/terraform-jumpstart
{{</tab >}}
{{< /tabs >}}

必要な環境変数は、[Helmによるインストール](../../gdi/k3s/#2-helm%E3%81%AB%E3%82%88%E3%82%8B%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB) ですでに設定されているはずです。そうでない場合は、以下の Terraform のステップで使用するために、以下の環境変数を作成してください。

{{< tabs >}}
{{% tab name="Environment Variables" %}}
export ACCESS_TOKEN=<replace_with_O11y-Workshop-ACCESS_token>
export REALM=<replace_with_splunk_realm>
{{</tab >}}
{{< /tabs >}}

Terraform を初期化し、Splunk Terraform Provider を最新版にアップグレードします。

{{% notice title="Note: SignalFx Terraform Provider のアップグレード" style="info" %}}
Splunk Terraform Provider の新バージョンがリリースされるたびに、以下のコマンドを実行する必要があります。リリース情報は [GitHub](https://github.com/splunk-terraform/terraform-provider-signalfx/releases) で確認できます。
{{% /notice %}}

{{< tabs >}}
{{% tab name="Initialise Terraform" %}}
terraform init -upgrade
{{</tab >}}
{{% tab name="Initialise Output" lang="text" %}}
    Upgrading modules...
    - aws in modules/aws
    - azure in modules/azure
    - docker in modules/docker
    - gcp in modules/gcp
    - host in modules/host
    - kafka in modules/kafka
    - kubernetes in modules/kubernetes
    - parent_child_dashboard in modules/dashboards/parent
    - pivotal in modules/pivotal
    - rum_and_synthetics_dashboard in modules/dashboards/rum_and_synthetics
    - usage_dashboard in modules/dashboards/usage

    Initializing the backend...

    Initializing provider plugins...
    - Finding latest version of splunk-terraform/signalfx...
    - Installing splunk-terraform/signalfx v6.20.0...
    - Installed splunk-terraform/signalfx v6.20.0 (self-signed, key ID CE97B6074989F138)

    Partner and community providers are signed by their developers.
    If you'd like to know more about provider signing, you can read about it here:
    https://www.terraform.io/docs/cli/plugins/signing.html

    Terraform has created a lock file .terraform.lock.hcl to record the provider
    selections it made above. Include this file in your version control repository
    so that Terraform can guarantee to make the same selections by default when
    you run "terraform init" in the future.

    Terraform has been successfully initialized!

    You may now begin working with Terraform. Try running "terraform plan" to see
    any changes that are required for your infrastructure. All Terraform commands
    should now work.

    If you ever set or change modules or backend configuration for Terraform,
    rerun this command to reinitialize your working directory. If you forget, other
    commands will detect it and remind you to do so if necessary.
{{</tab >}}
{{< /tabs >}}

## 2. プランの作成

`terraform plan` コマンドで、実行計画を作成します。デフォルトでは、プランの作成は以下のように構成されています。

* 既に存在するリモートオブジェクトの現在の状態を読み込み、Terraform の状態が最新であることを確認します
* 現在の設定を以前の状態と比較し、相違点を抽出します
* 適用された場合にリモートオブジェクトと設定とを一致させるための、一連の変更アクションを提案します

plan コマンドだけでは、提案された変更を実際に実行はされなません。変更を適用する前に、以下のコマンドを実行して、提案された変更が期待したものと一致するかどうかを確認しましょう。

{{< tabs >}}
{{% tab name="Execution Plan" %}}
terraform plan -var="access_token=$ACCESS_TOKEN" -var="realm=$REALM" -var="sfx_prefix=[$(hostname)]"
{{</tab >}}
{{% tab name="Execution Plan Output" lang="text" %}}
Plan: 146 to add, 0 to change, 0 to destroy.
{{</tab >}}
{{< /tabs >}}

プランが正常に実行されれば、そのまま apply することができます。

---

## 3. プランの適用

`terraform apply` コマンドは、上記の Terraform プランで提案されたアクションを実行します。

この場合、新しい実行プランが自動的に作成され（`terraform plan`を実行したときと同様です）、指示されたアクションを実行する前にAccess Token、Realm（プレフィックスのデフォルトは`Splunk`）の提供とプランの承認を求められます。

このワークショップでは、プレフィックスがユニークである必要があります。以下の `terraform apply` を実行してください。

{{< tabs >}}
{{% tab name="Apply Plan" %}}
terraform apply -var="access_token=$ACCESS_TOKEN" -var="realm=$REALM" -var="sfx_prefix=[$(hostname)]"
{{</tab >}}
{{% tab name="Apply Plan Output" lang="text" %}}
Apply complete! Resources: 146 added, 0 changed, 0 destroyed.
{{</tab >}}
{{< /tabs >}}

適用が完了したら、 **Alerts → Detectors** でディテクターが作成されたことを確認してください。ディテクターのプレフィックスには、インスタンスのホスト名が入ります。プレフィックスの値を確認するには以下を実行してください。

{{< tabs >}}
{{% tab name="Echo Hostname" %}}
echo $(hostname)
{{</tab >}}
{{< /tabs >}}

新しいディテクターのリストが表示され、上から出力されたプレフィックスを検索することができます。

![Detectors](../../../images/detectors.png)

## 4. 苦労して作ったもの全てを壊す

`terraform destroy` コマンドは、Terraform の設定で管理されているすべてのリモートオブジェクトを破壊する便利な方法です。

通常、本番環境では長期保存可能なオブジェクトを破棄することはありませんが、Terraformでは開発目的で一時的なインフラを管理するために使用されることがあり、その場合は作業が終わった後に `terraform destroy` を実行して、一時的なオブジェクトをすべてクリーンアップすることができます。

それでは、ここまでで適用したダッシュボードとディテクターを全て破壊しましょう！

{{< tabs >}}
{{% tab name="Destroy" %}}
terraform destroy -var="access_token=$ACCESS_TOKEN" -var="realm=$REALM"
{{</tab >}}
{{% tab name="Destroy Output" lang="text" %}}
Destroy complete! Resources: 146 destroyed.
{{</tab >}}
{{< /tabs >}}

_**Alerts → Detectors**_ に移動して、すべてのディテクターが削除されたことを確認してください。

![Destroyed](../../../images/destroy.png)

[^1]:
    Terraform は、インフラを安全かつ効率的に構築、変更、バージョン管理するためのツールです。Terraform は、既存の一般的なサービスプロバイダーだけでなく、様々なカスタムソリューションも管理できます。

    Terraform の設定ファイルには、単一のアプリケーションまたはデータセンター全体を実行するために必要なコンポーネントをに記述します。Terraform はそれを受けて、望ましい状態に到達するために何をするかを記述した実行プランを生成し、記述されたインフラを構築するために実行します。設定が変更されても、Terraform は何が変更されたかを判断し、差分の実行プランを作成して適用することができます。

    Terraform が管理できるインフラには、計算機インスタンス、ストレージ、ネットワークなどのローレベルのコンポーネントや、DNSエントリ、SaaS機能などのハイレベルのコンポーネントが含まれます。
[^2]:
    プロバイダーは、APIのインタラクションを理解し、リソースを公開する責務があります。一般的にプロバイダーは、IaaS（Alibaba Cloud、AWS、GCP、Microsoft Azure、OpenStackなど）、PaaS（Herokuなど）、またはSaaSサービス（Splunk、Terraform Cloud、DNSimple、Cloudflareなど）があります。
