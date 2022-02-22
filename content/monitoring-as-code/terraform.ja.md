# Monitoring as Code - ラボ概要

* Terraform[^1] を使用して Observability Cloud のダッシュボードとディテクターを管理します。
* Terraform のSplunk Provider[^2] を初期化します
* Terraformを実行して、Splunk Terraform Provider を使用してコードからディテクターとダッシュボードを作成します。
* Terraformでディテクターやダッシュボードを削除する方法を確認します。

---

## 1. 初期設定

Monitoring as Codeは、infrastructure as Codeと同じアプローチを採用しています。アプリケーション、サーバー、その他のインフラコンポーネントと同じようにモニタリングを管理できます。

Monitoring as Codeでは、可視化したり、何を監視するか定義したり、いつアラートを出すかなどを管理します。つまり、監視設定、プロセス、ルールをバージョン管理、共有、再利用することができます。

Splunk Terraform Providerの完全なドキュメントは[こちら](https://registry.terraform.io/providers/splunk-terraform/signalfx/latest/docs)にあります。

AWS/EC2 インスタンスにログインして、`signalfx-jumpstart` ディレクトリに移動します

=== "シェルコマンド"

    ```text
    cd ~/signalfx-jumpstart
    ```

必要な環境変数は、[Installation using Helm](../../otel/k3s/#2-installation-using-helm) ですでに設定されているはずです。そうでない場合は、以下の Terraform のステップで使用するために、以下の環境変数を作成してください。

=== "シェルコマンド"

    ```
    export ACCESS_TOKEN=<replace_with_default_access_token>
    export REALM=<replace_with_splunk_realm>
    ```

Terraform を初期化し、Splunk Terraform Provider を最新版にアップグレードします。

!!! note "SignalFx Terraform Provider のアップグレード"
    Splunk Terraform Provider の新バージョンがリリースされるたびに、以下のコマンドを実行する必要があります。リリース情報は[GitHub](https://github.com/splunk-terraform/terraform-provider-signalfx/releases){: target=_blank}で確認できます。

=== "シェルコマンド"

    ```text
    terraform init -upgrade
    ```

=== "出力"

    ```
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
    - usage_dashboard in modules/dashboards/usage

    Initializing the backend...

    Initializing provider plugins...
    - Finding latest version of splunk-terraform/signalfx...
    - Installing splunk-terraform/signalfx v6.7.3...
    - Installed splunk-terraform/signalfx v6.7.3 (signed by a HashiCorp partner, key ID 8B5755E223754FC9)

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
    ```

## 2. プランの作成

`terraform plan` コマンドは、実行計画を作成します。デフォルトでは、プランの作成は以下のように構成されています。

* 既に存在するリモートオブジェクトの現在の状態を読み込み、Terraform の状態が最新であることを確認します
* 現在の設定を以前の状態と比較し、相違点を抽出します
* 適用された場合にリモートオブジェクトと設定とを一致させるための、一連の変更アクションを提案します

plan コマンドだけでは、提案された変更を実際に実行はされなません。変更を適用する前に、以下のコマンドを実行して、提案された変更が期待したものと一致するかどうかを確認しましょう。

=== "シェルコマンド"

    ```text
    terraform plan -var="access_token=$ACCESS_TOKEN" -var="realm=$REALM" -var="sfx_prefix=[$(hostname)]"
    ```

=== "出力例"

    ```
    Plan: 92 to add, 0 to change, 0 to destroy.
    ```

プランが正常に実行されれば、そのまま適用することができます。

---

## 3. プランの適用

`terraform apply` コマンドは、上記の Terraform プランで提案されたアクションを実行します。

この場合、新しい実行プランが自動的に作成され（`terraform plan`を実行したときと同様です）、指示されたアクションを実行する前にAccess Token、Realm（プレフィックスのデフォルトは`Splunk`）の提供とプランの承認を求められます。

このワークショップでは、プレフィックスがユニークである必要があります。以下の `terraform apply` を実行してください。

=== "シェルコマンド"

    ```text
    terraform apply -var="access_token=$ACCESS_TOKEN" -var="realm=$REALM" -var="sfx_prefix=[$(hostname)]"
    ```

=== "出力例"

    ```
    Apply complete! Resources: 92 added, 0 changed, 0 destroyed.
    ```

適用が完了したら、 **Alerts → Detectors** でディテクターが作成されたことを確認してください。ディテクターのプレフィックスには、インスタンスのホスト名が入ります。プレフィックスの値を確認するには以下を実行してください。

=== "シェルコマンド"

    ```text
    echo $(hostname)
    ```

 新しいディテクターのリストが表示され、上から出力されたプレフィックスを検索することができます。

![Detectors](/images/monitoring-as-code/detectors.png)

## 3. 苦労して作ったもの全てを壊す

`terraform destroy` コマンドは、Terraform の設定で管理されているすべてのリモートオブジェクトを破壊する便利な方法です。

通常、本番環境では長期保存可能なオブジェクトを破棄することはありませんが、Terraformでは開発目的で一時的なインフラを管理するために使用されることがあり、その場合は作業が終わった後に `terraform destroy` を実行して、一時的なオブジェクトをすべてクリーンアップすることができます。

それでは、ここまでで適用したダッシュボードとディテクターを全て破壊しましょう！

=== "シェルコマンド"

    ```text
    terraform destroy -var="access_token=$ACCESS_TOKEN" -var="realm=$REALM"
    ```

=== "出力例"

    ```
    Destroy complete! Resources: 92 destroyed.
    ```

_**Alerts → Detectors**_ に移動して、すべてのディテクターが削除されたことを確認してください。

![Destroyed](/images/monitoring-as-code/destroy.png)

[^1]:
    Terraform は、インフラを安全かつ効率的に構築、変更、バージョン管理するためのツールです。Terraform は、既存の一般的なサービスプロバイダーだけでなく、様々なカスタムソリューションも管理できます。

    Terraform の設定ファイルには、単一のアプリケーションまたはデータセンター全体を実行するために必要なコンポーネントをに記述します。Terraform はそれを受けて、望ましい状態に到達するために何をするかを記述した実行プランを生成し、記述されたインフラを構築するために実行します。設定が変更されても、Terraform は何が変更されたかを判断し、差分の実行プランを作成して適用することができます。

    Terraform が管理できるインフラには、計算機インスタンス、ストレージ、ネットワークなどのローレベルのコンポーネントや、DNSエントリ、SaaS機能などのハイレベルのコンポーネントが含まれます。
[^2]:
    プロバイダーは、APIのインタラクションを理解し、リソースを公開する責務があります。一般的にプロバイダーは、IaaS（Alibaba Cloud、AWS、GCP、Microsoft Azure、OpenStackなど）、PaaS（Herokuなど）、またはSaaSサービス（Splunk、Terraform Cloud、DNSimple、Cloudflareなど）があります。
