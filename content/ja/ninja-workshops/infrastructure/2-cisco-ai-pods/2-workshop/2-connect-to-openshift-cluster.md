---
title: OpenShiftクラスターへの接続
linkTitle: 2. OpenShiftクラスターへの接続
weight: 2
time: 5 minutes
---

## EC2インスタンスへの接続

各参加者用にAWS/EC2上にUbuntu Linuxインスタンスを用意しています。

インストラクターから提供されたIPアドレスとパスワードを使用して、以下のいずれかの方法でEC2インスタンスに接続します。

* Mac OS / Linux
  * ssh splunk@IPアドレス
* Windows 10+
  * OpenSSHクライアントを使用
* それ以前のバージョンのWindows
  * Puttyを使用

## ワークショップ参加者番号の設定

インストラクターが各参加者に1から30までの番号を割り当てます。
この番号を環境変数に保存し、ワークショップ全体を通して使用するため覚えておいてください。

``` bash
export PARTICIPANT_NUMBER=<your participant number>
```

## OpenShift CLIのインストール

OpenShiftクラスターにアクセスするために、OpenShift CLIをインストールする必要があります。

以下のコマンドを使用して、OpenShift CLIバイナリをEC2インスタンスに直接ダウンロードします。

````
curl -L -O https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/stable/openshift-client-linux.tar.gz
````

内容を展開します。

````
tar -xvzf openshift-client-linux.tar.gz
````

生成されたファイル（`oc` と `kubectl`）をパスに含まれる場所に移動します。例えば以下のようにします。

``` bash
sudo mv oc /usr/local/bin/oc
sudo mv kubectl /usr/local/bin/kubectl
```

## OpenShiftクラスターへの接続

Kube設定ファイルがsplunkユーザーによって変更可能であることを確認します。

``` bash
chmod 600 /home/splunk/.kube/config
```

ワークショップ主催者から提供されたクラスターAPI URLとパスワードを使用して、OpenShiftクラスターにログインします。

``` bash
oc login https://api.<cluster-domain>:443 -u participant$PARTICIPANT_NUMBER -p '<password>'
```

OpenShiftクラスターに接続されていることを確認します。

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
