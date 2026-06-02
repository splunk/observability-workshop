---
title: OpenShift クラスターへの接続
linkTitle: 2. OpenShift クラスターへの接続
weight: 2
time: 5 minutes
---

## EC2 インスタンスへの接続

参加者の皆さま向けに、AWS/EC2 上に Ubuntu Linux インスタンスを用意しています。

インストラクターから提供された IP アドレスとパスワードを使って、以下のいずれかの方法で EC2 インスタンスに接続してください。

* Mac OS / Linux
  * ssh splunk@IP address
* Windows 10 以降
  * OpenSSH クライアントを使用してください
* それ以前のバージョンの Windows
  * Putty を使用してください

## ワークショップ参加者番号の設定

インストラクターから各参加者に 1 から 30 までの番号が割り当てられます。
この番号は、ワークショップ全体を通じて使用するため、環境変数に保存し、忘れないようにしてください。

``` bash
export PARTICIPANT_NUMBER=<your participant number>
```

## OpenShift CLI のインストール

OpenShift クラスターにアクセスするために、OpenShift CLI をインストールする必要があります。

以下のコマンドを使用して、OpenShift CLI のバイナリを EC2 インスタンスに直接ダウンロードできます。

````
curl -L -O https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/stable/openshift-client-linux.tar.gz
````

ファイルを展開します。

````
tar -xvzf openshift-client-linux.tar.gz
````

展開されたファイル（`oc` と `kubectl`）を、PATH に含まれる場所に移動します。例えば次のように実行します。

``` bash
sudo mv oc /usr/local/bin/oc
sudo mv kubectl /usr/local/bin/kubectl
```

## OpenShift クラスターへの接続

splunk ユーザーが Kube 設定ファイルを変更できるようにします。

``` bash
chmod 600 /home/splunk/.kube/config
```

ワークショップの主催者から提供されたクラスター API URL とパスワードを使用して、OpenShift クラスターにログインします。

``` bash
oc login https://api.<cluster-domain>:443 -u participant$PARTICIPANT_NUMBER -p '<password>'
```

OpenShift クラスターに接続できていることを確認します。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
oc whoami --show-server 
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
https://api.***.openshiftapps.com:443
```

{{% /tab %}}
{{< /tabs >}}
