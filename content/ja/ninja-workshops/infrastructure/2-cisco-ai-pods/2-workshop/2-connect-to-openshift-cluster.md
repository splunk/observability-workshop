---
title: OpenShift クラスターへの接続
linkTitle: 2. OpenShift クラスターへの接続
weight: 2
time: 5 minutes
---

## EC2 インスタンスへの接続

各参加者用に AWS/EC2 上に Ubuntu Linux インスタンスを用意しています。

講師から提供された IP アドレスとパスワードを使用して、以下のいずれかの方法で EC2 インスタンスに接続します。

* Mac OS / Linux
    * ssh splunk@IP address
* Windows 10+
    * OpenSSH クライアントを使用
* それ以前のバージョンの Windows
    * Putty を使用

## ワークショップ参加者番号の設定

講師が各参加者に 1 から 30 までの番号を割り当てます。
この番号を環境変数に保存してください。ワークショップ全体を通して使用するため、番号を覚えておいてください。

``` bash
export PARTICIPANT_NUMBER=<your participant number>
```

## OpenShift CLI のインストール

OpenShift クラスターにアクセスするために、OpenShift CLI をインストールする必要があります。

以下のコマンドを使用して、OpenShift CLI バイナリを EC2 インスタンスに直接ダウンロードします。

````
curl -L -O https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/stable/openshift-client-linux.tar.gz
````

コンテンツを展開します。

````
tar -xvzf openshift-client-linux.tar.gz
````

生成されたファイル（`oc` と `kubectl`）を、パスに含まれている場所に移動します。例えば以下のようにします。

``` bash
sudo mv oc /usr/local/bin/oc
sudo mv kubectl /usr/local/bin/kubectl
```

## OpenShift クラスターへの接続

Kube config ファイルが splunk ユーザーによって変更可能であることを確認します。

``` bash
chmod 600 /home/splunk/.kube/config
```

ワークショップ主催者から提供されたクラスター API URL とパスワードを使用して、OpenShift クラスターにログインします。

``` bash
oc login https://api.<cluster-domain>:443 -u participant$PARTICIPANT_NUMBER -p '<password>'
```

OpenShift クラスターに接続されていることを確認します。

{{< tabs >}}
{{% tab title="スクリプト" %}}

``` bash
oc whoami --show-server
```

{{% /tab %}}
{{% tab title="出力例" %}}

``` bash
https://api.***.openshiftapps.com:443
```

{{% /tab %}}
{{< /tabs >}}
